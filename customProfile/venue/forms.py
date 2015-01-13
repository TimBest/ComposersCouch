from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, HTML, Layout, Submit

from accounts.models import VenueProfile
from annoying.functions import get_object_or_None
from customProfile.venue import models

class BiographyForm(forms.ModelForm):

    def __init__(self, *args, **kw):
        super(BiographyForm, self).__init__(*args, **kw)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                'biography',
            ),
        )
    """def clean_biography(self):
        biography = self.cleaned_data['biography']
        raise ValidationError("Email already exists")
        return biography"""
    class Meta:
        model = VenueProfile
        widgets = {
          'biography' : forms.Textarea(attrs={'rows': 2, 'cols': 19}),
        }
        fields = ('biography',)

class HoursForm(forms.ModelForm):
    start = forms.TimeField(label=_("Open"), required=False,
                            widget=forms.TimeInput(format='%I:%M %p'),
                            input_formats=['%I:%M %p'])
    end = forms.TimeField(label=_("Close"), required=False,
                          widget=forms.TimeInput(format='%I:%M %p'),
                          input_formats=['%I:%M %p'])
    def __init__(self, *args, **kw):
      super(HoursForm, self).__init__(*args, **kw)
      self.fields['start'].label = False
      self.fields['end'].label = False
      self.helper = FormHelper()
      self.helper.form_tag = False
      self.helper.disable_csrf = True
      self.helper.layout = Layout(
        Div(
          HTML (
            "<div class='col-sm-2 left'>{{day}}</div>"
          ),
          Div('start',css_class='col-sm-5 center',),
          Div('end',css_class='col-sm-5 right',),
          css_class='row no-gutter',
        ),
      )

    class Meta:
        model = models.Hours
        fields = ('start','end',)

class EquipmentForm(forms.ModelForm):
    remove = forms.BooleanField(required=False)
    def __init__(self, *args, **kw):
      super(EquipmentForm, self).__init__(*args, **kw)
      self.fields['quantity'].label = False
      self.fields['name'].label = False
      self.fields['remove'].label = ''
      self.helper = FormHelper()
      self.helper.form_tag = False
      self.helper.layout = Layout(
            Div(
              Div('id',css_class='hidden',),
              Div(
                Div('quantity',css_class='col-xs-3 left',),
                Div('name',css_class='col-xs-7',),
                Div('remove',css_class='col-xs-2',),
                css_class='row no-gutter',
              ),
              Div('category',css_class='hidden',),
            ),
      )

    def save(self, commit=False):
        remove = self.cleaned_data.get('remove', False)
        formData = super(EquipmentForm, self).save(commit=False)
        if remove:
            equipment = get_object_or_None(models.Equipment, id=formData.id)
            if equipment:
                equipment.delete()
            return None
        return formData

    class Meta:
        model = models.Equipment
        fields = ('id','name','quantity','category',)

class PoliciesForm(forms.ModelForm):
    remove = forms.BooleanField(label=_(u'remove'),
                                initial=False,
                                required=False)
    def __init__(self, *args, **kw):
      super(PoliciesForm, self).__init__(*args, **kw)
      self.helper = FormHelper()
      self.helper.form_tag = False
      self.helper.layout = Layout(
        Div(
          Div('title',css_class='col-sm-5 left',),
          Div('description',css_class='col-sm-5 center',),
          Div('remove',css_class='col-sm-2 right',),
          css_class='row no-gutter',
        ),
      )
    def save(self,  commit=False):
        remove = self.cleaned_data.get('remove', False)
        formData = super(PoliciesForm, self).save(commit=False)
        policy = get_object_or_None(models.Policies, id=formData.id)
        if remove:
            if policy:
                policy.delete()
            return None
        return formData

    class Meta:
        model = models.Policies
        widgets = {
          'description' : forms.Textarea(attrs={'rows': 2, 'cols': 19}),
        }
        fields = ('title','description',)

class SeatingForm(forms.ModelForm):

    def __init__(self, *args, **kw):
        super(SeatingForm, self).__init__(*args, **kw)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
          'capacity',
        )

    class Meta:
        model = models.Seating
        fields = ('capacity',)

class StaffForm(forms.ModelForm):
    delete = forms.BooleanField(label=_(u'delete'),
                                initial=False,
                                required=False)
    def __init__(self, *args, **kw):
        super(StaffForm, self).__init__(*args, **kw)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                'job_title',
                'biography',
                'delete',
            ),
        )

    def save(self, id=None, commit=False):
        delete = self.cleaned_data.get('delete', False)
        if delete:
            if id:
                staff = get_object_or_None(models.Staff, id=id)
                staff.contact.delete()
                staff.delete()
            return None
        return super(StaffForm, self).save(commit=commit)

    class Meta:
        model = models.Staff
        widgets = {
          'biography' : forms.Textarea(attrs={'rows': 2, 'cols': 19}),
        }
        fields = ('job_title', 'biography',)
