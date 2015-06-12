# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

PHONE_COUNTRY_CODE_CHOICES = getattr(settings, "PHONE_COUNTRY_CODE_CHOICES", (
    ("+44", _("United Kingdom (+44)")),
    ("+49", _("Germany (+49)")),
    ("+370", _("Lithuania (+370)")),
    ))

class ForgienKeyOrCharField(models.Field):
    def __init__(self, othermodel, verbose_name=None, related_name=None, blank=False, null=True, max_length=False, *args, **kwargs):
        super(ForgienKeyOrCharField, self).__init__(*args, **kwargs)
        self.othermodel = othermodel
        self.verbose_name = verbose_name
        self.related_name = related_name
        self.blank = blank
        self.null = null
        self.max_length = max_length

    def contribute_to_class(self, cls, name):
        self.name = name
        if self.verbose_name is None and name:
            self.verbose_name = name.replace('_', ' ')
        # creating three model fields on the fly
        models.CharField(
            _("%s_text") % self.verbose_name,
            max_length=self.max_length,
            blank=self.blank,
            null=self.null,
            ).contribute_to_class(cls, "%s_text" % name)
        models.ForeignKey(
            self.othermodel,
            verbose_name= _("%s") % self.verbose_name,
            related_name= _("%s") % self.related_name,
            blank=self.blank,
            null=self.null,
            ).contribute_to_class(cls, "%s" % name)
        # when accessing the field by original model field name,
        # we'll manage tuples of country code, area code, and number
        setattr(cls, self.name, ForgienKeyOrCharFieldCreator(self))

class ForgienKeyOrCharFieldCreator(object):
    def __init__(self, field):
        self.field = field

    def __get__(self, obj, type=None):
        if obj is None:
            raise AttributeError('Can only be accessed via an instance.')
        text = obj.__dict__.get("%s_text" % self.field.name, None)
        model = obj.__dict__.get("%s_id" % self.field.name, None)
        return (model and text) and (model, text) or None

    def __set__(self, obj, value):
        if isinstance(value, tuple) and len(value) == 2:
            setattr(obj, "%s_text" % self.field.name, value[0])
            setattr(obj, "%s" % self.field.name, value[1])


"""
class MultiKeyOrCharField(Field):
    fields = {
        'manytomany': ManyToManyField(),
        'char': CharField(),
    }
"""
