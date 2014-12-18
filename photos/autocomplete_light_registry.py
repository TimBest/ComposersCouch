from __future__ import unicode_literals
import autocomplete_light

autocomplete_light.register(
    Tag,
    search_fields=['^name']
)
