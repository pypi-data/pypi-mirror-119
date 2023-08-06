#!/usr/bin/python
# Based on previous work done by Rafael C. Carrasco, José A. Mañas
# (Communications of the ACM 30(7), 1987) and Javier Sober
# https://github.com/postdataproject/skas-archived/blob/devel/skas/phonmet/syll/grapheme2syllable.py
#
# Presyllabification and syllabification rules are taken from
# Antonio Ríos Mestre's 'El Diccionario Electrónico Fonético del Español'
# https://www.raco.cat/index.php/Elies/article/view/194843
# http://elies.rediris.es/elies4/Fon2.htm
# http://elies.rediris.es/elies4/Fon8.htm
import copy
import re
from collections import Counter
from itertools import product

from spacy.tokens import Doc

from .pipeline import load_pipeline
from .rhymes import analyze_rhyme
from .schemes import scheme
from .structures import STRUCTURES_LENGTH
from .syllabification import ALTERNATIVE_SYLLABIFICATION
from .syllabification import CONSONANT_CLUSTER_RE
from .syllabification import CONSONANT_GROUP
from .syllabification import CONSONANT_GROUP_EXCEPTION_DL
from .syllabification import CONSONANT_GROUP_EXCEPTION_LL
from .syllabification import HIATUS_FIRST_VOWEL_RE
from .syllabification import LIAISON_FIRST_PART
from .syllabification import LIAISON_SECOND_PART
from .syllabification import LOWERING_DIPHTHONGS_WITH_H
from .syllabification import POSSESSIVE_PRON_UNSTRESSED
from .syllabification import PREFIX_DES_WITH_CONSONANT_RE
from .syllabification import PREFIX_SIN_WITH_CONSONANT_RE
from .syllabification import RAISING_DIPHTHONGS_WITH_H
from .syllabification import SPACE
from .syllabification import STRESSED_PRON
from .syllabification import STRESSED_UNACCENTED_MONOSYLLABLES
from .syllabification import STRESSED_WEAK_VOWELS
from .syllabification import STRONG_VOWELS
from .syllabification import SYLLABIFICATOR_FOREIGN_WORDS_DICT
from .syllabification import UNSTRESSED_FORMS
from .syllabification import UNSTRESSED_UNACCENTED_MONOSYLLABLES
from .syllabification import W_VOWEL_GROUP
from .syllabification import WEAK_VOWELS
from .syllabification import accents_re
from .syllabification import letter_clusters_re
from .syllabification import paroxytone_re


def have_prosodic_liaison(first_syllable, second_syllable):
    """Checks for prosodic liaison between two syllables

    :param first_syllable: Dictionary with key syllable (str) and is_stressed (bool) representing
        the first syllable
    :param second_syllable: Dictionary with key syllable (str) and is_stressed (bool)
        representing the second syllable
    :return: `True` if there is prosodic liaison and `False` otherwise
    :rtype: bool
    """
    if second_syllable['syllable'][0].lower() == 'y' and (
            len(second_syllable['syllable']) > 1) and (
            second_syllable['syllable'][1].lower() in set('aeiouáéíúó')):
        return False
    else:
        return (first_syllable['syllable'][-1] in LIAISON_FIRST_PART
                and second_syllable['syllable'][0] in LIAISON_SECOND_PART)


def get_syllables_word_end(words):
    """Get a list of syllables from a list of words extracting word boundaries

    :param words: List of dictonaries of syllables for each word in a line
    :return: List of dictionaries of syllables with an extra is_word_end key
    :rtype: list
    """
    syllables = []
    for word in words:
        if "symbol" in word:
            continue
        for i, syllable in enumerate(word["word"]):
            if i == len(word["word"]) - 1:
                syllable["is_word_end"] = True
            syllables.append(syllable)
    return syllables


def get_phonological_groups(word_syllables, liaison_type="synalepha",
                            breakage_func=None, liaison_positions=None):
    """Get a list of dictionaries for each phonological group on a line
    and joins the syllables to create phonological groups (pronounced together)
    according to a type of liaison, either synaloepha or sinaeresis

    :param word_syllables: List of dictionaries for each word of the line
    :param liaison_type: Which liaison is going to be performed synalepha or
        sinaeresis
    :param breakage_func: Function to decide when not to break a liaison that is
        specified in liaison_positions
    :param liaison_positions: Positions of the liaisons
    :return: A list of conjoined syllables
    :rtype: list
    """
    syllables = word_syllables[:]
    liaison_property = f"has_{liaison_type}"
    if liaison_positions is None:
        liaison_positions = [int(syllable.get(liaison_property, 0))
                             for syllable in syllables]
    skip_next = False
    while sum(liaison_positions) > 0:
        liaison_index = []
        reduced_syllables = []
        for idx, syllable in enumerate(syllables):
            if skip_next:
                skip_next = False
                continue
            breakage = False
            if idx < len(syllables) - 1:
                next_syllable = syllables[idx + 1]
                breakage = (
                        breakage_func is not None
                        and breakage_func(liaison_type, syllable, next_syllable)
                )
            if liaison_positions[idx] and not breakage:
                boundary_index = syllable.get(f'{liaison_type}_index', [])
                boundary_index.append(len(syllable.get('syllable')) - 1)
                liaison = {
                    'syllable': (syllable["syllable"]
                                 + next_syllable["syllable"]),
                    'is_stressed': (syllable["is_stressed"]
                                    or next_syllable["is_stressed"]),
                    f'{liaison_type}_index': boundary_index,
                }
                for prop in (liaison_property, "is_word_end"):
                    has_prop = next_syllable.get(prop, None)
                    if has_prop is not None:
                        liaison[prop] = has_prop
                reduced_syllables.append(liaison)
                liaison_index.append(liaison_positions[idx + 1])
                skip_next = True
            else:
                reduced_syllables.append(syllable)
                liaison_index.append(0)
        liaison_positions = liaison_index
        syllables = reduced_syllables
    poem_dict = clean_phonological_groups(
        syllables, liaison_positions, liaison_property
    )
    return poem_dict


