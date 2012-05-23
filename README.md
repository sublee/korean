korean
======

Processing Korean language.

    >>> import korean
    >>> subj = korean.Word(u'이흥섭')
    >>> obj = korean.Word(u'한국어')
    >>> verb = korean.Verb(u'좋아하다')
    >>> print u'{0:이} {1:을} {2:ㅂ니다}.'.format(subj, obj, verb)
    이흥섭이 한국어를 좋아합니다.
