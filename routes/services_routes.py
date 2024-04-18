from flask import Blueprint, request
import controllers

services = Blueprint('services', __name__)


@services.route('/service', methods=['POST'])
def service_add():
    return controllers.service_add(request)


@services.route('/service/category', methods=['POST'])
def service_add_category():
    return controllers.service_add_category(request)


@services.route('/services', methods=['GET'])
def services_get_all():
    return controllers.services_get_all(request)


@services.route('/service/<service_id>', methods=['GET'])
def service_by_id(service_id):
    return controllers.service_by_id(request, service_id)


@services.route('/service/<service_id>', methods=['PUT'])
def service_update():
    return controllers.service_update(request)


@services.route('/service/category', methods=['DELETE'])
def service_remove_category():
    return controllers.service_remove_category(request)


@services.route('/service/delete/<service_id>', methods=['DELETE'])
def service_delete(service_id):
    return controllers.service_delete(request, service_id)
