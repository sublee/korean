# -*- coding: utf-8 -*-
"""
    korean.grammar.particle
    ~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2012 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

from ..morpheme.word import Word


class Particle(Word):

    _registry = {}

    @classmethod
    def get(cls, key):
        return cls._registry[key]

    def __new__(cls, *args, **kwargs):
        return unicode.__new__(cls)

    def __init__(self, after_consonant, after_vowel=None):
        self.after_consonant = after_consonant
        self.after_vowel = after_vowel

    def __repr__(self):
        if self.after_vowel:
            rv = u'{}({})'.format(self.after_consonant, self.after_vowel)
        else:
            rv = self.after_consonant
        return rv.encode('utf-8')
