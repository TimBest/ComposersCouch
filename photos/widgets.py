from itertools import chain

from django.conf import settings
from django.forms import widgets
from django.forms.widgets import flatatt
from django.utils.encoding import force_text, force_unicode
from django.utils.functional import Promise
from django.utils import html
from django.utils.safestring import mark_safe

from annoying.functions import get_object_or_None
from photos.models import Image


class ImageSelectWidget(widgets.Select):
    """
    Customizable select widget, that allows to render
    data-xxx attributes from choices.

    .. attribute:: data_attrs

        Specifies object properties to serialize as
        data-xxx attribute. If passed ('id', ),
        this will be rendered as:
        <option data-id="123">option_value</option>
        where 123 is the value of choice_value.id

    """

    def __init__(self, attrs=None, choices=(), data_attrs=()):
        self.data_attrs = data_attrs
        super(ImageSelectWidget, self).__init__(attrs, choices)

    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_unicode(option_value)
        other_html = (option_value in selected_choices) and \
                         u' selected="selected"' or ''
        try:
            image = get_object_or_None(Image, id=option_label)
        except:
            image = None
        if image:
            for data_attr in self.data_attrs:
                other_html += ' data-%s="%s%s"' % (data_attr, settings.MEDIA_URL,image.image)
            
            option_label = self.image_id_to_title(image.id)

        return u'<option value="%s"%s>%s</option>' % (
            html.escape(option_value), other_html,
            html.conditional_escape(force_unicode(option_label)))

    def image_id_to_title(self, imageID):

        try:
            image = get_object_or_None(Image, id=imageID)
        except:
            image = None

        if image:
            return image.title
        else:
            return ""
