# -*- coding: utf-8 -*-
"""
    korean.ext.django.apps
    ~~~~~~~~~~~~~~~~~~~~~~

    A default AppConfig definition for Django 1.7+.

    .. versionadded:: 0.1.9

    .. _Django: https://www.djangoproject.com/

    :copyright: (c) 2012-2013 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import, unicode_literals

try:
    from django.apps import AppConfig
except ImportError:
    pass
else:
    class KoreanConfig(AppConfig):
        name = 'korean.ext.django'
        label = 'korean'

        def ready(self):
            pass
