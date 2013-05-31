# -*- coding: utf-8 -*-
"""
    korean.ext.django.templatetags.korean
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A module containing Django template tag and filter for korean.

    .. versionadded:: 0.1.7

    .. _Django: https://www.djangoproject.com/

    :copyright: (c) 2012-2013 by Heungsub Lee, Hyunwoo Park
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import, unicode_literals

from django import template
from django.template.defaultfilters import stringfilter

from .... import l10n


register = template.Library()


class ProofReadNode(template.Node):

    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        output = self.nodelist.render(context)
        return l10n.proofread(output)


@register.tag(name='proofread')
def do_proofread(parser, token):
    """A Django tag for ``proofread``

    .. sourcecode:: django

       <h1>proofread tag Usage</h1>

       {% load korean %}
       {% proofread %}
         {{ name }}은(는) {{ obj }}을(를) 획득했다.
       {% endproofread %}
    """
    nodelist = parser.parse(['endproofread'])
    parser.delete_first_token()
    return ProofReadNode(nodelist)


@register.filter
@stringfilter
def proofread(value):
    """A Django filter for ``proofread``

    .. sourcecode:: django

       <h1>proofread filter Usage</h1>

       {% load korean %}
       {{ 용사은(는) 검을(를) 획득했다.|proofread }}
    """
    return l10n.proofread(value)
