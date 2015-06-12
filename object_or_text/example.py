from django.db import models
from djutils import enum_as_choices
from core import DatePrecision, FuzzyDate
import forms

_precision_field_name = lambda name: "%s_precision"%name

class FuzzyDateCreator(object):
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
        self.precision_name = _precision_field_name(self.field.name)

    def __get__(self, obj, type=None):
        if obj is None:
            raise AttributeError('Can only be accessed via an instance.')

        date = obj.__dict__[self.field.name]
        if date is None: return None
        else:
            return FuzzyDate(date, precision=getattr(obj, self.precision_name))

    def __set__(self, obj, value):
        if isinstance(value, FuzzyDate):
            # fuzzy date is assigned: take over it's values
            obj.__dict__[self.field.name] = value.date
            setattr(obj, self.precision_name, value.precision)
        else:
            # standard python date: use the date portion and reset precision
            obj.__dict__[self.field.name] = self.field.to_python(value)
            # you could be tempted to reset the precision to "day" whenever
            # a user assigns a plain date - however, don't do this. when django
            # assigns to this while loading a row from the database, we want
            # to keep the precision that was already set!

class FuzzyDateField(models.DateField):
    """
    A field that stores a fuzzy date. See the module doc for more information.
    """
    def contribute_to_class(self, cls, name):
        # first, create a hidden "precision" field. It is *crucial* that this
        # field appears *before* the actual date field (i.e. self) in the
        # models _meta.fields - to achieve this, we need to change it's
        # creation_counter class variable.
        precision_field = models.IntegerField(
            choices=enum_as_choices(DatePrecision), editable=False,
            null=True, blank=True) # if not set, assume full precision
        # setting the counter to the same value as the date field itself will
        # ensure the precision field appear first - it is added first after all,
        # and when the date field is added later, it won't be sorted before it.
        precision_field.creation_counter = self.creation_counter
        cls.add_to_class(_precision_field_name(name), precision_field)

        # add the date field as normal
        super(FuzzyDateField, self).contribute_to_class(cls, name)

        # as we are not using SubfieldBase (see intro), we need to do it's job
        # ourselfs. we don't need to be generic, so don't use a metaclass, but
        # just assign the descriptor object here.
        setattr(cls, self.name, FuzzyDateCreator(self))

    def get_db_prep_save(self, value):
        if isinstance(value, FuzzyDate): value = value.date
        return super(FuzzyDateField, self).get_db_prep_save(value)

    def get_db_prep_lookup(self, lookup_type, value):
        if lookup_type == 'exact':
            return [self.get_db_prep_save(value)]
        elif lookup_type == 'in':
            return [self.get_db_prep_save(v) for v in value]
        else:
            # let the base class deal with the rest; some will work out fine,
            # like 'year', others will probably give unexpected results,
            # like 'range'.
            return super(FuzzyDateField, self).get_db_prep_lookup(lookup_type, value)

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.FuzzyDateField}
        defaults.update(kwargs)
        return super(FuzzyDateField, self).formfield(**defaults)

    # Although we need flatten_data for (oldforms) admin, we don't need to
    # implement it here, as the DateField baseclass will just call strftime on
    # our FuzzyDate object, which is something we support.
