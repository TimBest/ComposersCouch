from django import forms
from django.utils.translation import ugettext_lazy as _

from autocomplete_light import FixedModelForm
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Layout, Submit

from models import Image


class ImageForm(FixedModelForm):
    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                'image',
                'title',
                'description',
            ),
        )

    class Meta(object):
        model = Image
        widgets = {
            'description' : forms.Textarea(
                                attrs={'rows': 2, 'cols': 19}),
        }
        fields = ('image','title','description',)

class ImageOnlyForm(FixedModelForm):

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
