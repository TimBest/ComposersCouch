# -*- coding: utf-8 -*-
from django import forms
from django.db import models
from django.utils import six
from django.utils.encoding import smart_text

import ast

from annoying.functions import get_object_or_None
#from object_or_text.lookup import Model


_model_name = lambda name: ("%s" % name)
_text_name = lambda name: ("%s_text" % name)

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
        self._text_name = _text_name(self.field.name)

    def __get__(self, obj, type=None):
        if obj is None:
            raise AttributeError('Can only be accessed via an instance.')
        model = obj.__dict__.get(("%s_id" % self.field.name), None)
        text = obj.__dict__.get(self._text_name, None)
        if model:
            return get_object_or_None(self.field.related_model, pk=model)
        else:
            return text

    def __set__(self, obj, value):
        if value:
            try:
                list = ast.literal_eval(value)
                obj.__dict__[self.field.name] = list[0]
                obj.__dict__[self.is_model_field_name] = list[1]
                print "LIST: %s" % value
            except:
                if isinstance(value, six.string_types) or value is None:
                    print "TEXT: %s" % value
                    obj.__dict__[self.field.name] = value
                    obj.__dict__[self.is_model_field_name] = False
                else:
                    print "MODEL: %s" % value
                    obj.__dict__[self.field.name] = value.pk
                    obj.__dict__[self.is_model_field_name] = True

class ModelOrTextField(models.Field):

    def __init__(self, related_model=None, *args, **kwargs):
        super(ModelOrTextField, self).__init__(*args, **kwargs)
        self.related_model = related_model

    def formfield(self, **kwargs):
        #defaults = {'form_class': ObjectOrTextFormField,}
        defaults = {'form_class': ObjectOrTextFormField,}
        defaults.update(kwargs)
        return super(ModelOrTextField, self).formfield(**defaults)

    #def from_db_value(self, value, expression, connection, context):
    #    if isinstance(value, six.string_types) or value is None:
    #        return smart_text(value)
    #    else:
    #        return smart_text(value.pk)

    #def to_python(self, value):
    #    if isinstance(value, six.string_types) or value is None:
    #        return "[u'%s', False]" % smart_text(value)
    #    else:
    #        return "[u'%s', True]" % smart_text(value.pk)

    #def get_prep_value(self, value):
    #    print value
    #    if isinstance(value, six.string_types) or value is None:
    #        return smart_text(value)
    #    else:
    #        return smart_text(value.pk)

    #def get_internal_type(self):
    #    return 'CharField'


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
            related_model = self.related_model,
            blank=self.blank,
            null=self.null,
            ).contribute_to_class(cls, _text_name(name))
        models.ForeignKey(
            self.related_model,
            blank=True,
            null=True,
            ).contribute_to_class(cls, _model_name(name))
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
