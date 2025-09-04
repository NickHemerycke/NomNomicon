from flask import Flask, request, jsonify, render_template, redirect, session, url_for
from config import Config
from models import db, User

from os import environ as env

from dotenv import find_dotenv, load_dotenv

# Load environment variables from .env if present
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# -----------------------------
# Initialize Flask app
# -----------------------------
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/list')
def list():
    return render_template("list.html")

@app.route('/menu')
def menu():
    return render_template("menu.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
