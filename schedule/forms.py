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

from annoying.functions import get_object_or_None
from artist.models import ArtistProfile
from contact.models import Location
from photos.models import Image
from schedule.models import DateRange, Event, Show, Info


class DateForm(ModelForm):
    date_format = '%m/%d/%Y'
    time_format = '%I:%M %p'
    start = forms.SplitDateTimeField(label=_("Start"),
            input_date_formats=[date_format], input_time_formats=[time_format],
            widget=forms.SplitDateTimeWidget(time_format=time_format,
                                             date_format=date_format))
    end = forms.SplitDateTimeField(label=_("End"), required=False,
          input_date_formats=[date_format], input_time_formats=[time_format],
          widget=forms.SplitDateTimeWidget(time_format=time_format,
                                           date_format=date_format))
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
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
        start = self.cleaned_data.get('start')
        end = self.cleaned_data.get('end')
        if (start and end) and end < start:
            raise forms.ValidationError(_(u"The end time must be later than start time."))
        if start:
            event = get_object_or_None(Event, show__date__start=start, calendar=self.user.calendar)
            if event:
                raise forms.ValidationError(_(u"A participant in this event has a conflict. Try another date/time."))

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

class ShowInfoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ShowInfoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['headliner'].required = False
        self.fields['headliner_text'].label = "Headliner"
        self.fields['openers_text'].help_text = "Separate artists by commas"
        self.fields['openers_text'].label = "Openers"
        self.fields['venue_text'].label = "Venue"
        self.helper.layout = Layout('title', 'headliner_text', 'headliner',
            'openers_text', 'openers', 'venue_text', 'venue','description',)

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
            raise forms.ValidationError(_(u"You must be a participant in this show."))
        if not self.cleaned_data.get('title') and not self.cleaned_data.get('headliner_text'):
            raise forms.ValidationError(_(u"A Title or a Headliner is required."))
        if not self.cleaned_data.get('venue_text'):
            raise forms.ValidationError(_(u"A Venue is required."))
        return self.cleaned_data

    class Meta:
        model = Info
        fields = ('title','headliner','openers','venue','headliner_text',
                  'openers_text','venue_text','description',)
        widgets = {
            'description' : forms.Textarea(attrs={'rows': 2, 'cols': 19}),
            'headliner_text' : autocomplete_light.TextWidget('ArtistProfileAutocomplete'),
            'openers_text' : autocomplete_light.TextWidget('ArtistProfileAutocomplete'),
            'venue_text' : autocomplete_light.TextWidget('UserAutocomplete'),
        }
