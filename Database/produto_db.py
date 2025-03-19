from peewee import MySQLDatabase
from dotenv import load_dotenv
import os

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Obter as variáveis de ambiente
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = int(os.getenv('DB_PORT'))

# Configurar a conexão com o banco de dados
db = MySQLDatabase(
    database=db_name,
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port
)