from __future__ import absolute_import, unicode_literals  # Python 2 only

from django.contrib.staticfiles.storage import staticfiles_storage
from django import template

from jinja2 import nodes, TemplateSyntaxError
from jinja2.ext import Extension

from feeds.models import Follow
from annoying.functions import get_object_or_None


class FeedExtension(Extension):
    tags = set(['is_following', 'append_to_get'])

    def parse(self, parser):
        tag = next(parser.stream)

        package_name = parser.parse_expression()
        if not package_name:
            raise TemplateSyntaxError("Bad package name", tag.lineno)

        args = [package_name]
        if tag.value == "is_following":
            return nodes.CallBlock(self.call_method('is_following', args), [], [], []).set_lineno(tag.lineno)

        if tag.value == "append_to_get":
            return nodes.CallBlock(self.call_method('append_to_get', args), [], [], []).set_lineno(tag.lineno)

        return []

    def is_following(user, target):
        if get_object_or_None(Follow, user=user, target=target):
            return 'isFollowing'
        return None

    """
    Decorator to facilitate template tag creation
    """
    def easy_tag(func):
        """deal with the repetitive parts of parsing template tags"""
        def inner(parser, token):
            #print token
            try:
                return func(*token.split_contents())
            except TypeError:
                raise template.TemplateSyntaxError('Bad arguments for tag "%s"' % token.split_contents()[0])
        inner.__name__ = func.__name__
        inner.__doc__ = inner.__doc__
        return inner

    class AppendGetNode(template.Node):
        def __init__(self, dict):
            self.dict_pairs = {}
            for pair in dict.split(','):
                pair = pair.split('=')
                self.dict_pairs[pair[0]] = template.Variable(pair[1])

        def render(self, context):
            get = context['request'].GET.copy()

            for key in self.dict_pairs:
                get[key] = self.dict_pairs[key].resolve(context)

            path = context['request'].META['PATH_INFO']

            #print "&".join(["%s=%s" % (key, value) for (key, value) in get.items() if value])

            if len(get):
                path += "?%s" % "&".join(["%s=%s" % (key, value) for (key, value) in get.items() if value])


            return path

    @easy_tag
    def append_to_get(_tag_name, dict):
        return AppendGetNode(dict)
