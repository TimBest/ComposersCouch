
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from annoying.functions import get_object_or_None
from accounts.views import loginredirect
from composersCouch.utils import get_page
from utils import load_class

from photos.models import Image

from django.contrib.auth.models import User
username_field = 'username'

PHOTOS_IMAGES_ON_PAGE = getattr(settings, 'PHOTOS_IMAGES_ON_PAGE', 20)

PHOTOS_ON_PAGE = getattr(settings, 'PHOTOS_ON_PAGE', 20)

ImageForm = load_class(getattr(settings, 'PHOTOS_IMAGE_FORM', 'photos.forms.ImageForm'))


def get_images_queryset(self):
    images = Image.objects.all()
    self.e_context = dict()
    if 'tag' in self.kwargs:
        tag_instance = get_tag(self.kwargs['tag'])
        if tag_instance is None:
            raise Http404(_('No Tag found matching "%s".') % self.kwargs['tag'])
        self.e_context['tag'] = tag_instance
        images = TaggedItem.objects.get_by_model(images, tag_instance)
    if 'username' in self.kwargs:
        user = get_object_or_404(**{'klass': User, username_field: self.kwargs['username']})
        self.e_context['view_user'] = user
        images = images.filter(user=user)
    return images


class ImageListView(ListView):
    context_object_name = 'image_list'
    template_name = 'photos/image_list.html'
    paginate_by = getattr(settings, 'PHOTOS_IMAGES_ON_PAGE', 20)
    allow_empty = True

    get_queryset = get_images_queryset

    def get_context_data(self, **kwargs):
        context = super(ImageListView, self).get_context_data(**kwargs)
        context.update(self.e_context)
        return context


class ImageView(DetailView):
    context_object_name = 'image'
    template_name = 'photos/image.html'

    get_queryset = get_images_queryset

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(ImageView, self).get_context_data(**kwargs)
        image = context['image']

        base_qs = self.get_queryset()
        count = base_qs.count()
        img_pos = base_qs.filter(
            Q(order__lt=image.order)|
            Q(id__lt=image.id, order=image.order)
        ).count()
        next = None
        previous = None
        if count - 1 > img_pos:
            try:
                next = base_qs.filter(
                    Q(order__gt=image.order)|
                    Q(id__gt=image.id, order=image.order)
                )[0]
            except IndexError:
                pass
        if img_pos > 0:
            try:
                previous = base_qs.filter(
                    Q(order__lt=image.order)|
                    Q(id__lt=image.id, order=image.order)
                ).order_by('-order', '-id')[0]
            except IndexError:
                pass
        context['next'] = next
        context['previous'] = previous
        context.update(self.e_context)
        return context


class CreateImage(CreateView):
    template_name = 'photos/forms/image_form.html'
    model = Image
    form_class = ImageForm

    @method_decorator(login_required)
    @method_decorator(permission_required('%s.add_%s' % (Image._meta.app_label, Image.__name__.lower())))
    def dispatch(self, *args, **kwargs):
        return super(CreateImage, self).dispatch(*args, **kwargs)

    def get_form(self, form_class):
        return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return loginredirect(self.request, tab='photos')


def get_edit_image_queryset(self):
    if self.request.user.has_perm('%s.moderate_%s' % (Image._meta.app_label,  Image.__name__.lower())):
        return Image.objects.all()
    else:
        return Image.objects.filter(user=self.request.user)


class UpdateImage(UpdateView):
    template_name = 'photos/forms/image_edit_form.html'
    model = Image
    form_class = ImageForm

    get_queryset = get_edit_image_queryset

    @method_decorator(login_required)
    @method_decorator(permission_required('%s.change_%s' % (Image._meta.app_label,  Image.__name__.lower())))
    def dispatch(self, *args, **kwargs):
        return super(UpdateImage, self).dispatch(*args, **kwargs)


class DeleteImage(DeleteView):
    template_name = 'photos/image_delete.html'
    model = Image

    def get_success_url(self):
        return loginredirect(self.request, tab='photos')

    get_queryset = get_edit_image_queryset

    @method_decorator(login_required)
    @method_decorator(permission_required('%s.delete_%s' % (Image._meta.app_label,  Image.__name__.lower())))
    def dispatch(self, *args, **kwargs):
        return super(DeleteImage, self).dispatch(*args, **kwargs)

def ProfileImageView(extra_context,user):
    images = Image.objects.all()
    extra_context['paginate_by'] = getattr(settings, 'IMAGESTORE_IMAGES_ON_PAGE', 20)
    extra_context['image_list'] = images.filter(user=user)
    return extra_context

class ImageFormMixin(object):
    images_on_page = 4

    def get_context_data(self, **kwargs):
        context = super(ImageFormMixin, self).get_context_data(**kwargs)
        try:
            page_num = self.request.GET.get('page')
            images = Image.objects.filter(user=self.request.user)
            context['images'] = get_page(page_num, images, self.images_on_page)
        except:
            pass
        return context
