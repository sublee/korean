# -*- coding: utf-8 -*-
"""
    korean
    ~~~~~~

    A library for Korean morphology.

    :copyright: (c) 2012 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

from . import hangul, l10n, morphology
from .morphology import Morpheme, Noun, NumberWord, Loanword, Particle, \
                        Substantive


__copyright__ = 'Copyright 2012 by Heungsub Lee'
__version__ = '0.1.4'
__license__ = 'BSD'
__author__ = 'Heungsub Lee'
__author_email__ = 'h''@''subl.ee'
__url__ = 'http://packages.python.org/korean'
__all__ = ['hangul', 'l10n', 'morphology', 'Morpheme', 'Noun', 'NumberWord',
           'Loanword', 'Particle', 'Substantive']


def load_data():
    import json
    import os
    with open(os.path.join(os.path.dirname(__file__), 'data.json')) as f:
        data = json.load(f)
    # register allomorphic particles
    for forms in data['allomorphic_particles'].itervalues():
        particle = Particle(*forms)
        for form in forms:
            Particle.register(form, particle)
    # register numbers and digits
    for number, form in data['numbers'].iteritems():
        NumberWord.__numbers__[int(number)] = form
    for digit, form in data['digits'].iteritems():
        NumberWord.__digits__[int(digit)] = form


load_data()
