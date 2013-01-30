# -*- coding: utf-8 -*-
"""
    korean.morphology
    ~~~~~~~~~~~~~~~~~

    :copyright: (c) 2012-2013 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import, unicode_literals
import sys
import types

from .. import hangul


__all__ = ['Morphology', 'Morpheme', 'Particle', 'Substantive', 'Noun',
           'NumberWord', 'Loanword', 'pick_allomorph', 'merge',
           'define_allomorph_picker']


class Morphology(object):

    _registry = {}

    @classmethod
    def _register_morpheme(cls, morpheme_cls):
        for attr in dir(morpheme_cls):
            if not attr.startswith('$'):
                continue
            for keyword, func in getattr(morpheme_cls, attr):
                keyword = (morpheme_cls,) + keyword
                if keyword in cls._registry:
                    raise ValueError('Already defined rule')
                try:
                    cls._registry[attr][keyword] = func
                except KeyError:
                    cls._registry[attr] = {keyword: func}

    @classmethod
    def _make_decorator(cls, tmp_attr, keyword):
        assert tmp_attr.startswith('$')
        frm = sys._getframe(2)
        def decorator(func):
            rule = (keyword, func)
            try:
                frm.f_locals[tmp_attr].append(rule)
            except KeyError:
                frm.f_locals[tmp_attr] = [rule]
            return func
        return decorator

    @classmethod
    def define_allomorph_picker(cls, prefix_of=None, suffix_of=None):
        if not (prefix_of or suffix_of):
            raise TypeError('prefix_of or suffix_of should be defined')
        elif bool(prefix_of) == bool(suffix_of):
            raise TypeError('Cannot specify prefix_of and suffix_of both')
        keyword = (prefix_of, suffix_of)
        return cls._make_decorator('$allomorph_pickers', keyword)

    @classmethod
    def pick_allomorph(cls, morpheme, prefix_of=None, suffix_of=None):
        prefix_type = prefix_of and type(prefix_of)
        suffix_type = suffix_of and type(suffix_of)
        keyword = (type(morpheme), prefix_type, suffix_type)
        func = cls._registry['$allomorph_pickers'][keyword]
        bound_func = types.MethodType(func, morpheme)
        return bound_func(prefix_of or suffix_of)

    @classmethod
    def merge(cls, prefix, suffix):
        try:
            prefix = cls.pick_allomorph(prefix, prefix_of=suffix)
        except KeyError:
            pass
        try:
            suffix = cls.pick_allomorph(suffix, suffix_of=prefix)
        except KeyError:
            pass
        if hangul.is_final(suffix[0]):
            prefix = prefix.read()
            splitted = hangul.split_char(prefix[-1])
            assert not splitted[2]
            mid = hangul.join_char((splitted[0], splitted[1], suffix[0]))
            return '{0}{1}{2}'.format(prefix[:-1], mid, suffix[1:])
        else:
            return '{0}{1}'.format(prefix, suffix)


pick_allomorph = Morphology.pick_allomorph
define_allomorph_picker = Morphology.define_allomorph_picker
merge = Morphology.merge


#: Imports submodules on the end. Because they might need :class:`Morphology`.
from .morpheme import Morpheme
from .particle import Particle
from .substantive import Substantive, Noun, NumberWord, Loanword
