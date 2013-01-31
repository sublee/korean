# -*- coding: utf-8 -*-
"""
    korean.ext.jinja2
    ~~~~~~~~~~~~~~~~~

    Jinja2_ is one of the most used template engines for Python. This module
    contains Jinja2 template engine extensions to make :mod:`korean` easy to
    use.

    .. versionadded:: 0.1.5

    .. versionchanged:: 0.1.6
       Moved from :mod:`korean.l10n.jinja2ext` to :mod:`korean.ext.jinja2`.

    .. _Jinja2: http://jinja.pocoo.org/docs

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

       <h2>Conditional <code>autoproofread</code> block</h2>
       {% autoproofread locale.startswith('ko') %}
         {{ name }}은(는) {{ obj }}을(를) 획득했다.
       {% endautoproofread %}

    The import name is ``korean.ext.jinja2.proofread``. Just add it into
    your Jinja2 environment by the following code::

       from jinja2 import Environment
       jinja_env = Environment(extensions=['korean.ext.jinja2.proofread'])

    .. versionadded:: 0.1.5

    .. versionchanged:: 0.1.6
       Added ``enabled`` argument to ``{% autoproofread %}``.
    """

    tags = ['autoproofread']

    def __init__(self, environment):
        environment.filters['proofread'] = l10n.proofread

    def _proofread(self, enabled, caller):
        return l10n.proofread(caller()) if enabled else caller()

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        if parser.stream.current.type == 'block_end':
            args = [nodes.Const(True)]
        else:
            args = [parser.parse_expression()]
        body = parser.parse_statements(['name:end%s' % self.tags[0]],
                                       drop_needle=True)
        call = self.call_method('_proofread', args)
        return nodes.CallBlock(call, [], [], body, lineno=lineno)


# nicer import name
proofread = ProofreadingExtension
