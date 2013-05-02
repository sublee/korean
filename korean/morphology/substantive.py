# -*- coding: utf-8 -*-
"""
    korean.morphology.substantive
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2012-2013 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import, unicode_literals
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

            >>> format(Noun('엄마'), '을')
            '엄마를'
            >>> '{0:은} {1:로}'.format(Noun('아들'), Noun('마을'))
            '아들은 마을로'
            >>> '{0:은} {1:로}'.format(Noun('아들'), Noun('산'))
            '아들은 산으로'
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

            >>> Noun('레벨42').read()
            '레벨사십이'
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
    __unary_operations__ = {}

    def __init__(self, number):
        self.number = number

    def read(self):
        """Reads number as Korean.

            >>> NumberWord(1234567890).read()
            '십이억삼천사백오십육만칠천팔백구십'
            >>> NumberWord.read(0)
            '영'
        """
        return ''.join(type(self).read_phases(self.number))

    @classmethod
    def read_phases(cls, number):
        """Reads number as Korean but seperates the result at each 10k.

            >>> NumberWord.read_phases(1234567890)
            ('십이억', '삼천사백오십육만', '칠천팔백구십')
            >>> NumberWord.read_phases(0)
            ('영',)
        """
        rv, phase = [], []
        digit = 0
        negative = number < 0
        number = abs(number)
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
            number //= 10
            if (single or number) and (single != 1 or digit) and (single <= 1):
                pass
            else:
                phase.append(cls.__numbers__[single])
            if not number or digit % 4 == 3:
                if digit < 4 or len(phase) > 1:
                    rv.append(''.join(phase[::-1]))
                else:
                    rv.append('')
                phase = []
                if not number:
                    break
            digit += 1
        if negative:
            rv.append(cls.__unary_operations__['-'])
        return tuple(rv[::-1])

    def basic(self):
        return unicode(self.number)

    def __format__(self, spec):
        if ':' in spec:
            number_spec, spec = spec.split(':', 1)
            formatted_number = format(self.number, number_spec)
        else:
            formatted_number = None
        try:
            rv = super(NumberWord, self).__format__(spec)
        except ValueError:
            return format(self.number, spec)
        if formatted_number is not None:
            rv = formatted_number + rv[len(str(self.number)):]
        return rv


class Loanword(Substantive):
    """A class for loanword that is called "외래어" in Korean. This depends
    on `Hangulize <http://packages.python.org/hangulize>`_ which automatically
    transcribes a non-Korean word into Hangul.

    .. versionadded:: 0.1.4
    """

    def _import_hangulize(self):
        try:
            return self._hangulize
        except AttributeError:
            pass
        try:
            import hangulize
        except ImportError:
            raise ImportError('%s needs hangulize>=0.0.5' %
                              type(self).__name__)
        self._hangulize = hangulize
        return hangulize

    def __init__(self, word, code=None, iso639=None, lang=None):
        hangulize = self._import_hangulize()
        self.lang = lang or hangulize.get_lang(code, iso639)
        super(Loanword, self).__init__(word)

    def read(self):
        """Transcribes into Hangul using `Hangulize
        <http://packages.python.org/hangulize>`_.

        >>> Loanword('Guido van Rossum', 'nld').read()
        '히도 판로쉼'
        >>> Loanword('საქართველო', 'kat').read()
        '사카르트벨로'
        >>> Loanword('Leonardo da Vinci', 'ita').read()
        '레오나르도 다 빈치'
        """
        hangulize = self._import_hangulize()
        return hangulize.hangulize(self.basic(), lang=self.lang)
