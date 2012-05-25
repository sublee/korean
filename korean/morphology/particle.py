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

    def after_vowel(self):
        return self.forms[0]

    def after_consonant(self):
        return self.forms[1]

    def after_rieul(self):
        return self.forms[2]
