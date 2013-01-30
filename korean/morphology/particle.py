# -*- coding: utf-8 -*-
"""
    korean.morphology.particle
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2012-2013 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import, unicode_literals

from . import define_allomorph_picker
from .morpheme import Morpheme
from .substantive import Noun, NumberWord, Loanword
from .. import hangul


__all__ = ['Particle']


class Particle(Morpheme):
    """Particle (조사) is a postposition in Korean. Some particles have
    different allomorphs such as 을/를, 이/가. These forms follow forward
    syllable ends what phoneme; a vowel, a consonant, or a Rieul (ㄹ).
    """

    def __init__(self, after_vowel, after_consonant=None, after_rieul=None):
        if after_rieul:
            forms = (after_vowel, after_consonant, after_rieul)
        elif after_consonant:
            forms = (after_vowel, after_consonant)
        else:
            forms = (after_vowel,)
        super(Particle, self).__init__(*forms)

    @classmethod
    def get(cls, key):
        try:
            return super(Particle, cls).get(key)
        except KeyError:
            return cls.guess(key)

    @classmethod
    def guess(cls, key):
        length_of_first = lambda x: len(x[0])
        for other_key, particle in sorted(cls._registry.items(),
                                          key=length_of_first):
            if key.startswith(other_key):
                suffix = key[len(other_key):]
                return cls(*(form + suffix for form in particle.forms))
        raise KeyError('There is no guessable particle')

    @property
    def after_vowel(self):
        return self.basic()

    @property
    def after_consonant(self):
        try:
            return self.forms[1]
        except IndexError:
            return self.basic()

    @property
    def after_rieul(self):
        try:
            return self.forms[2]
        except IndexError:
            return self.basic()

    def naive(self):
        rv = []
        seen = set()
        unique_forms = [form for form in self.forms
                        if form not in seen and seen.add(form) is None]
        for forms in zip(unique_forms[:-1], unique_forms[1:]):
            length = map(len, forms)
            if len(set(length)) == 1:
                # such as "를(을)", "을(를)", "(를)을", "(을)를"
                rv.append('{0}({1})'.format(*forms))
                rv.append('{1}({0})'.format(*forms))
                rv.append('({0}){1}'.format(*forms))
                rv.append('({1}){0}'.format(*forms))
            else:
                # such as "(으)로"
                x = int(length[0] > length[1])
                args = forms[1 - x].rstrip(forms[x]), forms[x]
                rv.append('({0}){1}'.format(*args))
        return tuple(rv)

    def pick_allomorph_after_char(self, char):
        final = hangul.get_final(char)
        if not final:
            return self.after_vowel
        elif final == 'ㄹ':
            return self.after_rieul
        else:
            return self.after_consonant

    @define_allomorph_picker(suffix_of=Noun)
    @define_allomorph_picker(suffix_of=NumberWord)
    @define_allomorph_picker(suffix_of=Loanword)
    def pick_allomorph_after_substantive(self, substantive):
        return self.pick_allomorph_after_char(substantive.read()[-1])
