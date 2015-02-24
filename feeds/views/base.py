from datetime import datetime, timedelta, time
from django.core.urlresolvers import resolve, reverse
from django.shortcuts import redirect, render
from django.utils import timezone

from composersCouch.utils import get_page
from contact.utils import get_location
from feeds.forms import ZipcodeForm, AvailabilityForm
from genres.models import Category


class ZipcodeMixin(object):
    def get_zipcode(self):
        return self.kwargs.get('zipcode')

    def get_context_data(self, **kwargs):
        context = super(ZipcodeMixin, self).get_context_data(**kwargs)
        context['zipcodeForm'] = ZipcodeForm()
        context['zipcode'] = get_location(self.request, self.get_zipcode(), 'code')
        return context

class GenreMixin(object):
    path_to_genre = 'profile__genre__id'

    def filter_by_genre(self, genres, qs):
        if genres:
            genre_qs = []
            for i, genre in enumerate(genres):
                if i==0:
                    genre_qs = self.modelManager.filter(**{self.path_to_genre:genre})
                else:
                    genre_qs = genre_qs | self.modelManager.filter(**{self.path_to_genre:genre})
            return qs & genre_qs
        else:
            return qs

    def get_context_data(self, **kwargs):
        context = super(GenreMixin, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(popular=True)
        context['more_categories'] = Category.objects.filter(popular=False)

        category = self.request.GET.getlist('genre')
        my_genres = self.request.GET.get('my-genres')
        if self.request.user.is_authenticated() and my_genres :
            self.path_to_genre = 'profile__genre'
            context['my_genres'] = my_genres
        else:
            context['category'] = category
        return context

class FeedMixin(GenreMixin, ZipcodeMixin):
    modelManager = None

    def get_order(self, qs):
        return qs

    def get_default_order(self):
        return "default"

    def get_posts(self):
        return []

    def get_context_data(self, **kwargs):
        context = super(FeedMixin, self).get_context_data(**kwargs)
        context['scope'] = self.kwargs.get('scope', 'all')

        page_num = self.request.GET.get('page')
        posts = self.get_posts()
        if posts:
            posts = self.get_order(posts)
            if context.get('genres'):
                posts = self.filter_by_genre(context['genres'], posts)
        context['posts'] = get_page(page_num, posts, 25)
        if not self.kwargs.get('order'):
          context['order'] = self.get_default_order()
        return context

class AvailabilityMixin(object):
    model = None

    def dispatch(self, request, *args, **kwargs):
        year = kwargs.get('year')
        month = kwargs.get('month')
        day = kwargs.get('day')
        try:
            self.start_date = datetime(int(year), int(month), int(day))
        except:
            now = timezone.now()
            kwargs['year'] = now.year
            kwargs['month'] = now.month
            kwargs['day'] = now.day
            url_name = resolve(self.request.path_info).url_name
            response = redirect(reverse(url_name, kwargs=kwargs))
            response['Location'] += '?' + self.request.GET.urlencode()
            return response
        self.end_date = self.start_date + timedelta(1)
        return super(AvailabilityMixin, self).dispatch(request, *args, **kwargs)

    def get_exclude(self, start, end, **kwargs):
        return {
            'profile__user__calendar__events__show__date__start__lt' : end,
            'profile__user__calendar__events__show__date__end__gte'  : start
        }

    def get_context_data(self, **kwargs):
        context = super(AvailabilityMixin, self).get_context_data(**kwargs)
        context['date'] = self.start_date
        context['availabilityForm'] = AvailabilityForm()
        return context
