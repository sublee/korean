# -*- coding: utf-8 -*-
"""
    korean.morphology.substantive
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2012 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

from .morpheme import Morpheme


class Substantive(Morpheme):

    pass


class Noun(Substantive):

    def __format__(self, suffix):
        from .particle import Particle
        from ..inflection import inflect
        try:
            particle = Particle(suffix)
            suffix = inflect(particle, suffix_of=self)
        except LookupError:
            pass
        return u'{0!s}{1}'.format(self, suffix)


class NumberWord(Substantive):

    '''
    NATIVE_DIGITS = [u'영', u'한', u'두', u'세', u'네', u'다섯', u'여섯', \
                     u'일곱', u'여덟', u'아홉'[
    NATIVE_TENS = [u'열', u'스무', u'서른', u'마흔', u'쉰', u'예순', u'일흔', \
                   u'여든', u'아흔']
    HANJA_DIGITS = u'영일이삼사오육칠팔구'

    MINOR_SCALES = u'십백천'
    MAJOR_SCALES = u'만억조경해'

    def __init__(self, number):
        self.number = number
        super(NumberWord, self).__init__(u''.join(self.hanja()))

    def hanja(self):
        """Converts the number to Hanja text."""
        phases, scale, scale_len = [], 0, len(self.MINOR_SCALES) + 1
        number = self.number
        while number:
            n = number % 10
            if scale % scale_len == 0:
                phase = []
                phases.append(phase)
                if scale:
                    phase.append(self.MAJOR_SCALES[(scale - 1) / scale_len])
            elif n:
                phase.append(self.MINOR_SCALES[scale % scale_len - 1])
            if n and (n != 1 or not scale):
                phase.append(self.HANJA_DIGITS[n])
            number /= 10
            scale += 1
        return [''.join(phase[::-1]) for phase in phases[::-1]]

    def native(self):
        phases = self.hanja()[:-1]
        number = self.number % 100
        while number:
            n = number % 10

    def __format__(self, suffix):
        if not suffix:
            return unicode(self.number)
        else:
            return super(NumberWord, self).__format__(suffix)
    '''
