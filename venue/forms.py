from django import forms
from django.utils.translation import ugettext_lazy as _

from venue.models import VenueProfile
from annoying.functions import get_object_or_None
from venue import models

class BiographyForm(forms.ModelForm):

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

    class Meta:
        model = models.Hours
        fields = ('id','start','end',)

class EquipmentForm(forms.ModelForm):
    remove = forms.BooleanField(required=False)

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
        fields = ('id','title','description',)

class SeatingForm(forms.ModelForm):

    class Meta:
        model = models.Seating
        fields = ('capacity',)

class StaffForm(forms.ModelForm):
    delete = forms.BooleanField(label=_(u'delete'),
                                initial=False,
                                required=False)

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
