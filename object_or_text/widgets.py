from __future__ import unicode_literals

from django import forms
from django.forms.util import flatatt
from django.template.loader import render_to_string
from django.utils import safestring

from autocomplete_light.widgets import WidgetBase
from autocomplete_light import registry as default_registry


__all__ = ['ObjectOrTextWidget',]

class TextWidget(WidgetBase, forms.TextInput):
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

    def build_attrs(self, extra_attrs=None, **kwargs):
        max_values = extra_attrs.get('data-widget-maximum-values', 1)
        extra_attrs['data-widget-maximum-values'] =  max_values
        attrs = super(TextWidget, self).build_widget_attrs()
        attrs.update(super(TextWidget, self).build_attrs(extra_attrs, **kwargs))

        def update_attrs(source, prefix=''):
            for key, value in source.items():
                key = 'data-%s%s' % (prefix, key.replace('_', '-'))
                attrs[key] = value

        update_attrs(self.widget_js_attributes, 'widget-')
        update_attrs(self.autocomplete_js_attributes, 'autocomplete-')

        attrs['data-widget-bootstrap'] = 'text'
        attrs['class'] += ' autocomplete-light-model-or-text-widget'
        return attrs

    def render(self, name, value, attrs=None):
        widget_attrs = self.build_widget_attrs(name)
        attrs = self.build_attrs(attrs)
        self.html_id = attrs.pop('id', name)

        autocomplete = self.autocomplete(values=value)
        print name
        print value
        print attrs
        try:
            choices = [] #autocomplete.choices_for_values()
            #values = [autocomplete.choice_value(c) for c in choices]
        except:
            choices = []
        values = str(value)
        context = {
            'name': name,
            'values': values,
            'choices': choices,
            'widget': self,
            'attrs': safestring.mark_safe(flatatt(attrs)),
            'widget_attrs': safestring.mark_safe(flatatt(widget_attrs)),
            'autocomplete': autocomplete,
        }
        context.update(self.extra_context)

        template = getattr(autocomplete, 'widget_template',
                self.widget_template)
        return safestring.mark_safe(render_to_string(template, context))


class ObjectOrTextWidget(forms.MultiWidget):
    """
    Widget that just adds an autocomplete to fill a text input.

    Note that it only renders an ``<input>``, so attrs and widget_attrs are
    merged together.
    """
    def __init__(self, attrs={}, autocomplete=None, widget_js_attributes=None,
            autocomplete_js_attributes=None, extra_context=None, registry=None,
            widget_template="autocomplete_light/model_or_object_widget.html", widget_attrs=None):
        widgets = (
            TextWidget(
                autocomplete, widget_js_attributes,
                autocomplete_js_attributes, extra_context,
                registry, widget_template, widget_attrs,
            ),
            forms.CheckboxInput(attrs=attrs),
        )

        self.registry = default_registry if registry is None else registry
        self.autocomplete = self.registry.get_autocomplete_from_arg(
            autocomplete
        )

        super(ObjectOrTextWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        self.value = value

        if value and isinstance(value, basestring):
            return [value, False]
        elif value:
            return[value.pk, True]
        else:
            return ["", False]
