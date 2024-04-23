from db import db

service_order_xref = db.Table(
    "ServicesOrdersAssociation",
    db.Model.metadata,
    db.Column('service_id', db.ForeignKey('Services.service_id', ondelete='CASCADE'), primary_key=True),
    db.Column('order_id', db.ForeignKey('Orders.order_id', ondelete='CASCADE'), primary_key=True)
)
