"""
Marshmallow schemas can be used to serialize and deserialize models easily
"""

from feedback.extensions import ma
from feedback.surveys.models import Survey


class PICSurveySchema(ma.ModelSchema):

    def get_instance(self, data):
        """Overrides ModelSchema.get_instance with custom lookup fields"""
        lookup_cols = ['source_id']
        # print 'self.fields.keys()', self.fields.keys()
        filters = {
            key: data[key]
            for key in self.fields.keys() if key in lookup_cols
            }
        # print 'filters values', filters.values()
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
