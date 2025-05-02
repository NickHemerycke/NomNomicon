from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/dishes')
def dishes():
    return "<h1>Welcome to the Dishes Page</h1>"

@app.route('/ingredients')
def ingredients():
    return "<h1>Welcome to the Ingredients Page</h1>"

@app.route('/menu')
def menu():
    return "<h1>Welcome to the Menu Page</h1>"

if __name__ == '__main__':
    app.run(debug=True)