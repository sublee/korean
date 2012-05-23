# -*- coding: utf-8 -*-
"""
    korean.hangul
    ~~~~~~~~~~~~~

    Based on "hangul.py" of Hye-Shik Chang.

    :copyright: (c) 2012 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""


def S(*sequences):
    def to_tuple(sequence):
        if not sequence:
            return (sequence,)
        return tuple(sequence)
    return sum(map(to_tuple, sequences), ())


VOWELS = S(u'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ')
CONSONANTS = S(u'ㄱㄲㄳㄴㄵㄶㄷㄸㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅃㅄㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ')
INITIALS = S(u'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ')
FINALS = S(u'', u'ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ')
LETTER_ELEMENTS = (INITIALS, VOWELS, FINALS)
HANGUL_RANGE = xrange(ord(u'가'), ord(u'힣') + 1)
FIRST_HANGUL = HANGUL_RANGE[0]


def char_offset(char):
    if isinstance(char, int):
        offset = char
    else:
        assert len(char) == 1
        assert is_hangul(char)
        offset = ord(char) - FIRST_HANGUL
    assert offset < len(HANGUL_RANGE)
    return offset


def is_hangul(char):
    return ord(char) in HANGUL_RANGE


def is_vowel(char):
    return char in VOWELS


def is_consonant(char):
    return char in CONSONANTS


def is_initial(char):
    return char in INITIALS


def is_final(char):
    return char in FINALS


def get_initial(char):
    if is_initial(char):
        return char
    return INITIALS[int(char_offset(char) / (len(VOWELS) * len(FINALS)))]


def get_vowel(char):
    if is_vowel(char):
        return char
    return VOWELS[int(char_offset(char) / len(FINALS)) % len(VOWELS)]


def get_final(char):
    if is_final(char):
        return char
    return FINALS[char_offset(char) % len(FINALS)]


def split_char(char):
    code = char_offset(char)
    return (get_initial(code), get_vowel(code), get_final(code))


def join_char(splitted):
    assert len(splitted) == len(LETTER_ELEMENTS)
    if not (splitted[0] and splitted[1]):
        return splitted[0] or splitted[1]
    indexes = [tuple.index(*args) for args in zip(LETTER_ELEMENTS, splitted)]
    offset = (indexes[0] * len(VOWELS) + indexes[1]) * len(FINALS) + indexes[2]
    return unichr(FIRST_HANGUL + offset)
