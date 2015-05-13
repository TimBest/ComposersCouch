from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return [
            'learn',
            'about',
            'team',
            'credit',
            'changelog',
            'pipeline',
            'privacy',
            'terms',
        ]

    def location(self, item):
        return reverse(item)
