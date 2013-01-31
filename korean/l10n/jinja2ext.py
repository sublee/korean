# -*- coding: utf-8 -*-
"""
    korean.l10n.jinja2ext
    ~~~~~~~~~~~~~~~~~~~~~

    This module has been moved to :mod:`korean.ext.jinja2`.

    .. versionadded:: 0.1.5

    .. versionchanged:: 0.1.6
       Moved to :mod:`korean.ext.jinja2`.

    :copyright: (c) 2012-2013 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import, unicode_literals
import warnings

from ..ext.jinja2 import ProofreadingExtension, proofread


warnings.warn('This module has been moved to %r' % proofread.__module__,
              DeprecationWarning)