def clean_phonological_groups(groups, liaison_positions, liaison_property):
    """Clean phonological groups so their liaison property is consistently set
    according to the the liaison positions

    :param groups: Phonological groups to be cleaned
    :param liaison_positions: Positions of the liaisons
    :param liaison_property: The liaison type (synaeresis or synalepha)
    :return: Cleaned phonological groups
    :rtype: dict
    """
    clean_groups = []
    for idx, group in enumerate(groups):
        if liaison_property in group:
            clean_groups.append({
                **group, liaison_property: bool(liaison_positions[idx])
            })
        else:
            clean_groups.append(group)
    return clean_groups


def get_length_ranges(phonological_groups, length):
    count_liaisons = 0
    for syllable in phonological_groups:
        count_liaisons += len(syllable.get("synalepha_index", []))
        count_liaisons += len(syllable.get("sinaeresis_index", []))
    length_ranges_dict = {
        "min_length": length, "max_length": length + count_liaisons}
    return length_ranges_dict


def get_rhythmical_pattern(phonological_groups, rhythm_format="pattern",
                           rhyme_analysis=False):
    """Gets a rhythm pattern for a poem in either "pattern": "-++-+-+-"
    "binary": "01101010" or "indexed": [1,2,4,6] format

    :param phonological_groups: a dictionary with the syllables of the line
    :param rhythm_format: The output format for the rhythm
    :param rhyme_analysis: Whether or not rhyme analysis is to be performed
    :return: Dictionary with with rhythm and phonological groups
    :rtype: dict
    """
    stresses = get_stresses(phonological_groups)
    stress = format_stress(stresses, rhythm_format)
    stresses_length = len(stresses)
    rhythmical_pattern = {
        "stress": stress,
        "type": rhythm_format,
        "length": stresses_length,
    }
    if rhyme_analysis:
        length_range = get_length_ranges(phonological_groups, stresses_length)
        rhythmical_pattern.update({
            "length_range": length_range
        })
    return rhythmical_pattern


def get_stresses(phonological_groups):
    """Gets a list of stress marks, `True` for stressed, `False` for unstressed
    from a list of phonological groups applying rules depending on the ending
    stress.

    :param phonological_groups: a dictionary with the phonological groups
        (syllables) of the line
    :return: List of boolean values indicating whether a group is
        stressed (`True`) or not (`False`)
    :rtype: list
    """
    stresses = []
    last_word_syllables = []
    for group in phonological_groups:
        stresses.append(group["is_stressed"])
    for group in phonological_groups:
        last_word_syllables.append(group.get("is_word_end", False))
    # Get position for the last syllable of the penultimate word
    if last_word_syllables.count(True) > 1:
        penultimate_word = -(
            [i for i, n in enumerate(last_word_syllables[::-1]) if n][1] + 1)
    else:
        penultimate_word = None
    last_stress = -(stresses[::-1].index(True) + 1)
    # Oxytone (Aguda)
    if last_stress == -1:
        stresses.append(False)
    # Paroxytone (Esdrújula)
    elif last_stress == -3:
        if penultimate_word is None:
            stresses.pop()
        elif last_stress > penultimate_word:
            stresses.pop()
    return stresses


def format_stress(stresses, rhythm_format="pattern", indexed_separator="-"):
    """Converts a list of boolean elements into a string that matches the chosen
        rhythm format:
        "indexed": 2,5,8
        "pattern": -++--+-+-
        "binary": 01101001

    :param stresses: List of boolean elements representing stressed syllables
    :param rhythm_format: Format to be used: indexed, pattern, or binary
    :param indexed_separator: String to use as a separator for indexed pattern
    :return: String with the stress pattern
    :rtype: str
    """
    separator = ""
    if rhythm_format == 'indexed':
        stresses = [
            str(index + 1) for index, stress in enumerate(stresses) if stress
        ]
        separator = indexed_separator
    elif rhythm_format == 'binary':
        stresses = map(lambda stress: str(int(stress)), stresses)
    else:  # rhythm_format == 'pattern':
        stresses = map(lambda stress: "+" if stress else "-", stresses)
    return separator.join(stresses)


"""
Syllabifier functions
"""


