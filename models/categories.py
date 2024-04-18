import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db
from .service_category_xref import service_category_xref


class Categories(db.Model):
    __tablename__ = 'Categories'

    category_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    time = db.Column(db.Int(), nullable=False)
    extensions = db.Column(db.Boolean(), nullable=False)

    services = db.relationship('Services', secondary=service_category_xref,
                               back_populates='categories')

    def __init__(self, time, extensions):
        self.time = time
        self.extensions = extensions


class CategoriesSchema(ma.Schema):
    class Meta:
        fields = ['category_id', 'time', 'extensions', 'services']
    services = ma.fields.Nested("ServicesSchema", many=True, exclude=['categories'])


category_schema = CategoriesSchema()
categories_Schema = CategoriesSchema(many=True)
