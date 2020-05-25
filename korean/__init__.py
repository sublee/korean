# -*- coding: utf-8 -*-
"""
    korean
    ~~~~~~

    A library for Korean morphology.

    :copyright: (c) 2012-2013 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import, unicode_literals
import codecs
import sys

import six

from . import hangul, l10n, morphology
from .morphology import (Morpheme, Noun, NumberWord, Loanword, Particle,
                         Substantive)


__version__ = '0.1.9'
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
    path = os.path.join(os.path.dirname(__file__), 'data.json')
    with codecs.open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # register allomorphic particles
    for forms in six.itervalues(data['allomorphic_particles']):
        particle = Particle(*forms)
        for form in forms:
            Particle.register(form, particle)
    # register numbers and digits
    for number, form in six.iteritems(data['numbers']):
        NumberWord.__numbers__[int(number)] = form
    for digit, form in six.iteritems(data['digits']):
        NumberWord.__digits__[int(digit)] = form
    for operation, form in six.iteritems(data['unary_operations']):
        NumberWord.__unary_operations__[operation] = form


_load_data()
