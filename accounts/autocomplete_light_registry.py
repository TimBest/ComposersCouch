from django.contrib.auth.models import User

import autocomplete_light

from accounts.models import MusicianProfile


class MusicianProfileAutocomplete(autocomplete_light.AutocompleteModelTemplate):
    model = MusicianProfile
    attrs = {
        'placeholder': '',
    }
    search_fields = ['^name',]

autocomplete_light.register(
    MusicianProfile,
    MusicianProfileAutocomplete,
    choice_template='autocomplete/_musician.html',
    autocomplete_template='autocomplete/_musicians.html',
)

class UserAutocomplete(autocomplete_light.AutocompleteModelTemplate):
    model = User
    attrs = {
        'placeholder': '',
    }
    search_fields = ['^profile__musicianProfile__name','^profile__venueProfile__name','^first_name','^last_name',]

autocomplete_light.register(
    User,
    UserAutocomplete,
    choice_template='autocomplete/_user.html',
    autocomplete_template='autocomplete/_users.html',
)
