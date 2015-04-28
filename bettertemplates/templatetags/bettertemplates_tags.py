# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template
from django.conf import settings
from django.template.base import Template
from django.template.loader import get_template
from django.template.loader_tags import do_include, BlockNode

import six
from copy import copy

register = template.Library()


@register.tag(name='includeblock')
def do_include_block(parser, token):
    """
        Works like the {% include <template_name> %} django templatetag, 
        but additionally allows for definition of inline blocks that can be 
        referenced in the included template.
        Usage:
            
            {% includeblock 'example/includable_template.html' <...> %}
                {% block myblock %}
                    <p>An inner block. Reference this using {{ myblock }} in the included template!</p>
                {% endblock myblock %}
                <b>This content is never rendered because it appears outside inner blocks!</b>
            {% endincludeblock %}
    """
    # inherit behaviour form ``include`` templatetag
    include_node = do_include(parser, token)
    
    # make the parser "forget" any blocks encountered in the inner includeblock, 
    # so duplicate blocks don't cause a TemplateSyntaxError
    loaded_blocks = copy(parser.__loaded_blocks)
    nodelist = parser.parse(('endincludeblock',))
    parser.__loaded_blocks = loaded_blocks
    
    parser.delete_first_token()
    return IncludeBlockNode(nodelist, include_node)


class IncludeBlockNode(template.Node):
    """ The {% includeblock <template> ... %} tag works just like an {% include ... %} templatetag,
        with the addition of allowing an inner block of content to be specified. The tag
        allows all <with> kwargs supplied to the tag, just like the {% include ... %} tag. 
    
        We render all nodes found inside the {% includeblock <template> %} Tag.
        Nodes found inside a {% block %} block are rendered into a context variable with the name
            of their block. They can be used in the included <template> by accessing the variable 
            with the name of that block.
        Nodes found outside {% block %} blocks are rendered together and output after the last node 
            in the specified rendered <template>.
    """ 
    
    def __init__(self, nodelist, include_node):
        self.nodelist = nodelist
        self.include_node = include_node

    def render(self, context):
        try:
            # from django.template.loader_tags.IncludeNode:
            # parse the included template
            # django <= 1.6 compatibility. stores FilterExpression in self.template_name or has
            #     self.template as Template
            if not hasattr(self.include_node, 'template'):
                self.include_node.template = self.include_node.template_name
            if not isinstance(self.include_node.template, Template):
                # django >= 1.7
                self.include_node.template = self.include_node.template.resolve(context)
                if not callable(getattr(self.include_node.template, 'render', None)):
                    # If not, we'll try get_template
                    self.include_node.template = get_template(self.include_node.template)
            values = dict([(name, var.resolve(context)) for name, var
                       in six.iteritems(self.include_node.extra_context)])
            
            if self.include_node.isolated_context:
                context = context.new(values)
            else:
                context.update(values)
                
            # render each named block in the inner block into a context variable
            for block in self.nodelist.get_nodes_by_type(BlockNode):
                values[block.name] = block.nodelist.render(context)#block_output
                del self.nodelist[self.nodelist.index(block)]
                
            # render the included template
            output = self.include_node.template.render(context)
                
            if not self.include_node.isolated_context:
                context.pop()
            
            return output
        except:
            if settings.TEMPLATE_DEBUG:
                raise
            return ''
        
