from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

from autocomplete_light import ModelForm
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout

from models import Image


def clean_image(image):
    if image:
        if int(image._size) > int(settings.PHOTOS_MAX_UPLOAD_SIZE):
            raise ValidationError(
                _('Please keep filesize under %(max)s. Current filesize %(current)s'),
                code='invalid',
                params={'max': filesizeformat(settings.PHOTOS_MAX_UPLOAD_SIZE), 'current' : filesizeformat(image._size)},
            )
    return image

class ImageOnlyForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ImageOnlyForm, self).__init__(*args, **kwargs)
        self.fields['image'].label = 'Photo'
        self.fields['image'].required = False
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
              'image',
            ),
        )

    class Meta(object):
        model = Image
        fields = ['image',]

    def clean_image(self):
        image = self.cleaned_data.get("image", "")
        if image != self.instance.image:
            return clean_image(image)
        return image

class ImageForm(ImageOnlyForm):
    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['image'].required = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                'image',
                'title',
            ),
        )

    class Meta(object):
        model = Image
        fields = ('image','title',)

class AlbumArtForm(ImageOnlyForm):
    def __init__(self, *args, **kwargs):
        super(AlbumArtForm, self).__init__(*args, **kwargs)
        self.fields['image'].label = 'Album Art'

class SeatingChartForm(ImageOnlyForm):
    def __init__(self, *args, **kwargs):
        super(SeatingChartForm, self).__init__(*args, **kwargs)
        self.fields['image'].label = 'Seating Chart'

class PosterForm(ImageOnlyForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PosterForm, self).__init__(*args, **kwargs)
        self.fields['image'].label = 'Poster'

class MugshotForm(ImageOnlyForm):
    def __init__(self, *args, **kwargs):
        super(MugshotForm, self).__init__(*args, **kwargs)
        self.fields['image'].label = 'Mugshot'
