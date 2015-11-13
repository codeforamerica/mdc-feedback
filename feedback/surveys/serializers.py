"""
Marshmallow schemas can be used to serialize and deserialize models easily
"""

from flask import current_app

from feedback.extensions import ma, db
from feedback.surveys.models import Survey

from marshmallow import fields
from sqlalchemy import inspect
from pprint import pprint


class DataLoader:
    """A class that deduplicates raw data dictionaries,
        and then attempts to serialize them,
            either returning successfully validated models
            or reporting deserialization errors
    """
    def __init__(self, schema):
        self.schema = schema
        self.raw_data = []

    def add(self, data, many=False):
        """adds data to a raw data set() object
        """
        if not many:
            data = (data,)
        for d in data:
            if d not in self.raw_data:
                self.raw_data.append(d)

    def slice_and_add(self, data):
        """adds data to the raw data set, but only the subset of keys used by
        the serialization schema
        """
        keys = []
        for name, field in self.schema.fields.items():
            if field.load_from:
                keys.append(field.load_from)
            else:
                keys.append(name)
        sliced = {k:data[k] for k in keys if k in data}
        self.add(sliced)

    def log_errors(self, errors):
        for i, error in errors.items():
            problematic_datum = self.raw_data[i]
            for key, message in error.items():
                bad_input = problematic_datum[key]
                current_app.logger.error(
                    "DESERIALIZATIONERROR: '{field}': '{value}', {message}".format(
                        field=key,
                        value=bad_input,
                        message=message))

    def log_success(self, total, new, existing):
        current_app.logger.debug(
            "DESERIALIZED: {total} {cls} instances, {new} new, {existing} existing".format(
                total=total,
                cls=self.schema.opts.model.__name__,
                new=new,
                existing=existing
                ))

    def save_models_or_report_errors(self):
        """Tries to load data using the schema.
        If there are errors, it will log them.
        If there are no errors, it will save the models and return them

        Returns the models that were NOT already in the DB.
        """
        new = 0
        existing = 0
        total = 0
        new_models = []
        models, errors = self.schema.load(
            self.raw_data,
            many=True,
            session=db.session)

        if errors:
            self.log_errors(errors)
        else:
            for m in models:
                if inspect(m).persistent:
                    existing += 1
                else:
                    new += 1
                    new_models.append(m)
                db.session.add(m)
            db.session.commit()
            self.log_success(len(models), new, existing)
            return new_models


class PICSurveySchema(ma.ModelSchema):
    """ Our Scheme for the surveys at the PIC.
    Based on the Survey model
    """
    def get_instance(self, data):
        """Overrides ModelSchema.get_instance with custom lookup fields"""
        lookup_cols = ['source_id']
        filters = {
            key: data[key]
            for key in self.fields.keys() if key in lookup_cols
            }
        if None not in filters.values():
            return self.session.query(
                self.opts.model
            ).filter_by(
                **filters
            ).first()
        return None

    class Meta:
        model = Survey

pic_schema = PICSurveySchema()
