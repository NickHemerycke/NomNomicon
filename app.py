from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, login_manager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

bcrypt = Bcrypt(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dish.db'
app.config['SECRET_KEY'] = 'mysecret'  # For sessions
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    meal_type = db.Column(db.String(80), nullable=False)
    addToMenu = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('dishes', lazy=True))


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False)

    dish = db.relationship('Dish', backref=db.backref('ingredients', cascade='all, delete-orphan'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except:
            return 'There was an issue registering your account'

    return render_template('register.html')




@app.route('/')
@app.route('/dishes')
@login_required
def home():
    appetizers = Dish.query.filter_by(meal_type='appetizer', user_id=current_user.id).all()
    lunches = Dish.query.filter_by(meal_type='lunch', user_id=current_user.id).all()
    dinners = Dish.query.filter_by(meal_type='dinner', user_id=current_user.id).all()
    return render_template('index.html', appetizers=appetizers, lunches=lunches, dinners=dinners)  

@app.route('/add', methods=['POST'])
@login_required
def add():
    name = request.form.get('dish_name')
    meal_type = request.form.get('meal_type')
    ingredient_list = request.form.getlist('ingredients')

    new_dish = Dish(name=name, meal_type=meal_type, user_id=current_user.id)
    db.session.add(new_dish)
    db.session.flush()

    for ingredient_name in ingredient_list:
        if ingredient_name.strip():
            db.session.add(Ingredient(name=ingredient_name.strip(), dish_id=new_dish.id))

    db.session.commit()
    return redirect('/')

 


@app.route('/addToMenu/<int:dish_id>')
@login_required
def addToMenu(dish_id):
    dish = Dish.query.get(dish_id)
    if dish.user_id == current_user.id:
        dish.addToMenu = not dish.addToMenu
        db.session.commit()
    return redirect('/')

@app.route('/delete/<int:dish_id>')
@login_required
def delete(dish_id):
    dish = Dish.query.get(dish_id)
    if dish.user_id == current_user.id:
        db.session.delete(dish)
        db.session.commit()
    return redirect('/')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 


@app.route('/ingredients')
def ingredients():
    
    grocery_items = Ingredient.query.join(Dish).filter(Dish.addToMenu == True).all()
    
    
    ingredient_count = {}
    for ingredient in grocery_items:
        if ingredient.name in ingredient_count:
            ingredient_count[ingredient.name] += 1
        else:
            ingredient_count[ingredient.name] = 1
    
    return render_template('ingredients.html', ingredient_count=ingredient_count)




@app.route('/menu')
def menu():
    menu_items = Dish.query.filter_by(addToMenu=True).all()
    return render_template('menu.html', menu_items=menu_items) 

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)  
