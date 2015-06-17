# -*- coding: utf-8 -*-
from django import forms
from django.db import models
from django.utils import six
from django.utils.encoding import smart_text

import ast

from annoying.functions import get_object_or_None


_field_name = lambda name: ("%s" % name)
_is_model_field_name = lambda name: ("%s_is_model" % name)

class ObjectOrTextFormField(forms.CharField):

    def clean(self, value):
        if value:
            if value[1]:
                return self.widget.autocomplete.model.objects.get(pk=value[0])
            else:
                return value[0]
        else:
            return None

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
        if value:
            try:
                list = ast.literal_eval(value)
                obj.__dict__[self.field.name] = list[0]
                obj.__dict__[self.is_model_field_name] = list[1]
            except:
                if isinstance(value, six.string_types) or value is None:
                    obj.__dict__[self.field.name] = value
                    obj.__dict__[self.is_model_field_name] = False
                else:
                    obj.__dict__[self.field.name] = value.pk
                    obj.__dict__[self.is_model_field_name] = True

class CharField(models.CharField):

    def formfield(self, **kwargs):
        #defaults = {'form_class': ObjectOrTextFormField,}
        defaults = {'form_class': ObjectOrTextFormField,}
        defaults.update(kwargs)
        return super(CharField, self).formfield(**defaults)


    def to_python(self, value):
        if isinstance(value, six.string_types) or value is None:
            return "[u'%s', False]" % smart_text(value)
        else:
            return "[u'%s', True]" % smart_text(value.pk)

class ObjectOrTextField(models.Field):

    def __init__(self, model, blank=False, null=True, max_length=254, *args, **kwargs):
        super(ObjectOrTextField, self).__init__(*args, **kwargs)
        self.model = model
        self.blank = blank
        self.null = null
        self.max_length = max_length

    def contribute_to_class(self, cls, name):
        self.name = name
        CharField(
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

"""
class MultiKeyOrCharField(Field):
    fields = {
        'manytomany': ManyToManyField(),
        'char': CharField(),
    }
"""
