import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db
from .service_category_xref import service_category_xref


class Categories(db.Model):
    __tablename__ = 'Categories'

    category_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_name = db.Column(db.String(), nullable=False, unique=True)
    time = db.Column(db.String(), nullable=False)
    extensions = db.Column(db.Boolean(), nullable=False)
    active = db.Column(db.Boolean(), default=True)

    services = db.relationship('Services', secondary=service_category_xref,
                               back_populates='categories')

    def __init__(self, category_name, time, extensions, active):
        self.category_name = category_name
        self.time = time
        self.extensions = extensions
        self.active = active

    def new_category_obj():
        return Categories("", "", "", "")


class CategoriesSchema(ma.Schema):
    class Meta:
        fields = ['category_id', 'category_name', 'time', 'extensions', 'services', 'active']
    services = ma.fields.Nested("ServicesSchema", many=True, exclude=['categories'])


category_schema = CategoriesSchema()
categories_Schema = CategoriesSchema(many=True)
