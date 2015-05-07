from django.contrib.sitemaps import Sitemap

from fan.models import FanProfile

class FanSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return FanProfile.objects.filter(profile__has_owner=True)
