from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        info_items = ['learn', 'about', 'team', 'credit',]
        auth_items = ['login', 'signup',]
        return info_items + auth_items

    def location(self, item):
        return reverse(item)
