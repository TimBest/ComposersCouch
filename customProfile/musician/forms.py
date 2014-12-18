from django import forms

from autocomplete_light import ModelForm, MultipleChoiceWidget
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout

from models import Member, Instrument
from accounts.models import MusicianProfile
from annoying.functions import get_object_or_None


class BiographyForm(forms.ModelForm):

    def __init__(self, *args, **kw):
      super(BiographyForm, self).__init__(*args, **kw)
      self.helper = FormHelper()
      self.helper.form_tag = False
      self.helper.layout = Layout(
        Field('biography',spellcheck="true"),
      )
    class Meta:
        model = MusicianProfile
        widgets = {
          'biography' : forms.Textarea(attrs={'rows': 2, 'cols': 19}),
        }
        fields = ('biography',)

class MemberForm(ModelForm):
    remove_member = forms.BooleanField(required=False)
    instruments = forms.ModelMultipleChoiceField(
                      Instrument.objects.all(),
                      required=False,
                      widget=MultipleChoiceWidget(
                          'InstrumentAutocomplete',
                          attrs
={'placeholder':''}))

    def __init__(self, *args, **kw):
      super(MemberForm, self).__init__(*args, **kw)
      self.helper = FormHelper()
      self.helper.form_tag = False
      self.helper.layout = Layout(
        'name',
        'instruments',
        Field('biography',spellcheck="true"),
        Div(
          Div('current_member',css_class='col-sm-6 left',),
          Div('remove_member',css_class='col-sm-6 right',),
          css_class='row no-gutter',
        ),
      )

    def save(self):
        delete = False
        try:
            delete = self.cleaned_data['remove_member']
        except:
            pass
        formData = super(MemberForm, self).save(commit=False)
        member = get_object_or_None(Member, id=formData.id)
        if delete and member:
            member.delete()
            return None

        formData.save()
        return formData

    class Meta:
        model = Member
        widgets = {
          'biography' : forms.Textarea(attrs={'rows': 2, 'cols': 19}),
        }
        fields = ('name','current_member','instruments','biography',)
