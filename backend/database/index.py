from flask import Blueprint, render_template

Index = Blueprint("index", __name__)

@Index.route('/')
def index():
    return render_template("index.html")
