# app.py
from flask import Flask, render_template, request, redirect
from models import db, Dish, Ingredient

app = Flask(__name__)

# Configuring the database URI and disabling track modifications
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/nom_nomicon.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Create all tables in the database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    # Fetching dishes by category
    starters = Dish.query.filter_by(category='starter').all()
    mains = Dish.query.filter_by(category='main').all()
    desserts = Dish.query.filter_by(category='dessert').all()
    return render_template('menu.html', starters=starters, mains=mains, desserts=desserts)

@app.route('/add_dish', methods=['POST'])
def add_dish():
    name = request.form['name']
    category = request.form['category']
    ingredients = request.form.get('ingredients', '').split(',')

    # Add the new dish to the database
    new_dish = Dish(name=name, category=category)
    db.session.add(new_dish)
    db.session.commit()

    # Add ingredients to the dish
    for ing in ingredients:
        db.session.add(Ingredient(name=ing.strip(), dish=new_dish))
    db.session.commit()

    return redirect('/')

@app.route('/delete_dish/<int:id>')
def delete_dish(id):
    dish = Dish.query.get_or_404(id)
    db.session.delete(dish)
    db.session.commit()
    return redirect('/')

@app.route('/ingredients')
def ingredient_list():
    dishes = Dish.query.all()
    all_ingredients = {ing.name for dish in dishes for ing in dish.ingredients}
    return render_template('ingredients.html', ingredients=all_ingredients)

if __name__ == '__main__':
    app.run(debug=True)
