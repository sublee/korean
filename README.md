Korean -- A library for Korean morphology
=========================================

Sometimes you should localize your project to Korean. But common i18n solutions
such as gettext are not working with non Indo-European language well. Korean
also has many morphological difference. "korean" a Python module provides
useful Korean morphological functions. (in the future)

Here is an example for using Korean particle (postposition) formatter:

    >>> import korean
    >>> subj = korean.Noun(u'이흥섭')
    >>> obj = korean.Noun(u'한국어')
    >>> print u'{subj:은} {obj:을} 사용한다.'.format(subj=subj, obj=obj)
    이흥섭이 한국어를 좋아합니다.

Do not use "을(를)" anymore.
