from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

class FeedsSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return [
            ['requests',           {'order':'expiring', 'for':'band','scope':'any-distance'}],
            ['requests',           {'order':'expiring', 'for':'venue','scope':'any-distance'}],
            ['shows',              {'order':'upcoming', 'scope':'any-distance'}],
            ['artists',            {'order':'all', 'scope':'any-distance'}],
            ['available_artists',  {'order':'all', 'year':'2015','month':'32','day':'32'}],
            ['venues',             {'order':'all', 'scope':'any-distance'}],
            ['available_venues',   {'order':'all', 'year':'2015','month':'32','day':'32'}],
            ['updates',            {'order':'latest', 'scope':'any-distance'}],
        ]

    def location(self, item):
        return reverse(item[0], kwargs=item[1])
