import autocomplete_light

from models import Location, Zipcode


class LocationAutocomplete(autocomplete_light.AutocompleteModelBase):
    model = Location
    attrs = {
        'placeholder': '',
    }
    search_fields = ['^address_1', 'address_2', 'city', 'state',]
    limit_choices = 5

autocomplete_light.register(Location ,LocationAutocomplete)

class ZipcodeAutocomplete(autocomplete_light.AutocompleteModelBase):
    model = Zipcode
    attrs = {
        'placeholder': '',
    }
    search_fields = ['^code',]
    limit_choices = 5

autocomplete_light.register(Zipcode ,ZipcodeAutocomplete)
