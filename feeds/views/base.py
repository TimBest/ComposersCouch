from datetime import datetime, timedelta, time
from django.core.urlresolvers import resolve, reverse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.generic import ListView

from annoying.functions import get_object_or_None
from composersCouch.utils import get_page
from contact.utils import get_location
from feeds.forms import ZipcodeForm, AvailabilityForm
from genres.models import Category
from schedule.models import Show


class ZipcodeMixin(object):
    def get_zipcode(self):
        return self.kwargs.get('zipcode', None)

    def get_context_data(self, **kwargs):
        context = super(ZipcodeMixin, self).get_context_data(**kwargs)
        context['zipcodeForm'] = ZipcodeForm()
        context['zipcode'] = get_location(self.request, self.get_zipcode(), 'code')
        return context

class GenreMixin(object):
    path_to_genre = 'profile__genre__slug'

    def filter_by_genre(self, genres, qs):
        if genres:
            genre_qs = []
            for i, genre in enumerate(genres):
                if i==0:
                    genre_qs = self.modelManager.filter(**{self.path_to_genre:genre.slug})
                else:
                    genre_qs = genre_qs | self.modelManager.filter(**{self.path_to_genre:genre.slug})
            return qs & genre_qs
        else:
            return qs

    def get_context_data(self, **kwargs):
        context = super(GenreMixin, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(popular=True)
        context['more_categories'] = Category.objects.filter(popular=False)

        category_slug = self.request.GET.get('genre')
        my_genres = self.request.GET.get('my-genres')
        if self.request.user.is_authenticated() and my_genres :
            context['my_genres'] = my_genres
            context['genres'] = self.request.user.profile.genre.all()
        else:
            context['category'] = category_slug
            category = get_object_or_None(Category, slug=category_slug)
            if category:
                context['genres'] = category.genres.all()
        return context

class FeedMixin(GenreMixin, ZipcodeMixin, ListView):
    object_list = []
    model = Show
    template_name = 'feeds/show_list.html'
    paginate_by = 15
    default_order = "default"

    def get_order(self, qs):
        return qs

    def get_posts(self):
        return self.model.objects.all()

    def get_queryset(self):
        queryset = self.get_posts()
        queryset = self.get_order(queryset)
        return queryset

    def get_scope(self, **kwargs):
        context = {}
        context['scope'] = self.kwargs.get('scope', 'all')
        if context['scope'] == "any-distance":
            context['distance'] = "any distance"
        elif context['scope'] == "50":
            context['distance'] = "50 miles"
        return context

    def get_context_data(self, **kwargs):
        context = super(FeedMixin, self).get_context_data(**kwargs)
        context.update(self.get_scope())
        context['feedType'] = self.feedType
        context['order'] = self.kwargs.get('order', self.default_order)

        if context.get('genres') and context.get('object_list'):
            context['object_list'] = self.filter_by_genre(context['genres'], context['object_list'])
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
