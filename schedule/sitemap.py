from django.contrib.sitemaps import Sitemap

from schedule.models import Show

class ShowSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Show.objects.filter(visible=True)
