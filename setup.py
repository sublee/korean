# -*- coding: utf-8 -*-
"""
Korean
------

Korean is a library for Korean morphology.

Do not use "을(를)" anymore
```````````````````````````

::

    >>> from korean import Noun
    >>> fmt = u'{:은} {:을} 먹었다.'
    >>> print fmt.format(Noun(u'나'), Noun(u'밥'))
    나는 밥을 먹었다.
    >>> print fmt.format(Noun(u'우리 형'), Noun(u'파스타'))
    우리 형은 파스타를 먹었다.

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
    version='0.0.0',
    license='BSD',
    author='Heungsub Lee',
    author_email='h@subl.ee',
    description='A library for Korean morphology',
    long_description=__doc__,
    platforms='any',
    packages=['korean'],
    package_dir={'korean': 'korean'},
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
    ]
)
