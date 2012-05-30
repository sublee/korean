# -*- coding: utf-8 -*-
"""
    korean.morphology.substantive
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2012 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

from .morpheme import Morpheme
from ..hangul import is_hangul


class Substantive(Morpheme):
    """A class for Korean substantive ("체언")."""

    pass


class Noun(Substantive):
    """A class for Korean noun ("명사")."""

    def __format__(self, spec):
        """This custom formatter can choose the correct particle:

            >>> format(Noun(u'엄마'), u'을')
            엄마를
            >>> u'{0:은} {1:로}'.format(Noun(u'아들'), Noun(u'마을'))
            아들은 마을로
            >>> u'{0:은} {1:로}'.format(Noun(u'아들'), Noun(u'산'))
            아들은 산으로
        """
        from .particle import Particle
        from ..inflection import inflect
        separated_spec = spec.split(':')
        if is_hangul(separated_spec[0][0]):
            particle = Particle(separated_spec.pop(0))
            suffix = inflect(particle, suffix_of=self)
            text = u'{0!s}{1}'.format(self, suffix)
        else:
            text = unicode(self)
        try:
            spec = separated_spec[0]
        except IndexError:
            spec = ''
        return format(text, spec)
