===========================================
 Korean -- A library for Korean morphology
===========================================

Sometimes you should localize your project to Korean. But common i18n solutions
such as `Gettext <http://docs.python.org/library/gettext.html>`_ are not
working with non Indo-European language well. Korean also has many
morphological difference. :mod:`korean` a Python module provides useful Korean
morphological functions.

Here is an example for using Korean particle (postposition) formatter:

.. sourcecode:: pycon

   >>> from korean import Noun, NumberWord
   >>> fmt = u'{subj:은} {obj:을} 먹었다.'
   >>> fmt2 = u'{subj:은} 레벨 {level:이} 되었다.'
   >>> print fmt.format(subj=Noun(u'나'), obj=Noun(u'밥'))
   나는 밥을 먹었다.
   >>> print fmt.format(subj=Noun(u'학생'), obj=Noun(u'돈까스'))
   학생은 돈까스를 먹었다.
   >>> print fmt2.format(subj=Noun(u'용사'), level=NumberWord(4))
   용사는 레벨 4가 되었다.

Do not use "을(를)" anymore.

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

Working with Gettext
~~~~~~~~~~~~~~~~~~~~

It also can be worked with Gettext. Just use :func:`korean.l10n.patch_gettext()` function:

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

If your legacy already has been wrote with naive particle such as "을(를)", use
:func:`korean.l10n.proofread()` fucntion to get correct particles:

.. sourcecode:: pycon

   >>> import korean
   >>> korean.l10n.proofread(u'용사은(는) 검을(를) 획득했다.')
   용사는 검을 획득했다.
   >>> korean.l10n.proofread(u'집(으)로 가자.')
   집으로 가자.
