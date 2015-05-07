from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

class AuthViewSitemap(Sitemap):
    priority = 0.9
    changefreq = 'monthly'

    def items(self):
        return ['login', 'signup',]

    def location(self, item):
        return reverse(item)
