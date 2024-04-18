import routes


def register_blueprints(app):
    app.register_blueprint(routes.auth)
    app.register_blueprint(routes.services)
    app.register_blueprint(routes.categories)
    app.register_blueprint(routes.orders)
    app.register_blueprint(routes.users)
    app.register_blueprint(routes.scheduling)
