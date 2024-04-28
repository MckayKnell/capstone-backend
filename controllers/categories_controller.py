from flask import jsonify

from db import db
from lib.authenticate import auth, auth_admin
from models.categories import Categories, category_schema, categories_Schema
from util.reflection import populate_object


@auth_admin
def category_add(req):
    post_data = req.form if req.form else req.json

    new_category = Categories.new_category_obj()
    populate_object(new_category, post_data)

    try:
        db.session.add(new_category)
        db.session.commit()
    except:
        db.session.rollback
        return jsonify({"message": "unable to create record"}), 400

    return jsonify({"message": "new_category created", "results": category_schema.dump(new_category)}), 200


@auth
def categories_get_all(req):
    query = db.session.query(Categories).all()

    return jsonify({"message": "categories found", "results": categories_Schema.dump(query)}), 200


@auth
def categories_active(req):
    query = db.session.query(Categories).filter(Categories.active == True).all()

    if not query:
        return jsonify({"message": f'category could not be found'}), 404

    return jsonify({"message": "categories found", "results": categories_Schema.dump(query)}), 200


@auth_admin
def category_update(req, category_id):
    query = db.session.query(Categories).filter(Categories.category_id == category_id).first()
    post_data = req.form if req.form else req.get_json()
    populate_object(query, post_data)

    try:
        db.session.commit()
        return jsonify({'message': 'category updated', 'results': category_schema.dump(query)}), 200
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400


@auth_admin
def category_delete(req, category_id):
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not category_query:
        return jsonify({'message': ' category does not exist'}), 400

    try:
        db.session.delete(category_query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({'message': 'unable to delete category'})

    return ({'message': 'category deleted'})
