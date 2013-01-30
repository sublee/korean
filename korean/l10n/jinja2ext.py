# -*- coding: utf-8 -*-
"""
    korean.l10n.jinja2ext
    ~~~~~~~~~~~~~~~~~~~~~

    A module containing Jinja2 template engine extensions.

    :copyright: (c) 2012-2013 by Heungsub Lee
    :license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import, unicode_literals

from jinja2 import nodes
from jinja2.ext import Extension
from jinja2.utils import Markup

from .. import l10n


class ProofreadingExtension(Extension):
    """A Jinja2 extention which registers the ``proofread`` filter and the
    ``autoproofread`` block:

    .. sourcecode:: jinja

       <h1>ProofreadingExtension Usage</h1>

       <h2>Single filter</h2>
       {{ (name ~ '은(는) ' ~ obj ~ '을(를) 획득했다.')|proofread }}

       <h2>Filter chaining</h2>
       {{ '%s은(는) %s을(를) 획득했다.'|format(name, obj)|proofread }}

       <h2><code>autoproofread</code> block</h2>
       {% autoproofread %}
         {{ name }}은(는) {{ obj }}을(를) 획득했다.
       {% endautoproofread %}

    The import name is ``korean.l10n.jinja2ext.proofread``. Just add it into
    your Jinja2 environment by following code::

       from jinja2 import Environment
       jinja_env = Environment(extensions=['korean.l10n.jinja2ext.proofread'])

    .. versionadded:: 0.1.5
    """

    tags = ['autoproofread']

    def __init__(self, environment):
        environment.filters['proofread'] = l10n.proofread

    def _proofread(self, caller):
        return l10n.proofread(caller())

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        end_token = 'name:end%s' % self.tags[0]
        body = parser.parse_statements([end_token], drop_needle=True)
        call = self.call_method('_proofread')
        return nodes.CallBlock(call, [], [], body, lineno=lineno)


# nicer import name
proofread = ProofreadingExtension