def apply_exception_rules(word):
    """Applies presyllabification rules to a word,
    based on Antonio Ríos Mestre's work

    :param word: A string to be checked for exceptions
    :return: A string with the presyllabified word
    :rtype: str
    """
    # Vowel + w + vowel group
    if W_VOWEL_GROUP.match(word):
        match = W_VOWEL_GROUP.search(word)
        if match is not None:
            word = "-".join(match.groups())
    # Consonant groups with exceptions for LL and DL
    if CONSONANT_GROUP.match(word):
        match = CONSONANT_GROUP.search(word)
        if match is not None:
            word = "-".join(match.groups())
    if CONSONANT_GROUP_EXCEPTION_LL.match(word):
        match = CONSONANT_GROUP_EXCEPTION_LL.search(word)
        if match is not None:
            word = "-".join(match.groups())
    if CONSONANT_GROUP_EXCEPTION_DL.match(word):
        match = CONSONANT_GROUP_EXCEPTION_DL.search(word)
        if match is not None:
            word = "-".join(match.groups())
    # Prefix 'sin' followed by consonant
    if PREFIX_SIN_WITH_CONSONANT_RE.match(word):
        match = PREFIX_SIN_WITH_CONSONANT_RE.search(word)
        if match is not None:
            word = "-".join(match.groups())
    # Prefix 'des' followed by consonant
    if PREFIX_DES_WITH_CONSONANT_RE.match(word):
        match = PREFIX_DES_WITH_CONSONANT_RE.search(word)
        if match is not None:
            word = "-".join(match.groups())
    return word


def apply_exception_rules_post(word):
    """Applies presyllabification rules to a word,
    based on Antonio Ríos Mestre's work

    :param word: A string to be checked for exceptions
    :return: A string with the presyllabified word with hyphens
    :rtype: str
    """
    # We make one pass for every match found so we can perform
    # several substitutions
    matches = HIATUS_FIRST_VOWEL_RE.findall(word)
    if matches:
        for _ in matches[0]:
            word = re.sub(HIATUS_FIRST_VOWEL_RE, r'\1\2-\3', word)
    regexes = (CONSONANT_CLUSTER_RE, LOWERING_DIPHTHONGS_WITH_H,
               RAISING_DIPHTHONGS_WITH_H)
    for regex in regexes:
        matches = regex.findall(word)
        if matches:
            for _ in matches[0]:
                word = re.sub(regex, r'\1\2\3', word)
    return word


def syllabify(word, alternative_syllabification=False):
    """Syllabifies a word.

    :param word: The word to be syllabified.
    :param alternative_syllabification: Wether or not the alternative
        syllabification is used
    :return: List of syllables and exceptions where appropriate.
    :rtype: list
    """
    output = ""
    original_word = word
    # Checks if word exists on the foreign words dictionary
    if word in SYLLABIFICATOR_FOREIGN_WORDS_DICT:
        output = SYLLABIFICATOR_FOREIGN_WORDS_DICT[word]
    else:
        word = apply_exception_rules(word)
        while len(word) > 0:
            output += word[0]
            # Returns first matching pattern.
            m = letter_clusters_re.search(word)
            if m is not None:
                # Adds hyphen to syllables if regex pattern is not 5, 8, 11
                output += "-" if m.lastindex not in {5, 8, 11} else ""
            word = word[1:]
        output = apply_exception_rules_post(output)
    # Remove empty elements created during syllabification
    output = list(filter(bool, output.split("-")))
    if (alternative_syllabification
            and original_word.lower() in ALTERNATIVE_SYLLABIFICATION):
        return ALTERNATIVE_SYLLABIFICATION[original_word.lower()][1][0]
    else:
        return (output,
                ALTERNATIVE_SYLLABIFICATION.get(original_word, (None, ()))[1])


def get_orthographic_accent(syllable_list):
    """Given a list of str representing syllables,
    return position in the list of a syllable bearing
    orthographic stress (with the acute accent mark in Spanish)

    :param syllable_list: list of syllables as str or unicode each
    :return: Position or None if no orthographic stress
    :rtype: int
    """
    word = "|".join(syllable_list)
    match = accents_re.search(word)
    position = None
    if match is not None:
        last_index = match.span()[0]
        position = word[:last_index].count("|")
    return position


def is_paroxytone(syllables):
    """Given a list of str representing syllables from a single word,
    check if it is paroxytonic (llana) or not

    :param syllables: List of syllables as str
    :return: `True` if paroxytone, `False` if not
    :rtype: bool
    """
    if not get_orthographic_accent("".join(syllables)):
        return paroxytone_re.search(syllables[len(syllables) - 1]) is not None
    return False


def spacy_tag_to_dict(tag):
    """Creates a dict from spacy pos tags

    :param tag: Extended spacy pos tag
        ("Definite=Ind|Gender=Masc|Number=Sing|PronType=Art")
    :return: A dictionary in the form of
        "{'Definite': 'Ind', 'Gender': 'Masc', 'Number': 'Sing',
        'PronType': 'Art'}"
    :rtype: dict
    """
    if tag and '=' in tag:
        return dict([t.split('=') for t in tag.split('|')])
    else:
        return {}


