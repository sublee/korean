# -*- coding: utf-8 -*-
"""
    korean.l10n
    ~~~~~~~~~~~

    Helpers for localization to Korean.

    :copyright: (c) 2012-2013 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import, unicode_literals
from itertools import chain, product
import re
import warnings

from ..morphology import Noun, NumberWord, Particle, pick_allomorph


__all__ = ['Proofreading', 'proofread', 'Template', 'patch_gettext']


class Proofreading(object):
    """A function-like class. These :meth:`__call__` replaces naive particles
    to be correct. First, it finds naive particles such as "을(를)" or
    "(으)로". Then it checks the forward character of the particle and replace
    with a correct particle.

    :param token_types: specific types to make as token.
    """

    def __init__(self, token_types):
        # TODO: support various token types
        pass

    def parse(self, text):
        """Tokenizes the given text with unicode text or :class:`Particle`.

        :param text: the string that has been written with naive particles.
        """
        tokens = []
        naive_particles = []
        particle_map = {}
        for particle in set(Particle._registry.itervalues()):
            for naive in particle.naive():
                particle_map[naive] = particle
                naive_particles.append(naive)
        particle_pattern = '(%s)' % '|'.join(map(re.escape, naive_particles))
        particle_pattern = re.compile(particle_pattern)
        prev_span = [0, 0]
        for match in particle_pattern.finditer(text):
            span = match.span()
            tokens.append(text[prev_span[1]:span[0]])
            tokens.append(particle_map[match.group(1)])
            prev_span = span
        try:
            tokens.append(text[span[1]:])
        except UnboundLocalError:
            tokens.append(text)
        return tuple(tokens)

    def __call__(self, text):
        """Do proofread. More information in :class:`Proofreading`.

        :param text: the string that has been written with naive particles.
        """
        buf = []
        for token in self.parse(text):
            if isinstance(token, Particle):
                noun = Noun(buf[-1])
                try:
                    token = pick_allomorph(token, suffix_of=noun)
                except:
                    token = token.naive()[0]
            buf.append(token)
        return ''.join(buf)


#: Default :class:`Proofreading` object. It tokenizes ``unicode`` and
#: :class:`korean.Particle`. Use it like a function.
proofread = Proofreading([unicode, Particle])


class Template(unicode):
    """The :class:`Template` object extends :class:`unicode` and overrides
    :meth:`format` method. This can format particle format spec without
    evincive :class:`Noun` or :class:`NumberWord` arguments.

    Basically this example:

        >>> import korean
        >>> korean.l10n.Template('{0:을} 좋아합니다.').format('향수')
        '향수를 좋아합니다.'

    Is equivalent to the following:

        >>> import korean
        >>> '{0:을 좋아합니다.}'.format(korean.Noun('향수'))
        '향수를 좋아합니다.'
    """

    def format(self, *args, **kwargs):
        args = list(args)
        for seq, (key, val) in chain(product([args], enumerate(args)),
                                     product([kwargs], kwargs.items())):
            if isinstance(val, unicode):
                seq[key] = Noun(val)
            elif isinstance(val, (long, int)):
                seq[key] = NumberWord(int(val))
        return super(Template, self).format(*args, **kwargs)

    def __repr__(self):
        return '<%s %s>' % \
               (type(self).__name__, super(Template, self).__repr__())


def patch_gettext(translations):
    from ..ext.gettext import patch_gettext as original_patch_gettext
    warnings.warn('\'korean.l10n.patch_gettext\' is now called '
                  '\'korean.ext.gettext.patch_gettext\'', DeprecationWarning)
    return original_patch_gettext(translations)
