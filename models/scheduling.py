import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import marshmallow as ma

from db import db


class Scheduling(db.Model):
    __tablename__ = 'Scheduling'

    schedule_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    details = db.Column(db.String(),)
    timestamp = db.Column(db.datetime(), default=datetime.now(datetime.UTC))

    services = db.relationship('Services', foreign_keys='[Scheduling.service_id]', back_populates='scheduling')
    orders = db.relationship('Orders', foreign_keys='[Scheduling.order_id]', back_populates='scheduling')

    def __init__(self, details, timestamp):
        self.details = details
        self.timestamp = timestamp

    def new_schedule_obj():
        return Scheduling("", None)


class SchedulesSchema(ma.Schema):
    class Meta:
        fields = ['schedule_id', 'details', 'timestamp']


schedule_schema = SchedulesSchema()
schedules_schema = SchedulesSchema(many=True)