def get_word_stress(word, pos, tag, alternative_syllabification=False,
                    is_last_word=False):
    """Gets a list of syllables from a word and creates a list with syllabified
    word and stressed syllable index

    :param word: Word string
    :param is_last_word: Wether or not the word is the last one of a verse
    :param alternative_syllabification: Wether or not the alternative
        syllabification is used
    :param pos: PoS tag from spacy ("DET")
    :param tag: Extended PoS tag info from spacy
        ("Definite=Ind|Gender=Masc|Number=Sing|PronType=Art")
    :return: Dict with [original syllab word, stressed syllabified word,
        negative index position of stressed syllable or 0 if not stressed]
    :rtype: dict
    """
    syllable_list, _ = syllabify(word, alternative_syllabification)
    word_lower = word.lower()
    # Handle secondary stress on adverbs ending in -mente
    if pos == "ADV" and word_lower[-5:] == "mente" and len(word) > 5:
        root = word[:-5]
        mente = word[-5:]
        stress_root = get_word_stress(root, "ADJ", "")
        stress_mente = get_word_stress(mente, "NOUN", "")
        return {
            'word': stress_root['word'] + stress_mente['word'],
            "stress_position": stress_root['stress_position'] - len(
                stress_mente['word']),
            "secondary_stress_positions": [stress_mente['stress_position']],
        }
    # Bypass POS exceptions for the last word of a verse as it should always be
    # stressed
    if is_last_word:
        if len(syllable_list) == 1:
            stressed_position = -1
        else:
            tilde = get_orthographic_accent(syllable_list)
            if tilde is not None:
                stressed_position = -(len(syllable_list) - tilde)
            # Elif the word is paroxytone (llana)
            # we save the penultimate syllable.
            elif is_paroxytone(syllable_list):
                stressed_position = -2
            # If the word does not meet the above criteria that means
            # that it's an oxytone word (aguda).
            else:
                stressed_position = -1
    else:
        if len(syllable_list) == 1:
            first_monosyllable = syllable_list[0].lower()
            if ((first_monosyllable not in UNSTRESSED_UNACCENTED_MONOSYLLABLES)
                    and (
                        first_monosyllable in STRESSED_UNACCENTED_MONOSYLLABLES
                        or pos not in (
                                "SCONJ", "CCONJ", "DET", "PRON", "ADP")
                        or (pos == "PRON" and tag.get("Case") == "Nom")
                        or (pos == "DET" and tag.get("Definite") in (
                            "Dem", "Ind"))
                        or pos in (
                                "PROPN", "NUM", "NOUN", "VERB", "AUX",
                                "ADV")
                        or (pos == "ADJ" and tag.get("Poss",
                                                     None) != "Yes")
                        or (pos == "PRON"
                            and tag.get("PronType", None) in (
                                    "Prs", "Ind"))
                        or (pos == "DET" and tag.get("PronType",
                                                     None) == "Ind")
                        or (pos in ("ADJ", "DET"
                                           and tag.get("Poss",
                                                       None) == "Yes"))
                        or (pos in ("PRON", "DET")
                            and tag.get("PronType", None) in (
                                    "Exc", "Int", "Dem"))
                        or "".join(word).lower() in STRESSED_PRON) and (
                            word_lower not in UNSTRESSED_FORMS)):
                stressed_position = -1
            else:
                stressed_position = 0  # unstressed monosyllable
        else:
            tilde = get_orthographic_accent(syllable_list)
            if tilde is not None:
                stressed_position = tilde - len(syllable_list)
            elif (pos in ("INTJ", "PROPN", "NUM", "NOUN", "VERB", "AUX", "ADV")
                  or pos == "ADJ"
                  or (pos == "PRON" and tag.get("PronType", None) in (
                            "Prs", "Ind"))
                  or (pos == "DET" and tag.get("PronType", None) in (
                            "Dem", "Ind"))
                  or (pos == "DET" and tag.get("Definite", None) == "Ind")
                  or (pos == "PRON" and tag.get("Poss", None) == "Yes")
                  or (pos in ("PRON", "DET")
                      and tag.get("PronType", None) in ("Exc", "Int", "Dem"))
                  or (word_lower in STRESSED_PRON)) and (
                    word_lower not in UNSTRESSED_FORMS) and (
                    word_lower not in POSSESSIVE_PRON_UNSTRESSED):
                tilde = get_orthographic_accent(syllable_list)
                # If an orthographic accent exists,
                # the syllable negative index is saved
                if tilde is not None:
                    stressed_position = -(len(syllable_list) - tilde)
                # Elif the word is paroxytone (llana)
                # we save the penultimate syllable.
                elif is_paroxytone(syllable_list):
                    stressed_position = -2
                # If the word does not meet the above criteria that means
                # that it's an oxytone word (aguda).
                else:
                    stressed_position = -1
            else:
                stressed_position = 0  # unstressed
    out_syllable_list = []
    for index, syllable in enumerate(syllable_list):
        out_syllable_list.append(
            {
                "syllable": syllable,
                "is_stressed": len(syllable_list) - index == -stressed_position
            })
        if index < 1:
            continue
        # Sinaeresis
        first_syllable = syllable_list[index - 1]
        second_syllable = syllable
        if first_syllable and second_syllable and (
                (first_syllable[-1] in STRONG_VOWELS
                 and second_syllable[0] in STRONG_VOWELS)
                or (first_syllable[-1] in STRESSED_WEAK_VOWELS
                    and second_syllable[0] in STRONG_VOWELS)
                or (first_syllable[-1] in STRONG_VOWELS
                    and second_syllable[0] in WEAK_VOWELS)
                or (first_syllable[-1] in STRONG_VOWELS
                    and second_syllable[0] == "h"
                    and second_syllable[1] in STRONG_VOWELS)):
            out_syllable_list[index - 1].update({'has_sinaeresis': True})
    return {
        'word': out_syllable_list, "stress_position": stressed_position,
    }


