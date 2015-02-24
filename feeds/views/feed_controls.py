from urlparse import urlparse
from django.core.urlresolvers import resolve, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.views.generic.edit import FormView

from feeds.forms import ZipcodeForm, AvailabilityForm, RemovePostForm, FollowForm
from feeds.models import Post
from feeds.urls import homeCategory, homeScope
from genres.models import Genre


class ZipcodeFormView(FormView):
    form_class = ZipcodeForm

    def get(self, request, *args, **kwargs):
        path = self.request.POST.get('path')
        return redirect(path)

    def form_invalid(self, form):
        path = self.request.POST.get('path')
        return redirect(path)

    def form_valid(self, form):
        try:
            zipcode = form.save(commit=False).zip_code.code
        except:
            zipcode = self.request.POST.get('zip_code-autocomplete')
        path = self.request.POST.get('path')
        path = resolve(urlparse(path)[2])
        url_name = path.url_name
        kwargs = path.kwargs
        if url_name == 'home':
            kwargs['scope'] = homeScope
            url_name = homeCategory
        if zipcode:
            kwargs['zipcode'] = zipcode
        if not kwargs.get('order') and url_name != 'updates':
            kwargs['order'] = 'expiring'
        url = reverse(url_name, kwargs=kwargs)
        return redirect(url)

zipcode = ZipcodeFormView.as_view()

class AvailabilityFormView(FormView):
    form_class = AvailabilityForm

    def get(self, request, *args, **kwargs):
        path = self.request.POST.get('path')
        return redirect(path)

    def form_invalid(self, form):
        path = self.request.POST.get('path')
        return redirect(path)

    def form_valid(self, form):
        date = form.cleaned_data['date']
        path = self.request.POST.get('path')
        path = resolve(urlparse(path)[2])
        url_name = path.url_name
        kwargs = path.kwargs
        if date:
            kwargs['year'] = date.year
            kwargs['month'] = date.month
            kwargs['day'] = date.day
        url = reverse(url_name, kwargs=kwargs)
        return redirect(url)

availability = AvailabilityFormView.as_view()

def genre(request, template_name='autocomplete/genre.html', ajax_template='autocomplete/genre.html'):
    q = request.GET.get('q', '')
    context = {'q': q}
    queries = {}
    queries['genres'] = Genre.objects.filter(Q(name__icontains=q) | Q(categories__name__icontains=q)).distinct().order_by('name')[:10]
    context.update(queries)

    if request.is_ajax():
        return render(request, ajax_template, context)
    else:
        path = request.GET.get('path', None)
        url = resolve(urlparse(path)[2])
        return url

@login_required
@require_POST
def follow(request):
    '''
    A view to follow other users
    '''
    data = request.POST.copy()
    form = FollowForm(data=data)

    if form.is_valid():
        target = User.objects.get(id=request.POST['target'])
        form.save(user=request.user,target=target)
    # TODO: use ?next=sdngjk instead
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
@require_POST
def remove_post(request):
    '''
    A view to follow other users
    '''
    data = request.POST.copy()
    form = RemovePostForm(data=data)

    if form.is_valid():
        post = Post.objects.get(id=request.POST['post'])
        form.save(user=request.user, post=post)
    # TODO: use ?next=sdngjk instead
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
