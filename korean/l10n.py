# -*- coding: utf-8 -*-
"""
    korean.l10n
    ~~~~~~~~~~~

    Helpers for localization to Korean.

    :copyright: (c) 2012 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

from functools import partial
from itertools import chain, product

from .morphology import Noun, NumberWord


class Template(object):

    def __init__(self, template):
        self.template = template

    def format(self, *args, **kwargs):
        args = list(args)
        for seq, (key, val) in chain(product([args], enumerate(args)),
                                     product([kwargs], kwargs.items())):
            if isinstance(val, unicode):
                seq[key] = Noun(val)
            elif isinstance(val, int):
                seq[key] = NumberWord(val)
        return self.template.format(*args, **kwargs)

    def __repr__(self):
        return '<%s %r>' % (type(self).__name__, self.template)


def patch(translations):
    for meth in ['ugettext', 'ungettext']:
        def patched(orig, *args, **kwargs):
            return Template(orig(*args, **kwargs))
        patched.__name__ = meth
        orig = getattr(translations, meth)
        setattr(translations, meth, partial(patched, orig))
    return translations
