# -*- coding: utf-8 -*-
"""
    korean.morphology.morpheme
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2012 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

from ..hangul import get_final, is_hangul


class Morpheme(object):

    def __init__(self, text):
        assert isinstance(text, unicode)
        self.text = text

    def __unicode__(self):
        return self.text

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __getitem__(self, i):
        return unicode(self)[i]

    def __getslice__(self, start, stop, step=None):
        return unicode(self)[start:stop:step]

    def has_final(self):
        char = self[-1]
        if is_hangul(char):
            return bool(get_final(char))
        else:
            return char in 'bcdfgjklmnpqrtx'

    def __format__(self, suffix):
        return u'{0!s}{1}'.format(self, suffix)

    def __repr__(self):
        return '{0}:{1}'.format(type(self).__name__, str(self))
