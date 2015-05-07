from django.contrib.sitemaps import Sitemap

from artist.models import ArtistProfile

class ArtistSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return ArtistProfile.objects.filter(profile__has_owner=True)
