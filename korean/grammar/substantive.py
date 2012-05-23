# -*- coding: utf-8 -*-
"""
    korean.grammar.substantive
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2012 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

from ..morpheme import Morpheme


class Substantive(Morpheme):

    def __format__(self, suffix):
        from ..grammar.particle import Particle
        try:
            particle = Particle.get(suffix)
            if self.has_final():
                suffix = particle.after_consonant
            else:
                suffix = particle.after_vowel
        except LookupError:
            pass
        return u'{0!s}{1}'.format(self, suffix)


class Noun(Substantive): pass
class Pronoun(Substantive): pass
class NumberWord(Substantive): pass
