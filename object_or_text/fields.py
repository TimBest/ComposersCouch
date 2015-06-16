# -*- coding: utf-8 -*-
from django.db import models
from django import forms

from annoying.functions import get_object_or_None
from object_or_text.widgets import ObjectOrTextWidget


_field_name = lambda name: ("%s" % name)
_is_model_field_name = lambda name: ("%s_is_model" % name)

class ObjectOrTextField(models.Field):
    def __init__(self, model, blank=False, null=True, max_length=False, *args, **kwargs):
        super(ObjectOrTextField, self).__init__(*args, **kwargs)
        self.model = model
        self.blank = blank
        self.null = null
        self.max_length = max_length

    def contribute_to_class(self, cls, name):
        self.name = name
        models.CharField(
            max_length=self.max_length,
            blank=self.blank,
            null=self.null,
            ).contribute_to_class(cls, _field_name(name))
        models.BooleanField(
            default=False, editable=False,
        ).contribute_to_class(cls, _is_model_field_name(name))
        # when accessing the field by original model field name,
        # we'll manage tuples of country code, area code, and number
        setattr(cls, self.name, ObjectOrTextFieldCreator(self))


    def to_python(self, value):
        if value in (None, ''):
            return None
        return value

    def formfield(self, **kwargs):
        """ Specify form field and widget to be used on the forms """
        defaults = {
            'form_class': forms.MultiValueField,
            'widget': ObjectOrTextWidget,
        }
        kwargs.update(defaults)
        return super(ObjectOrTextField, self).formfield(**kwargs)

class ObjectOrTextFieldCreator(object):
    def __init__(self, field):
        self.field = field
        self.is_model_field_name = _is_model_field_name(self.field.name)

    def __get__(self, obj, type=None):
        if obj is None:
            raise AttributeError('Can only be accessed via an instance.')
        text = obj.__dict__.get(self.field.name, None)
        is_object = obj.__dict__.get(self.is_model_field_name, None)
        if is_object and text:
            return get_object_or_None(self.field.model, pk=text)
        else:
            return text

    def __set__(self, obj, value):
        obj.__dict__[self.field.name] = self.field.to_python(value)

"""
class MultiKeyOrCharField(Field):
    fields = {
        'manytomany': ManyToManyField(),
        'char': CharField(),
    }
"""
