import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db
from .service_category_xref import service_category_xref
from .service_order_xref import service_order_xref


class Services(db.Model):
    __tablename__ = 'Services'

    service_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(),)
    price = db.Column(db.Float(), nullable=False)
    quantity = db.Column(db.Integer(), nullable=True)

    categories = db.relationship('Categories', secondary=service_category_xref, back_populates='services')
    orders = db.relationship('Orders', secondary=service_order_xref, back_populates='services')

    def __init__(self, service_name, description, price, order_id, quantity):
        self.service_name = service_name
        self.description = description
        self.price = price
        self.quantity = quantity

    def new_service_obj():
        return Services("", "", 0, "", 0)


class ServicesSchema(ma.Schema):
    class Meta:
        fields = ['service_id', 'service_name', 'description', 'price', 'oder', 'categories', 'active']
    order = ma.fields.Nested("OrdersSchema", exclude=['services'])
    categories = ma.fields.Nested("CategoriesSchema", many=True, exclude=['services'])


service_schema = ServicesSchema()
services_schema = ServicesSchema(many=True)
