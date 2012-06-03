# -*- coding: utf-8 -*-
"""
    korean.l10n
    ~~~~~~~~~~~

    Helpers for localization to Korean.

    :copyright: (c) 2012 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

from functools import partial
from itertools import chain, product

from .inflection import inflect
from .morphology import Noun, NumberWord, Particle


class Template(unicode):
    """The :class:`Template` object extends :class:`unicode` and overrides
    :meth:`format` method. This can format particle format spec without
    evincive :class:`Noun` or :class:`NumberWord` arguments.

    Basically this example:

        >>> import korean
        >>> korean.l10n.Template(u'{0:을} 좋아합니다.').format(u'향수')
        향수를 좋아합니다.

    Is equivalent to the following:

        >>> import korean
        >>> u'{0:을 좋아합니다.}'.format(korean.Noun(u'향수'))
        향수를 좋아합니다.
    """

    def format(self, *args, **kwargs):
        args = list(args)
        for seq, (key, val) in chain(product([args], enumerate(args)),
                                     product([kwargs], kwargs.items())):
            if isinstance(val, unicode):
                seq[key] = Noun(val)
            elif isinstance(val, int):
                seq[key] = NumberWord(val)
        return super(Template, self).format(*args, **kwargs)

    def __repr__(self):
        return '<%s %s>' % \
               (type(self).__name__, super(Template, self).__repr__)


def patch_gettext(translations):
    """Patches Gettext translations object to wrap the result with
    :class:`korean.l10n.Template`. Then the result can work with a particle
    format spec.

    For example, here's a Gettext catalog for ko_KR:

    .. sourcecode:: pot

        msgid "{0} appears."
        msgstr "{0:이} 나타났다."

        msgid "John"
        msgstr "존"

        msgid "Christina"
        msgstr "크리스티나"

    You can use a particle format spec in Gettext messages after translations
    object is patched:

    .. sourcecode:: pycon

        >>> translations = patch_gettext(translations)
        >>> _ = translations.ugettext
        >>> _(u'{0} appears.').format(_(u'John'))
        존이 나타났다.
        >>> _(u'{0} appears.').format(_(u'Christina'))
        크리스티나가 나타났다.

    :param translations: the Gettext translations object to be patched that
                         would refer the catalog for ko_KR.
    """
    for meth in ['ugettext', 'ungettext']:
        def patched(orig, *args, **kwargs):
            return Template(orig(*args, **kwargs))
        patched.__name__ = meth
        orig = getattr(translations, meth)
        setattr(translations, meth, partial(patched, orig))
    return translations


def proofread(text):
    """Replaces naive particles to be correct. First, it finds naive particles 
    such as "을(를)" or "(으)로". Then it checks the forward character of the
    particle and replace with a correct particle.

    :param text: the string that has been written with naive particles.
    """
    for particle in set(Particle._registry.itervalues()):
        for naive in particle.naive():
            while True:
                found = text.find(naive)
                if found < 0:
                    break
                noun = Noun(text[found - 1])
                inflected_particle = inflect(particle, suffix_of=noun)
                text = text[:found] + inflected_particle + \
                       text[found + len(naive):]
    return text
