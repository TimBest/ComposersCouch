from django.db.models import Q
from django.shortcuts import render

from accounts.models import Profile
from artist.models import ArtistProfile
from fan.models import FanProfile
from venue.models import VenueProfile
from composersCouch.utils import get_page


def search(request, template_name='search/search.html',
           ajax_template='autocomplete/search.html'):

    q = request.GET.get('q', '')
    context = {'q': q}

    if request.is_ajax():
        template_name = ajax_template
        queries = {}
        queries['artists'] = ArtistProfile.objects.filter(name__icontains=q)[:3]
        queries['venues'] = VenueProfile.objects.filter(name__icontains=q)[:3]
        queries['fans'] = FanProfile.objects.filter(
            Q(profile__user__first_name__icontains=q) |
            Q(profile__user__last_name__icontains=q)
        )[:3]
        context.update(queries)
    else:
        profiles = Profile.objects.filter(
            Q(artist_profile__name__icontains=q) |
            Q(venueProfile__name__icontains=q) |
            Q(user__first_name__icontains=q) |
            Q(user__last_name__icontains=q)
        )
        page_num = request.GET.get('page')
        context['profiles'] = get_page(page_num, profiles, 5)


    return render(request, template_name, context)
