from flask import jsonify, request

from db import db
from lib.authenticate import auth, auth_admin
from models.services import Services, service_schema, services_schema
from models.categories import Categories
from util.reflection import populate_object


@auth_admin
def service_add(request):
    post_data = request.form if request.form else request.json

    new_service = Services.new_service_obj()
    populate_object(new_service, post_data)

    try:
        db.session.add(new_service)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback
        return jsonify({"message": "unable to create record"}), 400

    return jsonify({"message": "service created", "results": service_schema.dump(new_service)}), 200


@auth_admin
def service_add_category(request):
    post_data = request.json
    service_id = post_data.get('service_id')
    category_id = post_data.get('category_id')

    service_query = db.session.query(Services).filter(Services.service_id == service_id).first()
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    service_query.categories.append(category_query)
    db.session.commit()
    return jsonify({'message': 'category assigned to service', 'results': service_schema.dump(service_query)})


@auth_admin
def service_remove_category(request):
    post_data = request.json
    service_id = post_data.get('service_id')
    category_id = post_data.get('category_id')

    service_query = db.session.query(Services).filter(Services.service_id == service_id).first()
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    service_query.categories.remove(category_query)
    db.session.commit()
    return jsonify({'message': 'category removed from service'})


@auth
def services_get_all(req):
    query = db.session.query(Services).all()

    return jsonify({"message": "services found", "results": services_schema.dump(query)}), 200


@auth
def service_by_id(req, service_id):
    query = db.session.query(Services).filter(Services.service_id == service_id).all()

    if not query:
        return jsonify({"message": f'service could not be found'}), 404

    return jsonify({"message": "service found", "results": service_schema.dump(query)}), 200


@auth_admin
def service_update(request, service_id):
    query = db.session.query(Services).filter(Services.service_id == service_id).first()
    post_data = request.form if request.form else request.get_json()
    populate_object(query, post_data)

    try:
        db.session.commit()
        return jsonify({'message': 'service updated', 'results': service_schema.dump(query)}), 200
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400


@auth_admin
def service_delete(req, service_id):
    query = db.session.query(Services).filter(Services.service_id == service_id).first()

    if not query:
        return jsonify({"message": 'service could not be found'}), 404

    try:
        db.session.delete(query)
        db.session.commit()

    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete service"})

    return jsonify({'message': 'record has been deleted'})
