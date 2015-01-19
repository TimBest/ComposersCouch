from datetime import datetime
from django import forms
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

import autocomplete_light
from autocomplete_light import ModelForm
from crispy_forms.bootstrap import PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, HTML, Layout, Submit
from crispy_forms.bootstrap import AppendedText

from accounts.models import MusicianProfile
from contact.models import Location
from photos.models import Image
from schedule.models import DateRange, Event, Show, Info


class DateForm(ModelForm):
    date_format = '%m/%d/%Y'
    time_format = '%I:%M %p'
    start = forms.SplitDateTimeField(label=_("Start"),
                                    input_date_formats=[date_format],
                                    input_time_formats=[time_format],
                                    widget=forms.SplitDateTimeWidget(
                                        time_format=time_format,
                                        date_format=date_format))
    end = forms.SplitDateTimeField(label=_("End"),
                                  required=False,
                                  input_date_formats=[date_format],
                                  input_time_formats=[time_format],
                                  widget=forms.SplitDateTimeWidget(
                                      time_format=time_format,
                                      date_format=date_format))
    def __init__(self, *args, **kwargs):
        kwargs.pop('user', None)
        super(DateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
              Div('start',css_class='col-md-6 left',),
              Div('end',css_class='col-md-6 right',css_id='end-div',),
              css_class='row no-gutter',
            ),
        )
    def clean(self):
        # allows for equal start and end dates
        # when dates are equal end datetime is not shown in forms and templates
        if self.cleaned_data['end'] and self.cleaned_data['start']:
            if self.cleaned_data['end'] < self.cleaned_data['start']:
                raise forms.ValidationError(_(u"The end time must be later than start time."))
        return self.cleaned_data
    def save(self):
        date = super(DateForm, self).save(commit=False)
        if not date.end:
            date.end = date.start
        if date.start and date.end:
            date.save()
        else:
            date = None
        return date

    class Meta:
        model = DateRange
        fields = ('start','end',)


class EventForm(ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.pop('user', None)
        super(EventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'visible',
        )

    class Meta:
        model = Event
        fields = ('visible',)

class UserSelectForm(ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.pop('user', None)
        super(UserSelectForm, self).__init__(*args, **kwargs)
        self.participants = Layout ('headliner', 'openers', 'venue',)

class ShowInfoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ShowInfoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'title',
            'headliner',
            'headliner_text',
            'openers',
            'openers_text',
            'venue',
            'venue_text',
            'description',
        )
        self.fields['headliner'].required = False

    def clean(self):
        # user must be a participant in the evnet or request
        isParticipant = False
        try:
            if self.cleaned_data.get('headliner').profile.user == self.user:
                isParticipant = True
        except:
            pass
        if self.cleaned_data.get('venue') == self.user:
            isParticipant = True
        else:
            for o in self.cleaned_data.get('openers'):
                if o.profile.user == self.user:
                    isParticipant = True
        if not isParticipant:
            raise forms.ValidationError(_(u"You must be a participant in this show"))
        if not self.cleaned_data.get('title') and not (self.cleaned_data.get('headliner') or self.cleaned_data.get('headliner_text')):
            raise forms.ValidationError(_(u"A Title or a Headliner is required"))
        if not self.cleaned_data.get('venue') and not self.cleaned_data.get('venue_text'):
            raise forms.ValidationError(_(u"A Venue is required"))
        return self.cleaned_data

    class Meta:
        model = Info
        fields = ('title','headliner','openers','venue','headliner_text','openers_text','venue_text','description',)
        widgets = {
          'description' : forms.Textarea(attrs={'rows': 2, 'cols': 19}),
        }
