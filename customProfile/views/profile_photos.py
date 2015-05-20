from composersCouch.utils import get_page
from customProfile.views import ArtistProfileView, FanProfileView, VenueProfileView


class PhotosMixin(object):
    def get_context_data(self, **kwargs):
        context = super(PhotosMixin, self).get_context_data(**kwargs)
        page_num = self.request.GET.get('page')
        images = self.user.images.all()
        context['images'] = get_page(page_num, images, 24)
        return context

class ArtistPhotosView(PhotosMixin, ArtistProfileView):
    template_name = 'artist/photos.html'
artist_photos = ArtistPhotosView.as_view()

class FanPhotosView(PhotosMixin, FanProfileView):
    template_name = 'fan/photos.html'
fan_photos = FanPhotosView.as_view()

class VenuePhotosView(PhotosMixin, VenueProfileView):
    template_name = 'venue/photos.html'
venue_photos = VenuePhotosView.as_view()