def get_last_syllable(token_list):
    """Gets last syllable from a word in a dictionary

    :param token_list: list of dictionaries with line tokens
    :return: Last syllable
    :rtype: str
    """
    if len(token_list) > 0:
        for token in token_list[::-1]:
            if 'word' in token:
                return token['word'][-1]


def get_words(word_list, alternative_syllabification=False):
    """Gets a list of syllables from a word and creates a list with syllabified
    word and stressed syllable index

    :param word_list: List of spacy objects representing a word or sentence
    :param alternative_syllabification: Whether or not the alternative
        syllabification is used
    :return: List with [original syllab. word, stressed syllab. word, negative
        index position of stressed syllable]
    :rtype: list
    """
    syllabified_words = []
    for index, word in enumerate(word_list):
        if word.is_alpha:
            if '__' in word.tag_:
                pos, tag = word.tag_.split('__')
            else:
                pos = word.pos_ or ""
                tag = word.tag_ or ""
            tags = spacy_tag_to_dict(tag)
            # If it's the last word of a verse, mark it so it's always stressed
            # `is` is used here to be sure it's the same spacy object
            if word is [w for w in word_list if w.is_alpha][-1]:
                stressed_word = get_word_stress(word.text, pos, tags,
                                                alternative_syllabification,
                                                is_last_word=True)
            else:
                stressed_word = get_word_stress(word.text, pos, tags,
                                                alternative_syllabification)
            if word.pos_ in ("AUX", "VERB") and word._.affixes_length:
                stressed_word.update(
                    {'affixes_length': word._.affixes_length})
                stressed_word.update({'pos': word.pos_, 'tag': word.tag_})
            stressed_word.update({'pos': pos})
            syllabified_words.append(stressed_word)
        else:
            syllabified_words.append({"symbol": word.text})
    syllabified_words = join_affixes(syllabified_words)
    clean_word_list = [syll for syll in syllabified_words if "word" in syll]
    # Synalepha
    for index, word in enumerate(clean_word_list):
        if len(clean_word_list) != index + 1:
            first_syllable = clean_word_list[index]['word'][-1]
            second_syllable = clean_word_list[index + 1]['word'][0]
            if first_syllable and second_syllable and have_prosodic_liaison(
                    first_syllable, second_syllable):
                first_syllable.update({'has_synalepha': True})
    return syllabified_words


def join_affixes(line):
    """Join affixes of split words and recalculates stress

    :param line: List of syllabified words (dict)
    :return: List of syllabified words (dict) with joined affixes
    :rtype: list
    """
    syllabified_words = []
    indices_to_ignore = []
    for index, word in enumerate(line):
        affixes_length = word.get('affixes_length', None)
        if index in indices_to_ignore:
            continue
        elif affixes_length is None:
            syllabified_words.append(word)
        else:
            indices_to_ignore = range(index, index + affixes_length + 1)
            join_word = []
            for affix_index in indices_to_ignore:
                affix = line[affix_index]['word']
                join_word += [syll["syllable"] for syll in affix]
            word_stress = get_word_stress("".join(join_word), word["pos"],
                                          word["tag"])
            word_stress["word"][-1]["is_word_end"] = True
            syllabified_words.append(word_stress)
            # Add PoS information
            pos_list = [line[index]['pos'] for index in indices_to_ignore]
            join_pos = "+".join(pos_list)
            word_stress.update({'pos': join_pos})
    # Handle stress exception for certain paroxytone and proparoxytone words
    word_list = [token for token in syllabified_words if token.get("word")]
    last_word = word_list[-1]
    stresses_list = [syll["is_stressed"] for syll in last_word["word"]]
    if stresses_list.count(True) >= 1:
        last_word_stress = stresses_list.index(True) - len(last_word["word"])
        last_word_is_paroxytone = re.compile(r"VERB\+").match(last_word["pos"])
        last_word_is_adverb = last_word["pos"] == "ADV"
        if len(last_word["word"]) >= 3:
            # If last word is paroxytone and have enclitic pronouns, change the
            # stress to the last syllable and set the rest to False
            if last_word_stress == -3 and last_word_is_paroxytone:
                set_stress_exceptions(last_word)
                last_word["stress_position"] = -1
            # If last word is proparoxytone and is not and adverb, change the
            # stress to the last syllable and set the rest to False
            elif last_word_stress <= -4 and not last_word_is_adverb:
                set_stress_exceptions(last_word)
                last_word["stress_position"] = -1
    return syllabified_words if syllabified_words else line


def set_stress_exceptions(word):
    """Changes stresses of a word to only the last one

    :param word: The word that is going to be changed
    :return: Word with the new stresses
    """
    for idx, stress in enumerate(word["word"]):
        if idx != len(word["word"]) - 1:
            stress["is_stressed"] = False
        else:
            stress["is_stressed"] = True
    return word


