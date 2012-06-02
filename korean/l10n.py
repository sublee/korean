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

from .inflection import inflect
from .morphology import Noun, NumberWord, Particle


class Template(unicode):

    def format(self, *args, **kwargs):
        args = list(args)
        for seq, (key, val) in chain(product([args], enumerate(args)),
                                     product([kwargs], kwargs.items())):
            if isinstance(val, unicode):
                seq[key] = Noun(val)
            elif isinstance(val, int):
                seq[key] = NumberWord(val)
        return super(Template, self).format(*args, **kwargs)

    def __repr__(self):
        return '<%s %s>' % \
               (type(self).__name__, super(Template, self).__repr__)


def patch_gettext(translations):
    for meth in ['ugettext', 'ungettext']:
        def patched(orig, *args, **kwargs):
            return Template(orig(*args, **kwargs))
        patched.__name__ = meth
        orig = getattr(translations, meth)
        setattr(translations, meth, partial(patched, orig))
    return translations


def proofread(sentence):
    for particle in set(Particle._registry.itervalues()):
        for naive in particle.naive():
            while True:
                found = sentence.find(naive)
                if found < 0:
                    break
                noun = Noun(sentence[found - 1])
                inflected_particle = inflect(particle, suffix_of=noun)
                sentence = sentence[:found] + inflected_particle + \
                           sentence[found + len(naive):]
    return sentence
