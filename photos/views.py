from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView

from .models import Image
from .forms import ImageForm
from accounts.views import loginredirect
from composersCouch.utils import get_page


def get_images_queryset(self):
    images = Image.objects.all()
    self.e_context = dict()
    return images

class ImageView(DetailView):
    context_object_name = 'image'
    template_name = 'photos/image.html'

    get_queryset = get_images_queryset

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

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
