from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.utils.translation import ugettext_lazy as _

from autocomplete_light.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout

from annoying.functions import get_object_or_None
from contact.models import Location, Contact, Zipcode
from social_links.forms import clean_url


class ZipcodeForm(ModelForm):

    def __init__(self, *args, **kw):
        super(ZipcodeForm, self).__init__(*args, **kw)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout('zip_code',)
        self.fields['zip_code'].required = True

    class Meta:
        model = Location
        fields = ['zip_code']

class LocationForm(ModelForm):

    def __init__(self, *args, **kw):
      super(LocationForm, self).__init__(*args, **kw)
      self.helper = FormHelper()
      self.helper.form_tag = False
      self.fields['zip_code'].required = True
      self.helper.layout = Layout(
        Div(
          Div('address_1',css_class='col-sm-6 left',),
          Div('address_2',css_class='col-sm-6 right',),
          css_class='row no-gutter',
        ),
        Div(
          Div('city',css_class='col-sm-4 left',),
          Div('state',css_class='col-sm-4 center',),
          Div('zip_code',css_class='col-sm-4 right',),
          css_class='row no-gutter',
        ),
      )

    class Meta:
        model = Location
        fields = ['address_1','address_2','city','state','zip_code',]

class NonUserLocationForm(LocationForm):

    def __init__(self, *args, **kw):
      super(NonUserLocationForm, self).__init__(*args, **kw)
      self.fields['zip_code'].required = False


class ContactForm(forms.ModelForm):
    phone = forms.CharField(min_length=7, required=False)

    def __init__(self, *args, **kw):
      super(ContactForm, self).__init__(*args, **kw)
      self.helper = FormHelper()
      self.helper.form_tag = False
      self.helper.layout = Layout(
        'name',
        'email',
        'phone',
        'url',
      )

    def clean_url(self):
        return clean_url(self.cleaned_data.get("url", ""))

    class Meta:
        model = Contact
        fields = ['name','email','phone','url',]
