# -*- coding: utf-8 -*-
"""
Korean -- A library for Korean morphology
=========================================

Sometimes you should localize your project to Korean. But common i18n solutions
such as gettext are not working with non Indo-European language well. Korean
also has many morphological difference. "korean" a Python module provides
useful Korean morphological functions.

Do not use "을(를)" anymore
```````````````````````````

::

    >>> from korean import Noun
    >>> fmt = u'{subj:은} {obj:을} 먹었다.'
    >>> print fmt.format(subj=Noun(u'나'), obj=Noun(u'밥'))
    나는 밥을 먹었다.
    >>> print fmt.format(subj=Noun(u'학생'), obj=Noun(u'돈까스'))
    학생은 돈까스를 먹었다.

Links
`````

* `GitHub repository <http://github.com/sublee/korean>`_
* `development version
  <http://github.com/sublee/korean/zipball/master#egg=korean-dev>`_

"""
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='korean',
    version='0.1.3',
    license='BSD',
    author='Heungsub Lee',
    author_email='h@subl.ee',
    description='A library for Korean morphology',
    long_description=__doc__,
    url='http://github.com/sublee/korean',
    platforms='any',
    packages=['korean', 'korean.morphology'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: Korean',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Localization',
        'Topic :: Text Processing :: Linguistic',
    ],
    test_suite='tests.test_suite',
    tests_require=['unittest2', 'Babel'],
)
