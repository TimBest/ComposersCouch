from django.shortcuts import render

from accounts.models import MusicianProfile, VenueProfile


def search(request, template_name='search/search.html', ajax_template='autocomplete/search.html'):

    if request.is_ajax():
        template_name = ajax_template

    q = request.GET.get('q', '')
    context = {'q': q}

    queries = {}
    queries['musicians'] = MusicianProfile.objects.filter(name__icontains=q)[:3]
    queries['venues'] = VenueProfile.objects.filter(name__icontains=q)[:3]

    context.update(queries)
    return render(request, template_name, context)
