from mongoengine import Document, StringField, DateField

# Definir o modelo do Produto com mongoengine
class Produto(Document):
    nome = StringField(required=True)
    marca = StringField(required=True)
    codigo_de_barras = StringField(required=True)
    data_de_validade = DateField()