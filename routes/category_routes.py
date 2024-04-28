from flask import Blueprint, request
import controllers

categories = Blueprint('categories', __name__)


@categories.route('/category', methods=['POST'])
def category_add():
    return controllers.category_add(request)


@categories.route('/categories', methods=['GET'])
def categories_get_all():
    return controllers.categories_get_all(request)


@categories.route('/categories/active', methods=['GET'])
def categories_active():
    return controllers.categories_active(request)


@categories.route('/category/<category_id>', methods=['PUT'])
def category_update(category_id):
    return controllers.category_update(request, category_id)


@categories.route('/category/delete/<category_id>', methods=['DELETE'])
def category_delete(category_id):
    return controllers.category_delete(request, category_id)
