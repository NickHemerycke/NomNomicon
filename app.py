from flask import Flask, request, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dish.db'
db = SQLAlchemy(app)


class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    meal_type = db.Column(db.String(80), nullable=False)
    addToMenu = db.Column(db.Boolean, default=False)

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False)

    dish = db.relationship('Dish', backref=db.backref('ingredients', cascade='all, delete-orphan'))


@app.route('/')
@app.route('/dishes')
def home():
    appetizers = Dish.query.filter_by(meal_type='appetizer').all()
    lunches = Dish.query.filter_by(meal_type='lunch').all()
    dinners = Dish.query.filter_by(meal_type='dinner').all()
    return render_template('index.html', appetizers=appetizers, lunches=lunches, dinners=dinners)  

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('dish_name')
    meal_type = request.form.get('meal_type')
    ingredient_list = request.form.getlist('ingredients')  # Get all inputs named "ingredients"

    new_dish = Dish(name=name, meal_type=meal_type)
    db.session.add(new_dish)
    db.session.flush()  # To get the ID before commit

    for ingredient_name in ingredient_list:
        if ingredient_name.strip():
            db.session.add(Ingredient(name=ingredient_name.strip(), dish_id=new_dish.id))

    db.session.commit()
    return redirect('/')
 


@app.route('/addToMenu/<int:dish_id>')
def addToMenu(dish_id):
    dish = Dish.query.get(dish_id)  
    dish.addToMenu = not dish.addToMenu  
    db.session.commit()  
    return redirect('/')  


@app.route('/delete/<int:dish_id>')
def delete(dish_id):
    dish = Dish.query.get(dish_id)  
    db.session.delete(dish)  
    db.session.commit() 
    return redirect('/') 


@app.route('/ingredients')
def ingredients():
    # Get ingredients from dishes that are added to the menu
    dishes_on_menu = Dish.query.filter_by(addToMenu=True).all()

    # Flatten list of all ingredients from those dishes
    all_ingredients = []
    for dish in dishes_on_menu:
        all_ingredients.extend([ingredient.name for ingredient in dish.ingredients])

    return render_template('ingredients.html', ingredients=all_ingredients)



@app.route('/menu')
def menu():
    menu_items = Dish.query.filter_by(addToMenu=True).all()
    return render_template('menu.html', menu_items=menu_items) 

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)  
