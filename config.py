# from routes import route_home
# from routes import route_produto
# from Database import db 
# from Database import Produto
# def configure_all(app):
#     configure_routes(app)
#     configure_db()


# def configure_routes(app):
#     app.register_blueprint(route_home)
#     app.register_blueprint(route_produto, url_prefix="/produto")
    


# # Função para configurar o banco de dados
# def configure_db():
#     if db.is_closed():
#         db.connect()
#     db.create_tables([Produto])

from routes import route_home, route_produto
from Database import db 
from Database import Produto

def configure_all(app):
    configure_routes(app)
    configure_db()

def configure_routes(app):
    app.register_blueprint(route_home)
    app.register_blueprint(route_produto, url_prefix="/produto")

def configure_db():
    if db.is_closed():
        db.connect()
    db.create_tables([Produto])
