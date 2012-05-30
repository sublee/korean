# -*- coding: utf-8 -*-
"""
    korean.morphology.particle
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2012 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

from .morpheme import Morpheme
from .substantive import Noun
from .. import hangul, inflection


class Particle(Morpheme):

    @classmethod
    def get(cls, key):
        try:
            return super(Particle, cls).get(key)
        except KeyError:
            return cls.guess(key)

    @classmethod
    def guess(cls, key):
        for other_key, particle in cls._registry.iteritems():
            if key.startswith(other_key):
                suffix = key[len(other_key):]
                return cls(*(form + suffix for form in particle.forms))
        raise KeyError('There is no guessable particle')

    @property
    def after_vowel(self):
        return self.basic()

    @property
    def after_consonant(self):
        try:
            return self.forms[1]
        except IndexError:
            return self.basic()

    @property
    def after_rieul(self):
        try:
            return self.forms[2]
        except IndexError:
            return self.basic()

    @inflection.define(suffix_of=Noun)
    def inflect_after_noun(self, noun):
        final_of_noun = hangul.get_final(noun[-1])
        if not final_of_noun:
            return self.after_vowel
        elif final_of_noun == u'ㄹ':
            return self.after_rieul
        else:
            return self.after_consonant
