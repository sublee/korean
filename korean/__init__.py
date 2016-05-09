# -*- coding: utf-8 -*-
"""
    korean
    ~~~~~~

    A library for Korean morphology.

    :copyright: (c) 2012-2013 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import, unicode_literals
import sys

from . import hangul, l10n, morphology
from .morphology import (Morpheme, Noun, NumberWord, Loanword, Particle,
                         Substantive)


__version__ = '0.1.8'
__all__ = ['hangul', 'l10n', 'morphology', 'Morpheme', 'Noun', 'NumberWord',
           'Loanword', 'Particle', 'Substantive']


# Python 2's import seems to do not work with unicode __all__.
# __future__.unicode_literals could make a TypeError with "from __ import *".
if sys.version_info < (3,):
    for mod in [globals(), hangul, l10n, morphology]:
        if isinstance(mod, dict):
            mod['__all__'] = map(str, mod['__all__'])
        else:
            mod.__all__ = map(str, mod.__all__)


def _load_data():
    """Loads allomorphic particles and number words from :file:`data.json`."""
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
    for operation, form in data['unary_operations'].iteritems():
        NumberWord.__unary_operations__[operation] = form


_load_data()
