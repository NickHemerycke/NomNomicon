from flask import Flask, request, render_template, redirect, url_for, flash
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Recipe
from config import Config
from dotenv import find_dotenv, load_dotenv

# Load environment variables
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize DB & Migrations
db.init_app(app)
migrate = Migrate(app, db)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create tables if missing
with app.app_context():
    db.create_all()


# -----------------------------
# Routes (recipes + UI)
# -----------------------------
@app.route("/")
def home():
    if current_user.is_authenticated:
        appetizers = Recipe.query.filter_by(type="appetizer", user_id=current_user.id).all()
        lunch = Recipe.query.filter_by(type="lunch", user_id=current_user.id).all()
        dinner = Recipe.query.filter_by(type="dinner", user_id=current_user.id).all()
    else:
        appetizers, lunch, dinner = [], [], []
    return render_template("home.html", appetizers=appetizers, lunch=lunch, dinner=dinner)


@app.route("/upgrade-db")
def upgrade_db():
    from flask_migrate import upgrade
    upgrade()
    return "Database upgraded!"


@app.route("/list")
@login_required
def list():
    Recipes = Recipe.query.filter_by(selected=True, user_id=current_user.id).all()
    return render_template("list.html", Recipes=Recipes)


@app.route("/menu")
@login_required
def menu():
    appetizers = Recipe.query.filter_by(type="appetizer", user_id=current_user.id).all()
    lunch = Recipe.query.filter_by(type="lunch", user_id=current_user.id).all()
    dinner = Recipe.query.filter_by(type="dinner", user_id=current_user.id).all()
    selected = Recipe.query.filter_by(selected=True, user_id=current_user.id).all()
    return render_template(
        "menu.html", appetizers=appetizers, lunch=lunch, dinner=dinner, selected=selected
    )


@app.route("/add-to-menu", methods=["POST"])
@login_required
def add_to_menu():
    recipe_id = request.form.get("recipe_id")
    recipe = Recipe.query.filter_by(id=recipe_id, user_id=current_user.id).first()
    if recipe:
        recipe.selected = True
        db.session.commit()
        flash(f"{recipe.name} added to your menu!", "success")
    else:
        flash("Recipe not found or not yours.", "error")
    return redirect(url_for("menu"))


@app.route("/submit-recipe", methods=["POST"])
@login_required
def submit_recipe():
    category = request.form.get("category")
    dish_name = request.form.get("dish_name")
    ingredients = request.form.get("ingredients")

    if not category or not dish_name or not ingredients:
        flash("All fields are required!", "error")
        return redirect(url_for("home"))

    recipe = Recipe(
        type=category,
        name=dish_name,
        ingredients=ingredients,
        user_id=current_user.id
    )
    db.session.add(recipe)
    db.session.commit()

    flash("Recipe added successfully!", "success")
    return redirect(url_for("home"))


# -----------------------------
# Auth routes
# -----------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        if not name or not email or not password or not confirm:
            flash("All fields are required!", "error")
            return redirect(url_for("register"))
        if password != confirm:
            flash("Passwords do not match!", "error")
            return redirect(url_for("register"))
        if User.query.filter_by(email=email).first():
            flash("Email already registered!", "error")
            return redirect(url_for("register"))

        user = User(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Registration successful!", "success")
        return redirect(url_for("home"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Email and password are required.", "error")
            return redirect(url_for("login"))

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash(f"Welcome back, {user.name}!", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("home"))
        else:
            flash("Invalid email or password.", "error")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
