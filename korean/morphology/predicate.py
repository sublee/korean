# -*- coding: utf-8 -*-
"""
    korean.morphology.predicate
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2012 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

from .morpheme import Morpheme
from ..hangul import get_final, join_char, split_char, is_final
from ..helpers import Registry


ENDING = u'다'


class Predicate(Morpheme):

    def __init__(self, origin):
        assert origin.endswith(ENDING)
        assert len(origin) > len(ENDING)
        self.source = origin[:-len(ENDING)]
        super(Predicate, self).__init__(origin)

    def __format__(self, suffix):
        glue = self.source[-1]
        final = get_final(glue)
        if is_final(suffix[0]):
            splitted = split_char(glue)
            if glue == u'는':
                if suffix[0] == u'ㅆ':
                    glue = u'었'
                else:
                    glue = u'습'
            elif final in (u'', u'ㄴ', u'ㄹ'):
                if suffix[0] == u'ㅆ' and final != u'ㄴ':
                    if splitted[1] in u'ㅣ':
                        glue = join_char((splitted[0], u'ㅕ', suffix[0]))
                    elif splitted[1] in u'ㅏㅑㅗㅛ':
                        glue = join_char((splitted[0], u'ㅕ', suffix[0]))
                        glue += u'았'
                    else:
                        glue += u'었'
                else:
                    glue = join_char((splitted[0], splitted[1], suffix[0]))
            else:
                if suffix[0] == u'ㅂ':
                    glue += u'습'
                elif suffix[0] == u'ㄴ':
                    glue += u'는'
                elif suffix[0] == u'ㅆ':
                    glue += u'었'
            suffix = suffix[1:]
        return u''.join([self.source[:-1], glue, suffix])


class Verb(Predicate): pass
class Adjective(Predicate): pass
