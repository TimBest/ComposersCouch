from django.db import models
from django.utils.translation import ugettext as _


class Genre(models.Model):

    name =  models.CharField(_("name"), max_length=64)
    slug =  models.CharField(_("slug"), max_length=64)

    def __unicode__(self):
        return u'{0}'.format(self.name)

class Category(models.Model):

    name =  models.CharField(_("name"), max_length=64)
    slug =  models.CharField(_("slug"), max_length=64)
    genres = models.ManyToManyField(Genre, verbose_name=_("genres"),
                               related_name='categories')

    def __unicode__(self):
        return u'{0}'.format(self.name)
