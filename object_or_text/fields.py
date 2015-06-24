# -*- coding: utf-8 -*-
from django import forms
from django.db import models
from django.utils import six
from django.utils.encoding import smart_text

import ast

from annoying.functions import get_object_or_None
#from object_or_text.lookup import Model


_model_name = lambda name: ("%s_model" % name)
_text_name = lambda name: ("%s" % name)

class ObjectOrTextFormField(forms.CharField):

    def clean(self, value):
        try:
            return self.widget.autocomplete.model.objects.get(pk=value[0])
        except:
            return value[1]

class ObjectOrTextFieldCreator(object):
    def __init__(self, field):
        self.field = field
        self._model_name = _model_name(self.field.name)
        self._model_id_name = ("%s_id" % self._model_name)
        self._text_name = _text_name(self.field.name)

    def __get__(self, obj, type=None):
        if obj is None:
            raise AttributeError('Can only be accessed via an instance.')
        model = obj.__dict__.get(self._model_id_name, None)
        text = obj.__dict__.get(self._text_name, None)
        if model:
            return get_object_or_None(self.field.related_model, pk=model)
        else:
            return text

    def __set__(self, obj, value):
        print "__set__ %s" % value
        if isinstance(value, (long,int)):
            obj.__dict__[self._model_id_name] = value
            obj.__dict__[self._text_name] = value
            #print "pk of model: %s" % value
            print "pk of model: %s" % obj.__dict__.get(self._model_id_name, None)
        else:
            try:
                obj.__dict__[self._model_id_name] = int(value.pk)
                obj.__dict__[self._text_name] = int(value.pk)
                #print "model: %s" % value
                print "model: %s" % obj.__dict__.get(self._model_id_name, None)

            except AttributeError:
                obj.__dict__[self._model_name] = None
                obj.__dict__[self._text_name] = value
                #print "text: %s" % value
                print "text: %s" % obj.__dict__.get(self._text_name, None)



# keeping for migrations
class ModelOrTextField(models.Field):

    def __init__(self, related_model=None, *args, **kwargs):
        super(ModelOrTextField, self).__init__(*args, **kwargs)
        self.related_model = related_model

    def formfield(self, **kwargs):
        defaults = {'form_class': ObjectOrTextFormField,}
        defaults.update(kwargs)
        return super(ModelOrTextField, self).formfield(**defaults)

    def db_type(self, connection):
        return 'CharField'

class ModelField(models.ForeignKey):

    def formfield(self, **kwargs):
        defaults = {'form_class': ObjectOrTextFormField,}
        defaults.update(kwargs)
        return super(ModelField, self).formfield(**defaults)

    """def from_db_value(self, value, expression, connection, context):
        print "from_db_value %s" % value
        return value

    def to_python(self, value):
        print "TO PYTHON %s" % value
        return value

    def get_prep_value(self, value):
        print "get_prep_value %s" % value
        return value"""

    def db_type(self, connection):
        return 'ForeignKey'

#ModelOrTextField.register_lookup(Model)


class ObjectOrTextField(models.Field):

    def __init__(self, related_model, blank=False, null=True, max_length=254, *args, **kwargs):
        super(ObjectOrTextField, self).__init__(*args, **kwargs)
        self.related_model = related_model
        self.blank = blank
        self.null = null
        self.max_length = max_length

    def contribute_to_class(self, cls, name):
        self.name = name
        ModelOrTextField(
            max_length=self.max_length,
            blank=self.blank,
            null=self.null,
            ).contribute_to_class(cls, _text_name(name))
        ModelField(
            self.related_model,
            blank=True,
            null=True,
            ).contribute_to_class(cls, _model_name(name))
        # when accessing the field by original model field name,
        # we'll manage tuples of country code, area code, and number
        setattr(cls, self.name, ObjectOrTextFieldCreator(self))

    def formfield(self, **kwargs):
        defaults = {'form_class': ObjectOrTextFormField,}
        defaults.update(kwargs)
        return super(ObjectOrTextField, self).formfield(**defaults)

"""
class MultiKeyOrCharField(Field):
    fields = {
        'manytomany': ManyToManyField(),
        'char': CharField(),
    }
"""
