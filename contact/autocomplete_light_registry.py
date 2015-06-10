import autocomplete_light as al

from models import Location, Zipcode


class LocationAutocomplete(al.AutocompleteModelBase):
    model = Location
    attrs = {
        'placeholder': '',
    }
    search_fields = ['^address_1', 'address_2', 'city', 'state',]
    limit_choices = 5

al.register(Location ,LocationAutocomplete)

class ZipcodeAutocomplete(al.AutocompleteModelBase):
    model = Zipcode
    attrs = {
        'placeholder': '',
    }
    search_fields = ['^code',]
    limit_choices = 5

al.register(Zipcode ,ZipcodeAutocomplete)
