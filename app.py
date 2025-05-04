from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)




@app.route('/')
@app.route('/dishes')
def home():
    
    return render_template('index.html')

@app.route('/ingredients')
def ingredients():
    return render_template('ingredients.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

if __name__ == '__main__':
    app.run(debug=True)