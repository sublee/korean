# -*- coding: utf-8 -*-
"""
    korean.morphology.particle
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2012 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

from .morpheme import Morpheme
from ..helpers import Registry


class Particle(Morpheme, Registry):

    def __new__(cls,  after_consonant, after_vowel=None):
        return unicode.__new__(cls, after_consonant)

    def __init__(self, after_consonant, after_vowel=None):
        self.after_consonant = after_consonant
        self.after_vowel = after_vowel

    def __str__(self):
        if self.after_vowel:
            rv = u'{}({})'.format(self.after_consonant, self.after_vowel)
        else:
            rv = self.after_consonant
        return rv.encode('utf-8')
