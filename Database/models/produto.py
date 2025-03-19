from peewee import Model, CharField, DateField
from Database.produto_db import db 


class Produto(Model):
     nome = CharField()
     marca = CharField()
     codigo_de_barras = CharField()
     data_de_validade = DateField()

     class Meta:
         database = db

