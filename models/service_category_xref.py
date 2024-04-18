from db import db

service_category_xref = db.Table(
    "ServicesCategoriesAssociation",
    db.Model.metadata,
    db.Column('service_id', db.ForeignKey('Services.service_id', ondelete='CASCADE'), primary_key=True),
    db.Column('category_id', db.ForeignKey('Categories.category_id', ondelete='CASCADE'), primary_key=True)
)
