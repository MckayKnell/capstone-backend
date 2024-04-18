from flask import Blueprint, request
import controllers

orders = Blueprint('orders', __name__)


@orders.route('/order', methods=['POST'])
def order_add():
    return controllers.order_add(request)


@orders.route('/orders', methods=['GET'])
def orders_get_all():
    return controllers.orders_get_all(request)


@orders.route('/order/<order_id>', methods=['GET'])
def order_by_id(order_id):
    return controllers.order_by_id(request, order_id)


@orders.route('/order/<order_id>', methods=['PUT'])
def order_update():
    return controllers.order_update(request)
