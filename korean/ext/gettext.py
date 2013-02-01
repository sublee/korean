# -*- coding: utf-8 -*-
"""
    korean.ext.gettext
    ~~~~~~~~~~~~~~~~~~

    `Gettext <http://www.gnu.org/software/gettext>`_ is an internationalization
    and localization system commonly used for writing multilingual programs on
    Unix-like OS. This module contains utilities to integrate Korean and the
    Gettext system. It also works well with Babel_.

    .. _Babel: http://babel.edgewall.org/

    :copyright: (c) 2012-2013 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import, unicode_literals
from functools import partial

from ..l10n import Template


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
        >>> _('{0} appears.').format(_('John'))
        '존이 나타났다.'
        >>> _('{0} appears.').format(_('Christina'))
        '크리스티나가 나타났다.'

    :param translations: the Gettext translations object to be patched that
                         would refer the catalog for ko_KR.
    """
    methods_to_patch = ['gettext', 'ngettext']
    if hasattr(translations, 'ugettext'):
        methods_to_patch = ['u' + meth for meth in methods_to_patch]
    for meth in methods_to_patch:
        def patched(orig, *args, **kwargs):
            return Template(orig(*args, **kwargs))
        patched.__name__ = str(meth)
        orig = getattr(translations, meth)
        setattr(translations, meth, partial(patched, orig))
    return translations
