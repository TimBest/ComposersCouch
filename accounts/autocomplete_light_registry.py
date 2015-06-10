from django.contrib.auth.models import User

import autocomplete_light as al

from artist.models import ArtistProfile


class ArtistProfileAutocomplete(al.AutocompleteModelTemplate):
    model = ArtistProfile
    attrs = {
        'placeholder': '',
    }
    search_fields = ['^name',]
    limit_choices = 5

al.register(
    ArtistProfile,
    ArtistProfileAutocomplete,
    choice_template='autocomplete/artist.html',
)

class UserAutocomplete(al.AutocompleteModelTemplate):
    model = User
    attrs = {
        'placeholder': '',
    }
    search_fields = ['^profile__artist_profile__name','^profile__venueProfile__name','^first_name','^last_name',]
    limit_choices = 5

    def choices_for_request(self):
        self.choices = self.choices.exclude(id=-1)
        return super(UserAutocomplete, self).choices_for_request()

al.register(
    User,
    UserAutocomplete,
    choice_template='autocomplete/user.html',
)

class UserArtistAutocomplete(al.AutocompleteModelTemplate):
    model = User
    attrs = {
        'placeholder': '',
    }
    search_fields = ['^profile__artist_profile__name',]
    limit_choices = 5


    def choices_for_request(self):
        self.choices = self.choices.filter(profile__profile_type='m')
        return super(UserArtistAutocomplete, self).choices_for_request()

al.register(
    User,
    UserArtistAutocomplete,
    choice_template='autocomplete/user.html',
)
