Korean -- A library for Korean morphology
=========================================

Sometimes you should localize your project to Korean. But common i18n solutions
such as gettext are not working with non Indo-European language well. Korean
also has many morphological difference. "korean" a Python module provides
useful Korean morphological functions. (in the future)

Here is an example for using Korean particle (postposition) formatter:

    >>> from korean import Noun
    >>> fmt = u'{subj:은} {obj:을} 먹었다.'
    >>> print fmt.format(subj=Noun(u'나'), obj=Noun(u'밥'))
    나는 밥을 먹었다.
    >>> print fmt.format(subj=Noun(u'학생'), obj=Noun(u'돈까스'))
    학생은 돈까스를 먹었다.

Do not use "을(를)" anymore.
