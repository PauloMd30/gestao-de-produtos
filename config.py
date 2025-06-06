from routes import route_home, route_produto

def configure_all(app):
    # Defina explicitamente a pasta de templates
    app.template_folder = 'templates'
    
    # Configurar rotas
    configure_routes(app)

def configure_routes(app):
    # Registrar os blueprints
    app.register_blueprint(route_home)
    app.register_blueprint(route_produto, url_prefix="/produto")





