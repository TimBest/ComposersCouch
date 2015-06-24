from __future__ import unicode_literals

from django import forms

from autocomplete_light import ChoiceWidget, registry as default_registry


__all__ = ['ObjectOrTextWidget',]

class ModelWidget(ChoiceWidget):

    def build_attrs(self, extra_attrs=None, **kwargs):
        max_values = extra_attrs.get('data-widget-maximum-values', 1)
        extra_attrs['data-widget-maximum-values'] =  max_values
        attrs = super(ModelWidget, self).build_widget_attrs()
        attrs.update(super(ModelWidget, self).build_attrs(extra_attrs, **kwargs))

        def update_attrs(source, prefix=''):
            for key, value in source.items():
                key = 'data-%s%s' % (prefix, key.replace('_', '-'))
                attrs[key] = value

        update_attrs(self.widget_js_attributes, 'widget-')
        update_attrs(self.autocomplete_js_attributes, 'autocomplete-')

        attrs['title'] = "model-or-text-widget-model-input"
        return attrs



class ObjectOrTextWidget(forms.MultiWidget):

    def __init__(self, attrs={}, autocomplete=None, widget_js_attributes=None,
            autocomplete_js_attributes=None, extra_context=None, registry=None,
            widget_template="autocomplete_light/widget.html", widget_attrs={}):
        attrs['title'] = "model-or-text-widget-text-input"
        widgets = (
            ModelWidget(
                autocomplete, widget_js_attributes,
                autocomplete_js_attributes, extra_context,
                registry, widget_template, widget_attrs,
            ),
            forms.TextInput(attrs=attrs),
        )

        self.registry = default_registry if registry is None else registry
        self.autocomplete = self.registry.get_autocomplete_from_arg(
            autocomplete
        )
        super(ObjectOrTextWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        self.value = value
        if value and isinstance(value, basestring):
            return [value, value]
        else:
            return [value, value]
