from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

dishes = [
    {"id": 1, "name": "Spaghetti", "type": "Dinner", "ingredients": ["pasta", "tomato sauce"]},
    {"id": 2, "name": "Bruschetta", "type": "Appetizer", "ingredients": ["bread", "tomatoes", "basil"]}
]

@app.route("/dishes", methods=["GET"])
def get_dishes():
    return jsonify(dishes)

if __name__ == "__main__":
    app.run(debug=True)
