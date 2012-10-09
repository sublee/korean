===========================================
 Korean -- A library for Korean morphology
===========================================

Sometimes you should localize your project for Korean. But common
internationalization solutions such as `Gettext
<http://docs.python.org/library/gettext.html>`_ are not working with non
Indo-European languages well. We would get an awkward Korean sentence with
those solutions because Korean has many morphological difference with
Indo-European language.

:mod:`korean` a Python module provides useful Korean morphological functions
for getting natural Korean sentences.

Allomorphic particle
~~~~~~~~~~~~~~~~~~~~

In English, "be" is an allomorph. So the English localization system should can
select the correct form such as "is", "am", "are". Fortunately Gettext offers
``ngettext`` to make a natural plural expression. If it didn't offer, you would
see that awkward sentence:

.. sourcecode:: pycon

   >>> print _('Here is(are) %d apple(s).') % 1
   Here is(are) 1 apple(s).
   
Some Korean particle (postposition) is also an allomorph but they need
different allomorphic selection rule; it needs check the forward phoneme.
However common internationalization solutions don't offer about it. Of course,
:mod:`korean` does:

.. sourcecode:: pycon

   >>> from korean import Noun, NumberWord, Loanword
   >>> fmt = u'{subj:은} {obj:을} 먹었다.'
   >>> fmt2 = u'{subj:은} 레벨 {level:이} 되었다.'
   >>> print fmt.format(subj=Noun(u'나'), obj=Noun(u'밥'))
   나는 밥을 먹었다.
   >>> print fmt.format(subj=Noun(u'학생'), obj=Noun(u'돈까스'))
   학생은 돈까스를 먹었다.
   >>> print fmt2.format(subj=Noun(u'용사'), level=NumberWord(4))
   용사는 레벨 4가 되었다.
   >>> print fmt2.format(subj=Noun(u'마왕'), level=NumberWord(98))
   마왕은 레벨 98이 되었다.
   >>> print fmt2.format(subj=Loanword(u'Leonardo da Vinci', 'ita'),
   ...                   level=NumberWord(67))
   Leonardo da Vinci는 레벨 67이 되었다.

Working with Gettext
~~~~~~~~~~~~~~~~~~~~

It also can be worked with Gettext. Just use :func:`korean.l10n.patch_gettext`
function:

.. sourcecode:: pot

   msgid ""
   msgstr ""
   "Locale: ko_KR\n"
   "Content-Type: text/plain; charset=utf-8\n"
   "Content-Transfer-Encoding: 8bit\n"

   msgid "I like a {0}."
   msgstr "나는 {0:을} 좋아합니다."

   msgid "banana"
   msgstr "바나나"

   msgid "game"
   msgstr "게임"

.. sourcecode:: pycon

   >>> from babel.support import Translations
   >>> import korean
   >>> translations = Translations.load('i18n', 'ko_KR')
   >>> korean.l10n.patch_gettext(translations)
   >>> _ = translations.ugettext
   >>> _(u'I like a {0}.').format(_(u'banana'))
   나는 바나나를 좋아합니다.
   >>> _(u'I like a {0}.').format(_(u'game'))
   나는 게임을 좋아합니다.

Proofreading legacy text
~~~~~~~~~~~~~~~~~~~~~~~~

If your text already has been written with naive particle such as "을(를)",
use :func:`korean.l10n.proofread` fucntion to get correct particles:

.. sourcecode:: pycon

   >>> import korean
   >>> korean.l10n.proofread(u'용사은(는) 검을(를) 획득했다.')
   용사는 검을 획득했다.
   >>> korean.l10n.proofread(u'집(으)로 가자.')
   집으로 가자.

API
~~~

.. automodule:: korean.morphology
   :members:

.. automodule:: korean.l10n
   :members:

.. automodule:: korean.hangul
   :members:

..
    .. autofunction:: korean.hangul.char_offset

    .. autofunction:: korean.hangul.is_hangul

    .. autofunction:: korean.hangul.is_consonant

    .. autofunction:: korean.hangul.is_vowel

    .. autofunction:: korean.hangul.is_initial

    .. autofunction:: korean.hangul.is_final

    .. autofunction:: korean.hangul.get_initial

    .. autofunction:: korean.hangul.get_final

    .. autofunction:: korean.hangul.split_char

    .. autofunction:: korean.hangul.join_char

Installation
~~~~~~~~~~~~

Install via `PyPI <http://pypi.python.org/pypi/korean>`_ with
``easy_install`` or ``pip`` command:

.. sourcecode:: bash

   $ easy_install korean

.. sourcecode:: bash

   $ pip install korean

or check out development version:

.. sourcecode:: bash

   $ git clone git://github.com/sublee/korean.git

Licensing and Author
~~~~~~~~~~~~~~~~~~~~

This project licensed with `BSD <http://en.wikipedia.org/wiki/BSD_licenses>`_,
so feel free to use and manipulate as long as you respect these licenses. See
`LICENSE <https://github.com/sublee/korean/blob/master/LICENSE>`_ for the
details.

I'm `Heungsub Lee <http://subl.ee/>`_. Any regarding questions or patches are
welcomed.
