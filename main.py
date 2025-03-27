from flask import Flask
from config import configure_all


app= Flask(__name__, template_folder='templates')


configure_all(app)

