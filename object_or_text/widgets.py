from __future__ import unicode_literals

"""
The provided widgets are meant to rely on an Autocomplete class.

- :py:class:`ChoiceWidget` :py:class:`django:django.forms.Select`

ChoiceWidget is intended to work as a replacement for django's Select widget,
and MultipleChoiceWidget for django's SelectMultiple,

Constructing a widget needs an Autocomplete class or registered autocomplete
name.

The choice autocomplete widget renders from autocomplete_light/widget.html
template.
"""

from django import forms

from autocomplete_light.widgets import WidgetBase, TextWidget



__all__ = ['ObjectOrTextWidget',]


class ObjectOrTextWidget(TextWidget):
    """
    Widget that just adds an autocomplete to fill a text input.

    Note that it only renders an ``<input>``, so attrs and widget_attrs are
    merged together.
    """

    def __init__(self, autocomplete=None, widget_js_attributes=None,
            autocomplete_js_attributes=None, extra_context=None, registry=None,
            widget_template=None, widget_attrs=None, *args,
            **kwargs):

        forms.TextInput.__init__(self, *args, **kwargs)

        WidgetBase.__init__(self, autocomplete, widget_js_attributes,
                autocomplete_js_attributes, extra_context, registry,
                widget_template, widget_attrs)

    def render(self, name, value, attrs=None):
        """ Proxy Django's TextInput.render() """
        return forms.TextInput.render(self, name, value, attrs)

    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = super(ObjectOrTextWidget, self).build_widget_attrs()
        attrs.update(super(ObjectOrTextWidget, self).build_attrs(
            extra_attrs, **kwargs))

        def update_attrs(source, prefix=''):
            for key, value in source.items():
                key = 'data-%s%s' % (prefix, key.replace('_', '-'))
                attrs[key] = value

        update_attrs(self.widget_js_attributes, 'widget-')
        update_attrs(self.autocomplete_js_attributes, 'autocomplete-')

        attrs['data-widget-bootstrap'] = 'text'
        attrs['class'] += ' autocomplete-light-text-widget'

        return attrs
