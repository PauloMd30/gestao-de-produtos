from mongoengine import connect, Document, StringField, DateField, BooleanField
from dotenv import load_dotenv
import os
import certifi

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Obter a URI de conexão do MongoDB
db_uri = os.getenv('DB_URI')  # A string completa de conexão

# Conectar ao MongoDB usando a URI e o certificado SSL
try:
    # Conectar com MongoDB utilizando as opções SSL
    connect(
        host=db_uri, 
        tls=True,  # Certifique-se de que TLS está ativado
        tlsCAFile=certifi.where(),  # Usar o arquivo CA fornecido pelo certifi
        tlsAllowInvalidCertificates=True,  # Ignora certificados inválidos (usado em ambientes de desenvolvimento)
        tlsAllowInvalidHostnames=True  # Ignora erros de hostname no certificado
    )
    print("Conexão com MongoDB bem-sucedida!")
except Exception as e:
    print(f"Erro ao conectar com o MongoDB: {e}")

# Definir o modelo Produto
class Produto(Document):
    nome = StringField(required=True)
    marca = StringField(required=True)
    codigo_de_barras = StringField(required=True)
    data_de_validade = DateField()
    notificado = BooleanField(default=False) 
