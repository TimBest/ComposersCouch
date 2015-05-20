from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView

from .models import Image
from .forms import ImageForm
from annoying.functions import get_object_or_None
from accounts.views import loginredirect
from composersCouch.utils import get_page


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

veiw_image = ImageView.as_view()

class CreateImage(CreateView):
    template_name = 'photos/forms_image_form.html'
    model = Image
    form_class = ImageForm

    def get_form(self, form_class):
        return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return loginredirect(self.request, tab='photos')

create_image = login_required(CreateImage.as_view())


class UpdateImage(UpdateView):
    template_name = 'photos/forms_image_form.html'
    model = Image
    form_class = ImageForm

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)

    def get_success_url(self):
        kwargs= {'username':self.request.user.username, 'tab':'photos'}
        return reverse('redirectToProfile', kwargs=kwargs)

update_image = login_required(UpdateImage.as_view())

class DeleteImage(DeleteView):
    template_name = 'photos/image_delete.html'
    model = Image

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)

    def get_success_url(self):
        kwargs= {'username':self.request.user.username, 'tab':'photos'}
        return reverse('redirectToProfile', kwargs=kwargs)

delete_image = login_required(DeleteImage.as_view())

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
