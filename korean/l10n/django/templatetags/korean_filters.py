"""
    korean.l10n.django.templatetags.korean_filters
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A module containing Django template filters.
"""
from __future__ import absolute_import, unicode_literals

from django import template
from django.template.defaultfilters import stringfilter

from .... import l10n

register = template.Library()


@register.filter
@stringfilter
def proofread(value):
    """A Django filter for ``proofread``

    .. sourcecode:: django

       <h1>Proofread filter Usage</h1>

       <h2>Single filter</h2>
       {{ (name ~ '은(는) ' ~ obj ~ '을(를) 획득했다.')|proofread }}
    """
    return l10n.proofread(value)
