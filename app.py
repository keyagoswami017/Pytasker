from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os


load_dotenv()
app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
mongo = PyMongo(app)

#@app.route("/test-db")
#def test_db():
#    test_coll = mongo.db.test
#    test_coll.insert_one({"message": "Hello, World!"})
#    return jsonify({"msg": "Data inserted successfully!"}), 200

@app.route('/tasks',methods = ['POST'])
def create_task():
    task_collection = mongo.db.tasks
    data = request.get_json()

    if not all(key in data for key in ("title","description","status")):
        return jsonify({"error" : "Missing fields"}), 400
    
    task = {
        "title": data["title"],
        "description": data["description"],
        "status": data["status"]
    }
    result = task_collection.insert_one(task)
    return jsonify({"msg": "Task created successfully", "task_id": str(result.inserted_id)}), 201


@app.route('/tasks', methods=['GET'])
def get_tasks():
    task_collection = mongo.db.tasks
    tasks = task_collection.find()

    result = []
    for task in tasks:
        result.append({
            "id": str(task["_id"]),
            "title": task["title"],
            "description": task["description"],
            "status": task["status"]
        })
    return jsonify(result), 200

if __name__ == "__main__":
    app.run(debug=True)
    