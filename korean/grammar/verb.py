# -*- coding: utf-8 -*-
"""
    korean.grammar.verb
    ~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2012 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

from ..morpheme import Morpheme


class Verb(Morpheme):

    def __init__(self, origin):
        assert origin.endswith(u'다')
        self.origin = origin
