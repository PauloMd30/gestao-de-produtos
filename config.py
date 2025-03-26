from routes import route_home, route_produto


def configure_all(app):
     configure_routes(app)



def configure_routes(app):
     app.register_blueprint(route_home)
     app.register_blueprint(route_produto, url_prefix="/produto")
    




