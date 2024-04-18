from flask import Blueprint, request
import controllers

scheduling = Blueprint('scheduling', __name__)


@scheduling.route('/schedule', methods=['POST'])
def schedule_add():
    return controllers.schedule_add(request)


@scheduling.route('/scheduling', methods=['GET'])
def scheduling_get_all():
    return controllers.scheduling_get_all(request)


@scheduling.route('/schedule/<schedule_id>', methods=['GET'])
def schedule_by_id(schedule_id):
    return controllers.schedule_by_id(request, schedule_id)


@scheduling.route('/schedule/<schedule_id>', methods=['PUT'])
def schedule_update():
    return controllers.schedule_update(request)
