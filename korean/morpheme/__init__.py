# -*- coding: utf-8 -*-
"""
    korean.morpheme
    ~~~~~~~~~~~~~~~

    :copyright: (c) 2012 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

from ..hangul import final, is_hangul


class Morpheme(unicode):

    def has_final(self):
        char = self[-1]
        if is_hangul(char):
            return bool(final(char))
        else:
            return char in 'bcdfgjklmnpqrtx'
