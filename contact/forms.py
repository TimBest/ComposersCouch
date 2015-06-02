from django.forms import CharField

from autocomplete_light.forms import ModelForm

from contact.models import Location, Contact
from social_links.forms import clean_url


class ZipcodeForm(ModelForm):

    def __init__(self, *args, **kw):
        super(ZipcodeForm, self).__init__(*args, **kw)
        self.fields['zip_code'].required = True

    class Meta:
        model = Location
        fields = ['zip_code']

class LocationForm(ModelForm):

    def __init__(self, *args, **kw):
      super(LocationForm, self).__init__(*args, **kw)
      self.fields['zip_code'].required = True

    class Meta:
        model = Location
        fields = ['address_1','address_2','city','state','zip_code',]

class NonUserLocationForm(LocationForm):

    def __init__(self, *args, **kw):
      super(NonUserLocationForm, self).__init__(*args, **kw)
      self.fields['zip_code'].required = False


class ContactForm(ModelForm):
    phone = CharField(min_length=7, required=False)

    def clean_url(self):
        return clean_url(self.cleaned_data.get("url", ""))

    class Meta:
        model = Contact
        fields = ['name','email','phone','url',]
