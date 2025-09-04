from models import db, User, Recipe
from flask import Flask, request, render_template, redirect, url_for, flash

from config import Config
from flask_migrate import Migrate

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
    appetizers = Recipe.query.filter_by(type="appetizer").all()
    lunch = Recipe.query.filter_by(type="lunch").all()
    dinner = Recipe.query.filter_by(type="dinner").all()
    return render_template("home.html", appetizers=appetizers, lunch=lunch, dinner=dinner)


@app.route('/list')
def list():
    return render_template("list.html")

@app.route('/menu')
def menu():
    recipes = Recipe.query.all()
    return render_template("menu.html", recipes=recipes)

@app.route('/submit-recipe', methods=['POST'])
def submit_recipe():
    category = request.form.get("category")
    dish_name = request.form.get("dish_name")
    ingredients = request.form.get("ingredients")

    if not category or not dish_name or not ingredients:
        flash("All fields are required!", "error")
        return redirect(url_for("home"))

    recipe = Recipe(type=category, name=dish_name, ingredients=ingredients)
    db.session.add(recipe)
    db.session.commit()

    flash("Recipe added successfully!", "success")
    return redirect(url_for("home"))

migrate = Migrate(app, db)




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