def get_scansion(text, rhyme_analysis=False, rhythm_format="pattern",
                 rhythmical_lengths=None, split_stanzas_on=None,
                 pos_output=False, always_return_rhyme=False,
                 rhythmical_lengths_window=8, alternative_output=False):
    """Generates a list of dictionaries for each line

    :param text: Full text to be analyzed
    :param rhyme_analysis: Specify if rhyme analysis is to be performed
    :param rhythm_format: output format for rhythm analysis
    :param rhythmical_lengths: List with explicit rhythmical lengths per line
        that the analysed lines has to meet
    :param split_stanzas_on: Regular expression to split text in stanzas.
        Defaults to None for not splitting.
    :param pos_output: `True` or `False` for printing the PoS of the words
    :param always_return_rhyme: `True` or `False` for printing rhyme pattern
        even if no structure is detected
    :param rhythmical_lengths_window: Size of the window to calculate the most
        frequent line length when rhythmical_lengths is False. Defaults to 8
    :param alternative_output: Wheter or not to return the scansion in a
        new format compliant with postdata API
    :return: list of dictionaries per line
        (or list of list of dictionaries if split on stanzas)
    :rtype: list
    """
    if split_stanzas_on is None:
        return _get_scansion(
            text=text,
            rhyme_analysis=rhyme_analysis,
            rhythm_format=rhythm_format,
            rhythmical_lengths=rhythmical_lengths,
            pos_output=pos_output,
            always_return_rhyme=always_return_rhyme,
            rhythmical_lengths_window=rhythmical_lengths_window,
            alternative_output=alternative_output,
        )
    else:
        scansion = [
            _get_scansion(
                text=stanza,
                rhyme_analysis=rhyme_analysis,
                rhythm_format=rhythm_format,
                rhythmical_lengths=rhythmical_lengths,
                pos_output=pos_output,
                always_return_rhyme=always_return_rhyme,
                rhythmical_lengths_window=rhythmical_lengths_window,
                alternative_output=alternative_output,
            ) for stanza in re.compile(split_stanzas_on).split(text)
        ]
        if alternative_output and rhyme_analysis and always_return_rhyme:
            scansion = transform_scansion(scansion, text)
        return scansion


def _get_scansion(text, rhyme_analysis=False, rhythm_format="pattern",
                  rhythmical_lengths=None, split_stanzas_on=None,
                  pos_output=False, always_return_rhyme=False,
                  rhythmical_lengths_window=8, alternative_output=False):
    """Generates a list of dictionaries for each line

    :param text: Full text to be analyzed
    :param rhyme_analysis: Specify if rhyme analysis is to be performed
    :param rhythm_format: Output format for rhythm analysis
    :param rhythmical_lengths: List with explicit rhythmical lengths per line
        that the analysed lines has to meet
    :param split_stanzas_on: String or regular expression to split text in
        stanzas. Defaults to None for not splitting.
    :param pos_output: `True` or `False` for printing the PoS of the words
    :param always_return_rhyme: `True` or `False` for printing rhyme pattern
        even if no structure is detected
    :param rhythmical_lengths_window: Size of the window to calculate the most
        frequent line length when rhythmical_lengths is False. Defaults to 8
    :param alternative_output: Wheter or not to return the scansion in a
        new format compliant with postdata API
    :return: list of dictionaries per line
    :rtype: list
    """
    if isinstance(text, Doc):
        tokens = text
    else:
        nlp = load_pipeline()
        tokens = nlp(text)
    seen_tokens = []
    lines = []
    raw_tokens = []
    # Handle multi-line sentences and create the line with words
    for token in tokens:
        if (token.pos_ == SPACE
                and '\n' in token.orth_
                and len(seen_tokens) > 0):
            lines.append({"tokens": get_words(seen_tokens, False)})
            raw_tokens.append(seen_tokens)
            seen_tokens = []
        else:
            seen_tokens.append(token)
    if len(seen_tokens) > 0:
        lines.append({"tokens": get_words(seen_tokens, False)})
        raw_tokens.append(seen_tokens)
    # Extract phonological groups and rhythm per line
    for line in lines:
        syllables = get_syllables_word_end(line["tokens"])
        phonological_groups = get_phonological_groups(
            get_phonological_groups(syllables, liaison_type="sinaeresis")
        )
        line.update({
            "phonological_groups": phonological_groups,
            "rhythm": get_rhythmical_pattern(phonological_groups,
                                             rhythm_format,
                                             rhyme_analysis=rhyme_analysis)
        })
    if rhyme_analysis:
        analyzed_lines = analyze_rhyme(lines,
                                       always_return_rhyme=always_return_rhyme)
        if analyzed_lines is not None:
            for rhyme in [analyzed_lines]:
                for index, line in enumerate(lines):
                    line["structure"] = rhyme.get("name", "unknown")
                    line["rhyme"] = rhyme["rhyme"][index]
                    line["ending"] = rhyme["endings"][index]
                    line["ending_stress"] = rhyme["endings_stress"][index]
                    if line["ending_stress"] == 0:
                        line["rhyme_type"] = ""
                        line["rhyme_relaxation"] = None
                    else:
                        line["rhyme_type"] = rhyme["rhyme_type"]
                        line["rhyme_relaxation"] = rhyme["rhyme_relaxation"]
    lines_length = len(lines)
    structure_length = rhythmical_lengths if rhythmical_lengths else None
    for idx, line in enumerate(lines):
        if not structure_length:
            # Handle repeating stanzas
            line_structure = line.get("structure", None)
            structure_length, repeating_structure = STRUCTURES_LENGTH.get(
                line_structure, [[], False])
            if structure_length and repeating_structure:
                repetitions = int(lines_length / len(structure_length))
                structure_length = structure_length * repetitions
        if structure_length:
            structure_length_idx = structure_length[idx]
        elif lines_length > 1:
            structure_length_idx = get_structure_from_context(
                lines, idx, window=rhythmical_lengths_window
            )
        else:
            structure_length_idx = None
        if structure_length_idx is not None:
            if line["rhythm"]["length"] < structure_length_idx:
                candidates = generate_phonological_groups(raw_tokens[idx])
                for candidate in candidates:
                    rhythm = get_rhythmical_pattern(
                        candidate, rhythm_format,
                        rhyme_analysis=rhyme_analysis)
                    if rhythm["length"] == structure_length_idx:
                        line.update({
                            "phonological_groups": candidate,
                            "rhythm": rhythm,
                        })
                        break
    if not pos_output:
        remove_pos_from_output(lines)
    # scansion = remove_exact_length_matches(lines)
    scansion = lines
    if alternative_output\
            and split_stanzas_on is not None\
            and rhyme_analysis\
            and always_return_rhyme:
        scansion = transform_scansion(scansion, text)
    return scansion


