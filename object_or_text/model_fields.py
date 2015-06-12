from django.db import models
from django.forms import CharField

from annoying.functions import get_object_or_None
from object_or_text.widgets import ObjectOrTextWidget

_is_model_field_name = lambda name: ("%s_is_model" % name)

class ObjectOrTextFieldCreator(object):
    """
    An equivalent to Django's default attribute descriptor class (enabled via
    the SubfieldBase metaclass, see module doc for details). However, instead
    of callig to_python() on our FuzzyDateField class, it stores the two
    different party of a fuzzy date, the date and the precision, separately, and
    updates them whenever something is assigned. If the attribute is read, it
    builds the FuzzyDate instance "on-demand" with the current data.
    """
    def __init__(self, field):
        self.field = field
        self.is_model_field_name = _is_model_field_name(self.field.name)

    def __get__(self, obj, type=None):
        if obj is None:
            raise AttributeError('Can only be accessed via an instance.')

        text = obj.__dict__.get(self.field.name, None)
        is_object = obj.__dict__.get(self.is_model_field_name, None)
        if is_object and text:
            return get_object_or_None(self.field.object, pk=text)
        else:
            return text

    def __set__(self, obj, value):
        if value:
            if not isinstance(value, basestring):
                obj.__dict__[self.field.name] = value[0]
                setattr(obj, self.is_model_field_name, value[1])
            else:
                obj.__dict__[self.field.name] = self.field.to_python(value)

class ObjectOrTextField(models.Field):
    """
    A field that stores a fuzzy date. See the module doc for more information.
    """
    def __init__(self, objet, max_length=254, *args, **kwargs):
        self.object = object
        kwargs['max_length'] = max_length
        super(ObjectOrTextField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        self.name = name
        # first, create a hidden "is_object" field.
        is_model = models.BooleanField(default=False, editable=False,)
        cls.add_to_class(_is_model_field_name(name), is_model)

        # add the text field as normal
        super(ObjectOrTextField, self).contribute_to_class(cls, name)

        setattr(cls, self.name, ObjectOrTextFieldCreator(self))

    """def get_db_prep_save(self, value):
        if isinstance(value, FuzzyDate): value = value.date
        return super(ObjectOrTextField, self).get_db_prep_save(value)"""

    """def get_db_prep_lookup(self, lookup_type, value):
        if lookup_type == 'exact':
            return [self.get_db_prep_save(value)]
        elif lookup_type == 'in':
            return [self.get_db_prep_save(v) for v in value]
        else:
            # let the base class deal with the rest; some will work out fine,
            # like 'year', others will probably give unexpected results,
            # like 'range'.
            return super(ObjectOrTextField, self).get_db_prep_lookup(lookup_type, value)"""

    def formfield(self, **kwargs):
        defaults = {
            'form_class': CharField,
            'widget': ObjectOrTextWidget,
        }
        defaults.update(kwargs)
        return super(ObjectOrTextField, self).formfield(**defaults)

"""
class MultiKeyOrCharField(Field):
    fields = {
        'manytomany': ManyToManyField(),
        'char': CharField(),
    }
"""
