from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import resolve, reverse
from django.http import Http404
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView

from datetime import datetime
from datetime import timedelta

from annoying.functions import get_object_or_None
from composersCouch.utils import get_page
from contact.utils import get_location
from feeds.forms import ZipcodeForm, AvailabilityForm
from genres.models import Category
from schedule.models import Show


login_required_m = method_decorator(login_required)

class ZipcodeMixin(object):

    def get_context_data(self, **kwargs):
        context = super(ZipcodeMixin, self).get_context_data(**kwargs)
        context['locationForm'] = ZipcodeForm()
        context['zipcode'] = get_location(self.request, self.kwargs.get('zipcode'), 'code')
        return context

class GenreMixin(object):
    path_to_genre = 'profile__genre__slug'

    def filter_by_genre(self, genres, qs):
        if genres:
            genre_qs = []
            for i, genre in enumerate(genres):
                if i==0:
                    genre_qs = self.model.objects.filter(**{self.path_to_genre:genre.slug})
                else:
                    genre_qs = genre_qs | self.model.objects.filter(**{self.path_to_genre:genre.slug})
            return qs.distinct() & genre_qs.distinct()
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
    default_order = "Default"
    orders = {}
    filters = None

    def get_order(self, qs):
        order = self.orders.get(self.kwargs.get('order'))
        if order and qs:
            return qs.order_by(order)
        else:
            return qs

    def get_posts(self):
        if self.filters:
            return self.model.objects.filter(**self.filters)
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
        page_num = self.request.GET.get('page')
        queryset = self.get_queryset()
        if context.get('genres') and queryset:
            queryset = self.filter_by_genre(context['genres'], queryset)
        context['object_list'] = get_page(page_num, queryset, self.paginate_by)

        return context

    def paginate_queryset(self, queryset, page_size):
        """
        Paginate the queryset, if needed.
        """
        paginator = self.get_paginator(queryset, page_size, allow_empty_first_page=self.get_allow_empty())
        page = self.kwargs.get('page') or self.request.GET.get('page') or 1
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404(_(u"Page is not 'last', nor can it be converted to an int."))
        try:
            page = paginator.page(page_number)
            return (paginator, page, page.object_list, page.has_other_pages())
        except:
            return (None, None, queryset, False)


class AvailabilityMixin(object):
    model = None

    @login_required_m
    def dispatch(self, request, *args, **kwargs):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        try:
            self.start_date = datetime(int(year), int(month), int(day))
        except:
            now = timezone.now()
            self.kwargs['year'] = now.year
            self.kwargs['month'] = now.month
            self.kwargs['day'] = now.day
            url_name = resolve(self.request.path_info).url_name
            response = redirect(reverse(url_name, kwargs=self.kwargs))
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
        context['year'] = self.kwargs.get('year')
        context['month'] = self.kwargs.get('month')
        context['day'] = self.kwargs.get('day')
        return context
