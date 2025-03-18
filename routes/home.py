from flask import Blueprint, render_template

route_home = Blueprint("home", __name__)

@route_home.route("/")
def home():
     return render_template("index.html")