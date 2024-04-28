import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from models.users import Users
import marshmallow as ma

from .service_order_xref import service_order_xref


from db import db


class Orders(db.Model):
    __tablename__ = 'Orders'

    order_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = db.Column(db.DateTime(), default=datetime.now())
    active = db.Column(db.Boolean(), default=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"))
    notes = db.Column(db.String())

    services = db.relationship('Services', secondary=service_order_xref, back_populates='order', cascade='all')
    user = db.relationship('Users', foreign_keys='[Orders.user_id]', back_populates='order', cascade='all')
    scheduling = db.relationship('Scheduling', back_populates='order', cascade='all')

    def __init__(self, timestamp, active, notes):
        self.timestamp = timestamp
        self.active = active
        self.notes = notes

    def new_order_obj():
        return Orders(datetime.now(), True, "")


class OrdersSchema(ma.Schema):
    class Meta:
        fields = ['order_id', 'timestamp', 'user_id', 'services', 'active', 'notes']
    services = ma.fields.Nested("ServicesSchema", many=True, exclude=['order'])


order_schema = OrdersSchema()
orders_schema = OrdersSchema(many=True)


class OrderIDSchema(ma.Schema):
    class Meta:
        fields = ['order_id', 'timestamp', 'user_id', 'services', 'active']
    services = ma.fields.Nested("ServicesSchema", many=True, exclude=['order'])


order_name_id_schema = OrderIDSchema()
orderies_name_id_schema = OrderIDSchema(many=True)
