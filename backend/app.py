from pathlib import Path

from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient
from pymongo.errors import PyMongoError

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR.parent / "frontend" / "templates"

app = Flask(__name__, template_folder=str(TEMPLATE_DIR))

client = MongoClient("mongodb://localhost:27017/")
db = client["todo_db"]
collection = db["todos"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/submittodoitem', methods=['POST'])
def submit_todo():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    item_name = data.get('itemName', '').strip()
    item_description = data.get('itemDescription', '').strip()

    if not item_name or not item_description:
        return jsonify({
            "error": "itemName and itemDescription are required"
        }), 400

    todo = {
        "itemName": item_name,
        "itemDescription": item_description
    }

    try:
        result = collection.insert_one(todo)
    except PyMongoError:
        return jsonify({"error": "Failed to save todo item to the database"}), 500

    return jsonify({
        "message": "Todo saved successfully",
        "id": str(result.inserted_id)
    }), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
