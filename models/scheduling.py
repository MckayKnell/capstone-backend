import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import marshmallow as ma

from db import db


class Scheduling(db.Model):
    __tablename__ = 'Scheduling'

    schedule_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    details = db.Column(db.String(),)
    timestamp = db.Column(db.DateTime(), default=datetime.now())
    active = db.Column(db.Boolean(), default=True)
    service_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Services.service_id"))
    order_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Orders.order_id"))

    services = db.relationship('Services', back_populates='scheduling')
    order = db.relationship('Orders', back_populates='scheduling')

    def __init__(self, details, timestamp, active):
        self.details = details
        self.timestamp = timestamp
        self.active = active

    def new_schedule_obj():
        return Scheduling("", datetime.now(), True)


class SchedulesSchema(ma.Schema):
    class Meta:
        fields = ['schedule_id', 'details', 'timestamp', 'active']


schedule_schema = SchedulesSchema()
schedules_schema = SchedulesSchema(many=True)
