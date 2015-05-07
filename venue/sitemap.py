from django.contrib.sitemaps import Sitemap

from venue.models import VenueProfile

class VenueSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return VenueProfile.objects.filter(profile__has_owner=True)
