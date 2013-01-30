# -*- coding: utf-8 -*-
"""
    korean.hangul
    ~~~~~~~~~~~~~

    Processing a string written by Hangul. All code of here is based on
    `hangul.py
    <https://raw.github.com/sublee/hangulize/master/hangulize/hangul.py>`_ by
    `Hye-Shik Chang <http://openlook.org/>`_ at 2003.

    :copyright: (c) 2012-2013 by Heungsub Lee and 2003 by Hye-Shik Chang
    :license: BSD, see LICENSE for more details.
"""
from __future__ import unicode_literals


__all__ = ['char_offset', 'is_hangul', 'is_vowel', 'is_consonant',
           'is_initial', 'is_final', 'get_initial', 'get_vowel', 'get_final',
           'split_char', 'join_char']


def S(*sequences):
    def to_tuple(sequence):
        if not sequence:
            return (sequence,)
        return tuple(sequence)
    return sum(map(to_tuple, sequences), ())
VOWELS = S('ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ')
CONSONANTS = S('ㄱㄲㄳㄴㄵㄶㄷㄸㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅃㅄㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ')
INITIALS = S('ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ')
FINALS = S('', 'ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ')
LETTER_ELEMENTS = (INITIALS, VOWELS, FINALS)
HANGUL_RANGE = xrange(ord('가'), ord('힣') + 1)
FIRST_HANGUL = HANGUL_RANGE[0]
del S


def char_offset(char):
    """Returns Hangul character offset from "가"."""
    if isinstance(char, int):
        offset = char
    else:
        assert len(char) == 1
        assert is_hangul(char)
        offset = ord(char) - FIRST_HANGUL
    assert offset < len(HANGUL_RANGE)
    return offset


def is_hangul(char):
    """Checks if the given character is written in Hangul."""
    return ord(char) in HANGUL_RANGE


def is_vowel(char):
    """Checks if the given character is a vowel of Hangul."""
    return char in VOWELS


def is_consonant(char):
    """Checks if the given character is a consonant of Hangul."""
    return char in CONSONANTS


def is_initial(char):
    """Checks if the given character is an initial consonant of Hangul."""
    return char in INITIALS


def is_final(char):
    """Checks if the given character is a final consonant of Hangul. The final
    consonants contain what a joined multiple consonant and empty character.
    """
    return char in FINALS


def get_initial(char):
    """Returns an initial consonant from the given character."""
    if is_initial(char):
        return char
    return INITIALS[int(char_offset(char) / (len(VOWELS) * len(FINALS)))]


def get_vowel(char):
    """Returns a vowel from the given character."""
    if is_vowel(char):
        return char
    return VOWELS[int(char_offset(char) / len(FINALS)) % len(VOWELS)]


def get_final(char):
    """Returns a final consonant from the given character."""
    if is_final(char):
        return char
    return FINALS[char_offset(char) % len(FINALS)]


def split_char(char):
    """Splits the given character to a tuple where the first item is the
    initial consonant and the second the vowel and the third the final.
    """
    code = char_offset(char)
    return (get_initial(code), get_vowel(code), get_final(code))


def join_char(splitted):
    """Joins a tuple in the form ``(initial, vowel, final)`` to a Hangul
    character.
    """
    assert len(splitted) == len(LETTER_ELEMENTS)
    if not (splitted[0] and splitted[1]):
        return splitted[0] or splitted[1]
    indexes = [tuple.index(*args) for args in zip(LETTER_ELEMENTS, splitted)]
    offset = (indexes[0] * len(VOWELS) + indexes[1]) * len(FINALS) + indexes[2]
    return unichr(FIRST_HANGUL + offset)
