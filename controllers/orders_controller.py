from flask import jsonify

from db import db
from lib.authenticate import auth, auth_admin
from models.orders import Orders, order_schema, orders_schema
from util.reflection import populate_object


@auth_admin
def order_add(request):
    post_data = request.form if request.form else request.json

    new_order = Orders.new_order_obj()
    populate_object(new_order, post_data)
    try:
        db.session.add(new_order)
        db.session.commit()
    except:
        db.session.rollback
        return jsonify({"message": "unable to create order"}), 400

    return jsonify({"message": "order created", "results": order_schema.dump(new_order)}), 200


@auth
def orders_active(req):
    query = db.session.query(Orders).filter(Orders.active == True).all()

    if not query:
        return jsonify({"message": f'orders could not be found'}), 404

    return jsonify({"message": "orders found", "results": orders_schema.dump(query)}), 200


@auth
def orders_get_all(req):
    query = db.session.query(Orders).all()

    return jsonify({"message": "order found", "results": orders_schema.dump(query)}), 200


@auth
def order_by_id(req, order_id):
    query = db.session.query(Orders).filter(Orders.order_id == order_id).first()

    if not query:
        return jsonify({"message": f'order could not be found'}), 404

    return jsonify({"message": "order found", "results": order_schema.dump(query)}), 200


@auth_admin
def order_update(req, order_id):
    query = db.session.query(Orders).filter(Orders.order_id == order_id).first()
    post_data = req.form if req.form else req.get_json()

    populate_object(query, post_data)

    db.session.commit()
    return jsonify({'message': 'order updated', 'results': order_schema.dump(query)}), 200


@auth_admin
def order_delete(req, order_id):
    query = db.session.query(Orders).filter(Orders.order_id == order_id).first()

    if not query:
        return jsonify({"message": 'order could not be found'}), 404

    try:
        db.session.delete(query)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete order"})

    return jsonify({'message': 'record has been deleted'})
