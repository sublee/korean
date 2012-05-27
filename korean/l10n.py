# -*- coding: utf-8 -*-
"""
    korean.l10n
    ~~~~~~~~~~~

    Helpers for localization to Korean.

    :copyright: (c) 2012 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

from itertools import chain, product

from .morphology import Noun


class Localization(object):

    def __init__(self, get_locale=lambda: 'ko_KR'):
        self.get_locale = get_locale

    def maybe_korean(self, template):
        if self.get_locale().startswith('ko'):
            return KoreanTemplate(template)
        return template


class KoreanTemplate(object):

    def __init__(self, template):
        self.template = template

    def format(self, *args, **kwargs):
        args = list(args)
        for seq, (key, val) in chain(product([args], enumerate(args)),
                                     product([kwargs], kwargs.items())):
            if isinstance(val, unicode):
                seq[key] = Noun(val)
        return self.template.format(*args, **kwargs)
