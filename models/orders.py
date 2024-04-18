import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import marshmallow as ma

from .service_order_xref import service_order_xref


from db import db


class Orders(db.Model):
    __tablename__ = 'Orders'

    now_datetime = datetime.utcnow()

    order_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = db.Column(db.datetime(), default=now_datetime)

    services = db.relationship('Services', secondary=service_order_xref, back_populates='order', cascade='all,delete')
    users = db.relationship('Users', foreign_keys='[Users.order_id]', back_populates='order', cascade='all,delete')

    def __init__(self, timestamp):
        self.timestamp = timestamp


class OrdersSchema(ma.Schema):
    class Meta:
        fields = ['order_id', 'timestamp', 'user_id', 'services']
    services = ma.fields.Nested("ServicesSchema", many=True, exclude=['order'])


order_schema = OrdersSchema()
orders_schema = OrdersSchema(many=True)


class OrderIDSchema(ma.Schema):
    class Meta:
        fields = ['order_id', 'timestamp', 'user_id', 'services']
    services = ma.fields.Nested("ServicesSchema", many=True, exclude=['order'])


order_name_id_schema = OrderIDSchema()
orderies_name_id_schema = OrderIDSchema(many=True)
