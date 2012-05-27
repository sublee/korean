# -*- coding: utf-8 -*-
"""
    korean.inflection
    ~~~~~~~~~~~~~~~~~

    :copyright: (c) 2012 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

import sys
import types


class Inflection(object):

    _registry = {}

    @classmethod
    def define(cls, prefix_of=None, suffix_of=None):
        #from ..morpheme import Morpheme
        if not (prefix_of or suffix_of):
            raise TypeError('prefix_of or suffix_of should be defined')
        elif bool(prefix_of) == bool(suffix_of):
            raise TypeError('Cannot specify prefix_of and suffix_of both')
        #elif not isinstance(prefix_of or suffix_of, Morpheme):
        #    raise TypeError('Need a morpheme')
        frm = sys._getframe(1)
        def decorator(f):
            definition = dict(prefix_of=prefix_of, suffix_of=suffix_of, func=f)
            try:
                frm.f_locals['$inflections'].append(definition)
            except KeyError:
                frm.f_locals['$inflections'] = [definition]
            return f
        return decorator

    @classmethod
    def register(cls, target_cls, inflection_definitions):
        for definition in inflection_definitions:
            prefix_of = definition.get('prefix_of')
            suffix_of = definition.get('suffix_of')
            func = definition['func']
            key = (target_cls, prefix_of, suffix_of)
            if key in cls._registry:
                raise ValueError('Already defined inflection rule')
            cls._registry[key] = func

    @classmethod
    def inflect(cls, morpheme, prefix_of=None, suffix_of=None):
        prefix_type = prefix_of and type(prefix_of)
        suffix_type = suffix_of and type(suffix_of)
        func = cls._registry[(type(morpheme), prefix_type, suffix_type)]
        bound_func = types.MethodType(func, morpheme)
        return bound_func(prefix_of or suffix_of)


define = Inflection.define
register = Inflection.register
inflect = Inflection.inflect
