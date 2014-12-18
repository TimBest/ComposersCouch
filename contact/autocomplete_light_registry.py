import autocomplete_light

from models import Location, Zipcode


class LocationAutocomplete(autocomplete_light.AutocompleteModelBase):
    model = Location
    search_fields = ['^address_1', 'address_2', 'city', 'state',]

autocomplete_light.register(Location ,LocationAutocomplete)

class ZipcodeAutocomplete(autocomplete_light.AutocompleteModelBase):
    model = Zipcode
    search_fields = ['^code',]

autocomplete_light.register(Zipcode ,ZipcodeAutocomplete)
