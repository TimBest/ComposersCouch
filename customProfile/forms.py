from django.contrib.auth.models import User

from autocomplete_light import ModelForm

from accounts.models import Profile
from artist.models import ArtistProfile
from venue.models import VenueProfile


class ArtistProfileForm(ModelForm):

    def __init__(self, *args, **kwargs):
        try:
            required = kwargs.pop('required')
        except:
            required = True
        super(ArtistProfileForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = required

    class Meta:
        model = ArtistProfile
        fields = ('name',)


class VenueProfileForm(ModelForm):

    def __init__(self, *args, **kwargs):
        try:
            required = kwargs.pop('required')
        except:
            required = True
        super(VenueProfileForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = required

    class Meta:
        model = VenueProfile
        fields = ('name',)

class UserForm(ModelForm):

    def __init__(self, *args, **kwargs):
        try:
            required = kwargs.pop('required')
        except:
            required = True
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = required
        self.fields['last_name'].required = required

    class Meta:
        model = User
        fields = ('first_name', 'last_name')

class UsernameForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(UsernameForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = "www.composerscouch.com/slug/"
        self.fields['username'].label = "Slug"
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ('email', 'username',)

class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = ('genre',)
