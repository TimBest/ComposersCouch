import autocomplete_light as al

from .models import Genre


class GenreAutocomplete(al.AutocompleteModelBase):
    search_fields = ['^name','^categories__name']
    attrs = {
        'placeholder': '',
    }
    order_by = ['name']
    limit_choices = 5

    def choices_for_request(self):
        """
        Return a queryset based on :py:attr:`choices` using options
        :py:attr:`split_words`, :py:attr:`search_fields` and
        :py:attr:`limit_choices`.
        """
        assert self.choices is not None, 'choices should be a queryset'
        assert self.search_fields, 'autocomplete.search_fields must be set'
        q = self.request.GET.get('q', '')
        exclude = self.request.GET.getlist('exclude')
        conditions = self._choices_for_request_conditions(q, self.search_fields)
        return self.order_choices(self.choices.filter(
            conditions).exclude(pk__in=exclude).distinct())[0:self.limit_choices]

al.register(Genre, GenreAutocomplete,  distinct=True)
