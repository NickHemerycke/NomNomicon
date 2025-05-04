from flask import Flask, request, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dish.db'
db = SQLAlchemy(app)

# Model: Dish (note the PascalCase naming convention)
class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appetizer = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Boolean, default=False)

# Home route
@app.route('/')
@app.route('/dishes')
def home():
    dishes = Dish.query.all()  # Fetch all dishes from the database
    return render_template('index.html', dishes=dishes)  # Pass dishes to template

# Add a new dish route
@app.route('/add', methods=['POST'])
def add():
    appetizer = request.form.get('appetizer')  # Get the 'appetizer' value from the form
    new_dish = Dish(appetizer=appetizer)  # Create a new dish instance
    db.session.add(new_dish)  # Add the new dish to the session
    db.session.commit()  # Commit the session to save the dish in the database
    return redirect('/')  # Redirect back to the home page

# Mark dish as complete
@app.route('/complete/<int:dish_id>')
def complete(dish_id):
    dish = Dish.query.get(dish_id)  # Find the dish by its ID
    dish.complete = not dish.complete  # Toggle the 'complete' field
    db.session.commit()  # Commit the changes to the database
    return redirect('/')  # Redirect to the home page

# Delete a dish
@app.route('/delete/<int:dish_id>')
def delete(dish_id):
    dish = Dish.query.get(dish_id)  # Find the dish by its ID
    db.session.delete(dish)  # Delete the dish
    db.session.commit()  # Commit the changes to the database
    return redirect('/')  # Redirect to the home page

# Ingredients page route
@app.route('/ingredients')
def ingredients():
    return render_template('ingredients.html')  # Render the ingredients page

# Menu page route
@app.route('/menu')
def menu():
    return render_template('menu.html')  # Render the menu page

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create all the tables in the database
    app.run(debug=True)  # Run the app in debug mode
