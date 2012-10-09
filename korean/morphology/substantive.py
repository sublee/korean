# -*- coding: utf-8 -*-
"""
    korean.morphology.substantive
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2012 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import
import re

from .morpheme import Morpheme
from ..hangul import is_hangul


__all__ = ['Substantive', 'Noun', 'NumberWord', 'Loanword']


class Substantive(Morpheme):
    """A class for Korean substantive that is called "체언" in Korean."""

    def __format__(self, spec):
        """:class:`Substantive`'s custom formatter appends the correct particle
        after the substantive string using particle format spec such as
        ``{0:은}`` or ``{1:로}``:

            >>> format(Noun(u'엄마'), u'을')
            u'엄마를'
            >>> u'{0:은} {1:로}'.format(Noun(u'아들'), Noun(u'마을'))
            u'아들은 마을로'
            >>> u'{0:은} {1:로}'.format(Noun(u'아들'), Noun(u'산'))
            u'아들은 산으로'
        """
        from .particle import Particle
        from . import merge
        separated_spec = spec.split(':')
        if separated_spec[0] and is_hangul(separated_spec[0][0]):
            text = merge(self, Particle(separated_spec.pop(0)))
        else:
            text = unicode(self)
        try:
            spec = separated_spec[0]
        except IndexError:
            spec = ''
        return format(text, spec)


class Noun(Substantive):
    """A class for Korean noun that is called "명사" in Korean."""

    READING_PATTERN = re.compile(r'(?P<other>[^0-9]+)?(?P<number>[0-9]+)?')

    def read(self):
        """Reads a noun as Korean. The result will be Hangul.

            >>> Noun(u'레벨42').read()
            u'레벨사십이'
        """
        rv = []
        for match in self.READING_PATTERN.finditer(unicode(self)):
            if match.group('other'):
                rv.append(match.group('other'))
            if match.group('number'):
                rv.append(NumberWord(int(match.group('number'))).read())
        return ''.join(rv)


class NumberWord(Substantive):
    """A class for Korean number word that is called "수사" in Korean."""

    __numbers__ = {}
    __digits__ = {}

    def __init__(self, number):
        self.number = number

    def read(self):
        """Reads number as Korean.

            >>> NumberWord(1234567890).read()
            u'십이억삼천사백오십육만칠천팔백구십'
            >>> NumberWord.read_phases(0)
            u'영'
        """
        return ''.join(type(self).read_phases(self.number))

    @classmethod
    def read_phases(cls, number):
        """Reads number as Korean but seperates the result at each 10k.

            >>> NumberWord.read_phases(1234567890)
            (u'십이억', u'삼천사백오십육만', u'칠천팔백구십')
            >>> NumberWord.read_phases(0)
            (u'영',)
        """
        rv, phase = [], []
        digit = 0
        while True:
            single = number % 10
            if digit >= 4:
                try:
                    phase.append(cls.__digits__[digit])
                except KeyError:
                    pass
            if single:
                try:
                    phase.append(cls.__digits__[digit % 4])
                except KeyError:
                    pass
            number /= 10
            if not single and not number or \
               single == 1 and not digit or single > 1:
                phase.append(cls.__numbers__[single])
            if not number or digit % 4 == 3:
                if digit < 4 or len(phase) > 1:
                    rv.append(''.join(phase[::-1]))
                else:
                    rv.append(u'')
                phase = []
                if not number:
                    break
            digit += 1
        return tuple(rv[::-1])

    def basic(self):
        return unicode(self.number)

    def __format__(self, spec):
        try:
            return super(NumberWord, self).__format__(spec)
        except ValueError:
            return format(self.number, spec)


class Loanword(Substantive):
    """A class for loanword that is called "외래어" in Korean. This depends
    on `Hangulize <http://packages.python.org/hangulize>`_ which automatically
    transcribes a non-Korean word into Hangul.
    """

    def _import_hangulize(self):
        try:
            return self._hangulize
        except AttributeError:
            pass
        try:
            import hangulize
        except ImportError:
            raise ImportError('%s needs hangulize>=0.0.5' % type(self).__name__)
        self._hangulize = hangulize
        return hangulize

    def __init__(self, word, code=None, iso639=None, lang=None):
        hangulize = self._import_hangulize()
        self.lang = lang or hangulize.get_lang(code, iso639)
        super(Loanword, self).__init__(word)

    def read(self):
        """Transcribes into Hangul using `Hangulize
        <http://packages.python.org/hangulize>`_.

        >>> Loanword(u'Guido van Rossum', 'nld').read()
        u'히도 판로쉼'
        >>> Loanword(u'საქართველო', 'kat').read()
        u'사카르트벨로'
        >>> Loanword(u'Leonardo da Vinci', 'ita').read()
        u'레오나르도 다 빈치'
        """
        hangulize = self._import_hangulize()
        return hangulize.hangulize(self.basic(), lang=self.lang)
