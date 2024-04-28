from flask import Blueprint, request
import controllers

scheduling = Blueprint('scheduling', __name__)


@scheduling.route('/schedule', methods=['POST'])
def schedule_add():
    return controllers.schedule_add(request)


@scheduling.route('/scheduling', methods=['GET'])
def scheduling_get_all():
    return controllers.scheduling_get_all(request)


@scheduling.route('/scheduling/active', methods=['GET'])
def scheduling_active():
    return controllers.scheduling_active(request)


@scheduling.route('/schedule/<schedule_id>', methods=['PUT'])
def schedule_update(schedule_id):
    return controllers.schedule_update(request, schedule_id)


@scheduling.route('/schedule/delete/<schedule_id>', methods=['DELETE'])
def schedule_delete(schedule_id):
    return controllers.schedule_delete(request, schedule_id)
