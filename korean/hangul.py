# -*- coding: utf-8 -*-
"""
    korean.hangul
    ~~~~~~~~~~~~~

    :copyright: (c) 2012 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""


HANGUL_RANGE = xrange(0xac00, 0xd7a3 + 1)


def initial(char):
    i = (ord(char) - HANGUL_RANGE[0]) / (21 * 28)
    if i:
        return unichr(i)


def vowel(char):
    i = ((ord(char) - HANGUL_RANGE[0]) % (21 * 28)) / 28
    if i:
        return unichr(i)


def final(char):
    i = (ord(char) - HANGUL_RANGE[0]) % 28
    if i:
        return unichr(i)


def is_hangul(char):
    return ord(char) in HANGUL_RANGE
