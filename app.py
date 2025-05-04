from flask import Flask, request, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dish.db'
db = SQLAlchemy(app)


class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appetizer = db.Column(db.String(200), nullable=False)
    addToMenu = db.Column(db.Boolean, default=False)

# Home route
@app.route('/')
@app.route('/dishes')
def home():
    dishes = Dish.query.all()  
    return render_template('index.html', dishes=dishes)  

# Add a new dish route
@app.route('/add', methods=['POST'])
def add():
    appetizer = request.form.get('appetizer')  
    new_dish = Dish(appetizer=appetizer)  
    db.session.add(new_dish)  
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
    return render_template('ingredients.html')  


@app.route('/menu')
def menu():
    return render_template('menu.html')  

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)  
