from flask import Flask
from config import configure_all


app= Flask(__name__)

configure_all(app)


