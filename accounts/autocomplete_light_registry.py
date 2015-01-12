from django.contrib.auth.models import User

import autocomplete_light

from accounts.models import MusicianProfile


class MusicianProfileAutocomplete(autocomplete_light.AutocompleteModelTemplate):
    model = MusicianProfile
    attrs = {
        'placeholder': 'Search artists',
    }
    search_fields = ['^name',]

autocomplete_light.register(
    MusicianProfile,
    MusicianProfileAutocomplete,
    choice_template='autocomplete/_musician.html',
    autocomplete_template='autocomplete/_musicians.html',
)

class UserArtistAutocomplete(autocomplete_light.AutocompleteModelTemplate):
    model = User
    attrs = {
        'placeholder': 'Search artists',
    }
    search_fields = ['^profile__musicianProfile__name',]


    def choices_for_request(self):
        self.choices = self.choices.filter(profile_type='m')

        return super(UserArtistAutocomplete, self).choices_for_request()

autocomplete_light.register(
    MusicianProfile,
    MusicianProfileAutocomplete,
    choice_template='autocomplete/_musician.html',
    autocomplete_template='autocomplete/_musicians.html',
)

class UserAutocomplete(autocomplete_light.AutocompleteModelTemplate):
    model = User
    attrs = {
        'placeholder': 'Search users',
    }
    search_fields = ['^profile__musicianProfile__name','^profile__venueProfile__name','^first_name','^last_name',]

autocomplete_light.register(
    User,
    UserAutocomplete,
    choice_template='autocomplete/_user.html',
    autocomplete_template='autocomplete/_users.html',
)
