# -*- coding: utf-8 -*-
"""
    korean.morphology.morpheme
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2012-2013 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import, unicode_literals
import sys

from ..hangul import get_final, is_hangul


__all__ = ['Morpheme']


class MorphemeMetaclass(type):

    def __new__(meta, name, bases, attrs):
        from . import Morphology
        cls = type.__new__(meta, name, bases, attrs)
        cls._registry = {}
        Morphology._register_morpheme(cls)
        return cls

    def __call__(cls, *forms):
        if len(forms) == 1:
            try:
                return cls.get(forms[0])
            except KeyError:
                pass
        return super(MorphemeMetaclass, cls).__call__(*forms)


class Morpheme(object):
    """This class presents a morpheme (형태소) or allomorph (이형태). It
    can have one or more forms. The first form means the basic allomorph
    (기본형).

    :param forms: each forms of allomorph. the first form will be basic
                  allomorph.
    """

    __metaclass__ = MorphemeMetaclass

    _registry = None

    def __init__(self, *forms):
        assert all([isinstance(form, unicode) for form in forms])
        self.forms = forms

    @classmethod
    def get(cls, key):
        """Returns a pre-defined morpheme object by the given key."""
        return cls._registry[key]

    @classmethod
    def register(cls, key, obj):
        """Registers a pre-defined morpheme object to the given key."""
        cls._registry[key] = obj

    def read(self):
        """Every morpheme class would implement this method. They should make a
        morpheme to the valid Korean text with Hangul.
        """
        return unicode(self)

    def basic(self):
        """The basic form of allomorph."""
        return self.forms[0]

    def __unicode__(self):
        return self.basic()

    def __str__(self):
        return unicode(self).encode('utf-8')

    if sys.version_info >= (3,):
        __str__ = __unicode__
        del __unicode__

    def __getitem__(self, i):
        return unicode(self)[i]

    def __getslice__(self, start, stop, step=None):
        return unicode(self)[start:stop:step]

    def __format__(self, suffix):
        return '{0!s}{1}'.format(self, suffix)

    def __repr__(self):
        return '{0}({1!s})'.format(type(self).__name__, unicode(self))