def get_structure_from_context(lines, n, window=3):
    """Get the most frequent line length around line n using a window

    :param lines: List of dictionary lines of the poem
    :param n:  Integer with the reference position
    :param window: Integer with the size of the window around the reference
                   position. Defaults to 3
    :return: The most frequent line length
    """
    context = (
        lines[max(n - window, 0):n]
        + lines[n + 1:min(n + window + 1, len(lines))]
    )
    lengths = [line["rhythm"]["length"] for line in context]
    return Counter(lengths).most_common(1)[0][0]


def remove_pos_from_output(lines):
    """Remove `pos` tag from the output dictionary

    :param lines: List of dictionary lines of the poem
    :return: Dictionary with the key removed
    :rtype: dict
    """
    for line in lines:
        token_list = [token for token in line.get("tokens") if
                      line.get("tokens")]
        for token in token_list:
            if token.get("word"):
                token.pop("pos")
    return lines


def break_on_h(liaison_type, syllable_left, syllable_right):
    return (
            liaison_type == "synalepha"
            and syllable_right["syllable"][0].lower() == "h"
    )


def generate_phonological_groups(tokens):
    """Generates phonological groups from a list of tokens

    :param tokens: list of spaCy tokens
    :return: Generator with a list of phonological groups
    :rtype: generator
    """
    for alternative_syllabification in (True, False):
        words = get_words(tokens, alternative_syllabification)
        syllables = get_syllables_word_end(words)
        for liaison in (
                ("synalepha",),
                ("synalepha", "sinaeresis"),
                ("sinaeresis",),
                ("sinaeresis", "synalepha"),
        ):
            for ignore_synalepha_h in (break_on_h, None):
                for liaison_positions_1 in generate_liaison_positions(
                        syllables, liaison[0]
                ):
                    groups = get_phonological_groups(
                        syllables[:],
                        liaison_type=liaison[0],
                        liaison_positions=liaison_positions_1,
                        breakage_func=ignore_synalepha_h,
                    )
                    if len(liaison) == 1:
                        yield groups
                    else:
                        for liaison_positions_2 in generate_liaison_positions(
                                syllables, liaison[1]
                        ):
                            yield get_phonological_groups(
                                groups,
                                liaison_type=liaison[1],
                                liaison_positions=liaison_positions_2,
                                breakage_func=ignore_synalepha_h,
                            )


def generate_liaison_positions(syllables, liaison):
    """Generates all possible combinations for the liaisons on a list of syllables

    :param syllables: List of syllables with
    :param liaison: Type of liaison combination to be generated
    :return: Generator with a list of possible combinations
    :rtype: generator
    """
    positions = [int(syllable.get(f"has_{liaison}", 0))
                 for syllable in syllables]
    # Combinations start by applying all possible liaisons: [1, 1, ...]
    combinations = list(product([1, 0], repeat=sum(positions)))
    liaison_indices = [
        index for index, position in enumerate(positions) if position
    ]
    # Prioritize single liaisons
    non_single_liaisons = []
    for combination in combinations:
        liaison_positions = [0] * len(positions)
        for index, liaison_index in enumerate(liaison_indices):
            liaison_positions[liaison_index] = combination[index]
        if has_single_liaisons(liaison_positions):
            yield liaison_positions
        else:
            non_single_liaisons.append(liaison_positions)
    for liaison_position in non_single_liaisons:
        yield liaison_position


def has_single_liaisons(liaisons):
    """Checks whether liaisons (a list of 1's and 0's) has consecutive liaisons
        (1's) or not

    :param liaisons: List of possible liaisons to apply per phonological group
    :return: True if no consecutive liaisons, False otherwise
    :rtype: bool
    """
    return not any(i == j == 1 for i, j in zip(liaisons, liaisons[1:]))


def remove_exact_length_matches(lines):
    """Removes key "length_range" on lines with an exact length match
    :param lines: List of dictionary lines of the poem
    :return: Returns the lines list without  the "length_range" on lines with
    an exact length match
    """
    for line in lines.copy():
        if "length_range" in line["rhythm"]:
            ranges = line["rhythm"]["length_range"]
            if ranges["min_length"] == ranges["max_length"]:
                del line["rhythm"]["length_range"]
    return lines


def join_syllables(token):
    """Join all symbols and syllables from a list of tokens into a string."
    :param token: List of dictionaries representing tokens
    :return: String of syllables
    """
    if "symbol" in token:
        return token["symbol"]
    else:
        return "".join([syll["syllable"] for syll in token["word"]])


