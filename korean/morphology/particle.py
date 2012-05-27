# -*- coding: utf-8 -*-
"""
    korean.morphology.particle
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2012 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

from .morpheme import Morpheme
from .substantive import Noun
from .. import hangul, inflection


class Particle(Morpheme):

    @property
    def after_vowel(self):
        return self.forms[0]

    @property
    def after_consonant(self):
        return self.forms[1]

    @property
    def after_rieul(self):
        return self.forms[2]

    @inflection.define(suffix_of=Noun)
    def inflect_after_noun(self, noun):
        final_of_noun = hangul.get_final(noun[-1])
        if not final_of_noun:
            return self.after_vowel
        elif final_of_noun == u'ㄹ':
            return self.after_rieul
        else:
            return self.after_consonant
