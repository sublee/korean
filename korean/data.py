# -*- coding: utf-8 -*-
"""
    korean.data
    ~~~~~~~~~~~

    :copyright: (c) 2012 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

from .grammar.particle import Particle


for args in [(u'과', u'와'), (u'은', u'는'), (u'을', u'를'), (u'이', u'가')]:
    particle = Particle(*args)
    Particle.register(particle.after_consonant, particle)
    if particle.after_vowel:
        Particle.register(particle.after_vowel, particle)
