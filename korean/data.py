# -*- coding: utf-8 -*-
"""
    korean.data
    ~~~~~~~~~~~

    :copyright: (c) 2012 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

from .grammar.particle import Particle


for args in [(u'은', u'는'), (u'이', u'가'), (u'을', u'를'), (u'에게'), \
             (u'도')]:
    particle = Particle(*args)
    Particle._registry[particle.after_consonant] = particle
    if particle.after_vowel:
        Particle._registry[particle.after_vowel] = particle
