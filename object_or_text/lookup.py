from django.db.models import ForeignKey, Transform
from django.db.models.loading import get_model


class Model(Transform):
    lookup_name = 'model'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)

        app_label, model_and_field_name = lhs.replace("\"", "").split('_')
        model_name, field_name = model_and_field_name.split('.')

        model = get_model(app_label, model_name)
        self.object_model = model._meta.get_field(field_name).object_model

        #model = get_model
        print lhs
        print lhs_params
        print rhs
        print rhs_params
        params = lhs_params + rhs_params
        return '%s <> %s' % (lhs, rhs), params



"""class Model(Transform):
    lookup_name = 'model'

    def as_sql(self, compiler, connection):
        lhs, params = compiler.compile(self.lhs)

        app_label, model_and_field_name = lhs.replace("\"", "").split('_')
        model_name, field_name = model_and_field_name.split('.')

        model = get_model(app_label, model_name)
        self.object_model = model._meta.get_field(field_name).object_model
        print self.object_model
        print lhs
        print params
        return "%s" % lhs, params

    @property
    def output_field(self):
        return ForeignKey(self.lhs.field.object_model)"""
