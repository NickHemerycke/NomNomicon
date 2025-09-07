from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    # Relationship to recipes
    recipes = db.relationship("Recipe", backref="author", lazy=True)

    # Password helpers
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Recipe(db.Model):
    __tablename__ = "recipe"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)  # appetizer, lunch, dinner
    name = db.Column(db.String(200), nullable=False)
    ingredients = db.Column(db.Text, nullable=True)
    selected = db.Column(db.Boolean, default=False)

    # Link recipe to the user who created it
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
