from mongoengine import connect, Document, StringField, DateField
from dotenv import load_dotenv
import os

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Obter a URI de conexão do MongoDB
db_uri = os.getenv('DB_URI')  # A string completa de conexão

# Conectar ao MongoDB usando a URI
try:
    connect(host=db_uri)
    print("Conexão com MongoDB bem-sucedida!")
except Exception as e:
    print(f"Erro ao conectar com o MongoDB: {e}")

# Definir o modelo Produto
class Produto(Document):
    nome = StringField(required=True)
    marca = StringField(required=True)
    codigo_de_barras = StringField(required=True)
    data_de_validade = DateField()