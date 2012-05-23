# -*- coding: utf-8 -*-
"""
    korean
    ~~~~~~

    Processing Korean language.

    :copyright: (c) 2012 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

from . import Morpheme


class Word(Morpheme):

    def __format__(self, format_spec):
        from ..grammar.particle import Particle
        try:
            particle = Particle.get(format_spec)
            if self.has_final():
                particle = particle.after_consonant
            else:
                particle = particle.after_vowel
            return u'{0!s}{1}'.format(self, particle)
        except KeyError:
            return super(Word, self).__format__(format_spec)
