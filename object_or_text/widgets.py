from __future__ import unicode_literals

from django import forms
from django.contrib.staticfiles.storage import staticfiles_storage

from autocomplete_light.widgets import WidgetBase


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

    def render(self, name, value, attrs=None):
        """ Proxy Django's TextInput.render() """
        return forms.TextInput.render(self, name, value, attrs)

    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = super(TextWidget, self).build_widget_attrs()
        attrs.update(super(TextWidget, self).build_attrs(
            extra_attrs, **kwargs))

        def update_attrs(source, prefix=''):
            for key, value in source.items():
                key = 'data-%s%s' % (prefix, key.replace('_', '-'))
                attrs[key] = value

        update_attrs(self.widget_js_attributes, 'widget-')
        update_attrs(self.autocomplete_js_attributes, 'autocomplete-')

        attrs['data-widget-bootstrap'] = 'text'
        attrs['class'] += ' autocomplete-light-model-or-text-widget'
        return attrs


class ObjectOrTextWidget(forms.MultiWidget):
    """
    Widget that just adds an autocomplete to fill a text input.

    Note that it only renders an ``<input>``, so attrs and widget_attrs are
    merged together.
    """
    def __init__(self, attrs={}, autocomplete=None, widget_js_attributes=None,
            autocomplete_js_attributes=None, extra_context=None, registry=None,
            widget_template=None, widget_attrs=None):
        widgets = (
            TextWidget(
                autocomplete, widget_js_attributes,
                autocomplete_js_attributes, extra_context,
                registry, widget_template, widget_attrs,
            ),
            forms.CheckboxInput(attrs=attrs),
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

    def format_output(self, rendered_widgets):
        deck = u'<span class="deck autocomplete-light-model-or-text-widget"></span>'
        if self.value:
            # TODO: replace this with something that used the declared choice template
            try:
                mugshot = self.value.profile.mugshot.image.url
            except:
                mugshot = staticfiles_storage.url('img/mugshot.png')
            deck = u'<span class="deck autocomplete-light-model-or-text-widget">\
                        <span class="hilight" data-value="%s">\
                            <a href="#" style="display: inline-block;" class="remove text-muted fa fa-times-circle"></a>\
                            <img class="mugshot" src="%s" alt="Profile mugshot" height="45" width="45">\
                            <span >%s</span>\
                       </span>\
                      <span>' % (self.value.pk, mugshot, self.value.profile)
        return (u'%s<a href="#" style="display:none" class="remove text-muted fa fa-times-circle"></a>\
                 <span style="display:none" class="choice-template">\
                 <span class="choice prepend-remove append-option-html">\
                 </span></span></span>' % deck).join(rendered_widgets)
