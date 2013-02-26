# -*- coding: utf-8 -*-
"""
    korean.__main__
    ~~~~~~~~~~~~~~~

    Command-line tools.

    :copyright: (c) 2012-2013 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import
import contextlib
import sys

from baker import Baker

from . import l10n


baker = Baker()


@contextlib.contextmanager
def file_or_stdin(path):
    f = open(path) if path is not None else sys.stdin
    yield f
    f.close()


@baker.command
def proofread(path=None, charset='utf-8'):
    with file_or_stdin(path) as f:
        for line in f.xreadlines():
            print l10n.proofread(line.decode(charset)),


@baker.command
def validate(path=None, charset='utf-8'):
    pass


if __name__ == '__main__':
    baker.run()
