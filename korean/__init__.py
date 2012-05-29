# -*- coding: utf-8 -*-
"""
    korean
    ~~~~~~

    A library for Korean morphology.

    :copyright: (c) 2012 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

from . import data
from .inflection import define, register, inflect
from .l10n import KoreanTemplate, patch_translations
from .morphology import Morpheme, Noun, NumberWord, Particle, Substantive
