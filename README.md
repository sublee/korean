korean -- A library for Korean morphology
=========================================

Sometimes you should localize your project to Korean. But common i18n
solutions such as gettext are not working with non Indo-European language
well. Korean also has many morphological difference. "korean" a Python
module provides useful Korean morphological functions. (in the future)

Here is an example for using Korean particle (postposition) formatter:

    >>> import korean
    >>> subj = korean.Noun(u'이흥섭')
    >>> obj = korean.Noun(u'한국어')
    >>> verb = korean.Verb(u'좋아하다')
    >>> print u'{0:이} {1:을} {2:ㅂ니다}.'.format(subj, obj, verb)
    이흥섭이 한국어를 좋아합니다.

Do not use "을(를)" anymore.