def transform_scansion(scansion, text):
    """Converts the old output to the new format
    :param scansion: Scansion dictionary
    :param text: Original text of the poem
    :return: New scansion dictionary
    """
    poem = copy.deepcopy(scheme)
    stanzas_list = []
    absolute_line_number = 1
    is_sonnet = scansion[0][0].get("structure") == "sonnet"
    stanzas_content_list = text.split('\n\n')
    line_content_list = []
    for stanza_text in stanzas_content_list:
        line_content_list.extend(stanza_text.splitlines())

    for st_idx, stanza in enumerate(scansion):
        line_list = []
        for line_idx, line in enumerate(stanza):
            new_line = copy.deepcopy(scheme["stanzaList"][0]["lineList"][0])
            tokens, _, rhythm, structure, rhyme, ending, ending_stress, \
                rhyme_type, rhyme_relaxation = [v for v in line.values()]
            print(rhythm)
            phonological_list = []
            for pg in line["phonological_groups"]:
                phonological_dict = copy.deepcopy(
                    scheme["stanzaList"][0]["lineList"][0][
                        "phonologicalGroups"][0])
                phonological_dict.update({
                    "content": pg["syllable"],
                    "isStressed": pg["is_stressed"],
                    "isWordEnd": pg.get("is_word_end", False),
                    "sinaeresisIndex": pg.get("sinaeresis_index"),
                    "synalephaIndex": pg.get("synalepha_index"),
                })
                phonological_list.append(phonological_dict)
            token_list = []
            word_number = 1
            for token in line["tokens"]:
                content = join_syllables(token)
                if "symbol" in token:
                    token = {"content": content,
                             "type": "symbol"}
                    token_list.append(token)
                else:
                    word_dict = copy.deepcopy(
                        scheme["stanzaList"][0]["lineList"][0]["tokenList"][0])
                    word_dict.update({
                        "content": content,
                        "type": "word",
                        "wordNumber": word_number
                    })
                    word_number += 1
                    syllable_list = []
                    for syl_idx, s in enumerate(token["word"]):
                        syllable_dict = copy.deepcopy(
                            scheme["stanzaList"][0]["lineList"][0]["tokenList"][
                                0]["syllableList"][0])
                        syllable_dict.update({
                            "content": s["syllable"],
                        })
                        syllable_dict.update({
                            "isStressed": s["is_stressed"],
                            "isWordEnd": s.get("is_word_end", False),
                            "hasSinaeresis": s.get("has_sinaeresis", False),
                            "hasSynalepha": s.get("has_synalepha", False),
                        })
                        for key, value in s.items():
                            if key != "syllable":
                                syllable_dict[key] = value
                        syllable_list.append(syllable_dict)
                    word_dict.update({"syllableList": syllable_list})
                    token_list.append(word_dict)
            line_pattern_dict = copy.deepcopy(
                scheme["stanzaList"][0]["lineList"][0]["linePattern"])
            line_pattern_dict.update({
                "lineMinLength": rhythm["length_range"]["min_length"],
                "lineMaxLength": rhythm["length_range"]["max_length"],
                "syllabicMetricalLength": rhythm["length"],
                "patterningMetricalScheme": rhythm["stress"],
                "employs": rhythm["type"],
                "scannedLine": " ".join([syl["content"].upper() if syl[
                    "isStressed"] else syl["content"].lower() for syl in
                                         phonological_list])
            })
            rhyme_dict = copy.deepcopy(
                scheme["stanzaList"][0]["lineList"][0]["rhyme"])
            rhyme_dict.update({
                "rhymeLabel": rhyme,
                "ending": ending,
                "rhymeGrapheme": ending,
                "typeOfRhymeMatching": rhyme_type,
                "endingStressedVowel": ending[ending_stress] if ending else None,
            })
            new_line.update({
                "relativeLineNumber": line_idx + 1,
                "absoluteLineNumber": absolute_line_number,
                "content": line_content_list[absolute_line_number - 1],
                "linePattern": line_pattern_dict,
                "rhyme": rhyme_dict,
                "phonologicalGroups": phonological_list,
                "tokenList": token_list
            })
            line_list.append(new_line)
            absolute_line_number += 1
        stanza_dict = copy.deepcopy(scheme["stanzaList"][0])
        stanza_pattern_dict = copy.deepcopy(
            scheme["stanzaList"][0]["stanzaPattern"])
        stanza_pattern_dict.update({
            "metricalType": structure,
            "rhymeScheme": "".join(
                [line["rhyme"]["rhymeLabel"] for line in line_list]),
        })
        stanza_dict.update({
            "stanzaPattern": stanza_pattern_dict,
            "stanzaNumber": st_idx + 1,
            "content": stanzas_content_list[st_idx],
            "lineList": line_list})
        stanzas_list.append(stanza_dict)
    poem.update({
        # "content": text,
        "stanzaList": stanzas_list})
    if is_sonnet:
        poem["structure"] = "sonnet"
        poem["stanzas_list"][0]["structure"] = "cuarteto"
        poem["stanzas_list"][1]["structure"] = "cuarteto"
        poem["stanzas_list"][2]["structure"] = "terceto"
        poem["stanzas_list"][3]["structure"] = "terceto"
    return poem
