# -*- coding: utf-8 -*-
from django.db import models
from django.forms import CharField
from django.utils.translation import ugettext_lazy as _

from annoying.functions import get_object_or_None
from object_or_text.widgets import ObjectOrTextWidget


class ObjectOrTextField(models.Field):
    def __init__(self, model, verbose_name=None, related_name=None, blank=False, null=True, max_length=False, *args, **kwargs):
        super(ObjectOrTextField, self).__init__(*args, **kwargs)
        self.model = model
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
            self.model,
            verbose_name= _("%s_object") % self.verbose_name,
            related_name= _("%s_object") % self.related_name,
            blank=self.blank,
            null=self.null,
            ).contribute_to_class(cls, "%s_object" % name)
        # when accessing the field by original model field name,
        # we'll manage tuples of country code, area code, and number
        setattr(cls, self.name, ObjectOrTextFieldCreator(self))

    def formfield(self, **kwargs):
        """ Specify form field and widget to be used on the forms """
        defaults = {
            'form_class': CharField,
            'widget': ObjectOrTextWidget,
        }
        kwargs.update(defaults)
        return super(ObjectOrTextField, self).formfield(**kwargs)

class ObjectOrTextFieldCreator(object):
    def __init__(self, field):
        self.field = field

    def __get__(self, obj, type=None):
        if obj is None:
            raise AttributeError('Can only be accessed via an instance.')
        text = obj.__dict__.get("%s_text" % self.field.name, None)
        object_id = obj.__dict__.get("%s_object_id" % self.field.name, None)
        if object_id:
            return get_object_or_None(self.field.model, pk=object_id)
        else:
            return text

    def __set__(self, obj, value):
        if isinstance(value, self.field.model):
            setattr(obj, "%s_object_id" % self.field.name, value.pk)
        else:
            setattr(obj, "%s_text" % self.field.name, value)


"""
class MultiKeyOrCharField(Field):
    fields = {
        'manytomany': ManyToManyField(),
        'char': CharField(),
    }
"""
