from flask import jsonify, request

from db import db
from lib.authenticate import auth, auth_admin
from models.categories import Categories
from models.orders import Orders
from models.scheduling import Scheduling, schedule_schema, schedules_schema
from util.reflection import populate_object


@auth_admin
def schedule_add(request):
    post_data = request.form if request.form else request.json

    new_schedule = Scheduling.new_schedule_obj()
    populate_object(new_schedule, post_data)

    db.session.add(new_schedule)
    db.session.commit()
    return jsonify({"message": "schedule created", "results": schedule_schema.dump(new_schedule)}), 200


@auth
def scheduling_get_all(req):
    query = db.session.query(Scheduling).all()

    return jsonify({"message": "scheduling found", "results": schedules_schema.dump(query)}), 200


@auth
def scheduling_active(req):
    query = db.session.query(Scheduling).filter(Scheduling.active == True).all()

    if not query:
        return jsonify({"message": f'schedule could not be found'}), 404

    return jsonify({"message": "schedule found", "results": schedules_schema.dump(query)}), 200


@auth_admin
def schedule_update(request, schedule_id):
    query = db.session.query(Scheduling).filter(Scheduling.schedule_id == schedule_id).first()
    post_data = request.form if request.form else request.get_json()
    populate_object(query, post_data)

    try:
        db.session.commit()
        return jsonify({'message': 'schedule updated', 'results': schedule_schema.dump(query)}), 200
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400


@auth_admin
def schedule_delete(req, schedule_id):
    query = db.session.query(Scheduling).filter(Scheduling.schedule_id == schedule_id).first()

    if not query:
        return jsonify({"message": 'schedule could not be found'}), 404

    try:
        db.session.delete(query)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete schedule"})

    return jsonify({'message': 'record has been deleted'})
