from flask import jsonify

from db import db
from lib.authenticate import auth, auth_admin
from models.orders import Orders, order_schema, orders_schema
from util.reflection import populate_object


@auth_admin
def order_add(req):
    post_data = req.form if req.form else req.json

    fields = ['order_name']
    required_fields = ['order_name']

    values = {}

    for field in fields:
        field_data = post_data.get(field)
        if field_data in required_fields and not field_data:
            return jsonify({'message': f'(field) is required'}), 400

        values[field] = field_data

    new_order = Orders(values['order_name'])
    try:
        db.session.add(new_order)
        db.session.commit()
        query = db.session.query(Orders).filter(Orders.order_name == values['order_name']).first()
        values['order_id'] = query.order_id
        return jsonify({'message': 'order created', 'result': values}), 201
    except:
        db.session.rollback()
        return jsonify({'message': 'unable to create record'}), 400


@auth
def orders_get_all(req):
    query = db.session.query(Orders).all()

    return jsonify({"message": "order found", "results": orders_schema.dump(query)}), 200


@auth
def order_by_id(req, order_id):
    query = db.session.query(Orders).filter(Orders.order_id == order_id).all()

    if not query:
        return jsonify({"message": f'order could not be found'}), 404

    return jsonify({"message": "order found", "results": order_schema.dump(query)}), 200


@auth_admin
def order_update(req, order_id):
    query = db.session.query(Orders).filter(Orders.order_id == order_id).first()
    post_data = req.form if req.form else req.get_json()

    populate_object(query, post_data)

    try:
        db.session.commit()
        return jsonify({'message': 'order updated', 'results': {
            'order_id': query.order_id,
            'order_name': query.order_name
        }}), 200
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400
