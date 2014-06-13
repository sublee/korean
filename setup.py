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
from __future__ import with_statement
import re
from setuptools import find_packages, setup
from setuptools.command.test import test
import sys


# detect the current version
with open('korean/__init__.py') as f:
    version = re.search(r'__version__\s*=\s*\'(.+?)\'', f.read()).group(1)
assert version


# use pytest instead
def run_tests(self):
    pyc = re.compile(r'\.pyc|\$py\.class')
    test_file = pyc.sub('.py', __import__(self.test_suite).__file__)
    raise SystemExit(__import__('pytest').main([test_file]))
test.run_tests = run_tests


tests_require = ['pytest', 'jinja2']
if sys.version_info < (3,):
    tests_require.extend(['hangulize', 'django'])
setup(
    name='korean',
    version=version,
    license='BSD',
    author='Heungsub Lee',
    author_email=re.sub('((sub).)(.*)', r'\2@\1.\3', 'sublee'),
    url='http://pythonhosted.org/korean',
    description='A library for Korean morphology',
    long_description=__doc__,
    platforms='any',
    packages=find_packages(),
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
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Localization',
        'Topic :: Text Processing :: Linguistic',
    ],
    install_requires=['setuptools'],
    test_suite='koreantests',
    tests_require=tests_require,
    use_2to3=(sys.version_info >= (3,)),
)
