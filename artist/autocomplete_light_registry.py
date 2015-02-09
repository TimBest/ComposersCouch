import autocomplete_light

from models import Instrument


class InstrumentAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['^name',]
    widget_attrs={
        'placeholder': 'foo',
    },
    attrs={
        'placeholder': 'foo',
    },

autocomplete_light.register(Instrument, InstrumentAutocomplete, widget_attrs={
        'placeholder': 'foo',
    })
