# -*- coding: utf-8 -*-
"""
    korean.morphology.morpheme
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2012 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

from ..hangul import get_final, is_hangul


class MorphemeMetaclass(type):

    def __new__(meta, name, bases, attrs):
        from .. import inflection
        try:
            inflection_definitions = attrs.pop('$inflections')
        except KeyError:
            pass
        cls = type.__new__(meta, name, bases, attrs)
        cls._registry = {}
        try:
            inflection.register(cls, inflection_definitions)
        except UnboundLocalError:
            pass
        return cls

    def __call__(cls, *forms):
        try:
            if len(forms) == 1:
                key = forms[0]
                return cls._registry[key]
        except KeyError:
            pass
        return super(MorphemeMetaclass, cls).__call__(*forms)

    def register(cls, key, obj):
        cls._registry[key] = obj


class Morpheme(object):

    __metaclass__ = MorphemeMetaclass

    def __init__(self, *forms):
        assert all([isinstance(form, unicode) for form in forms])
        self.forms = forms

    def basic(self):
        return self.forms[0]

    def __unicode__(self):
        return self.basic()

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
