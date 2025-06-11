from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from bson import ObjectId
from bson.errors import InvalidId
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

@app.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    try:
        task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
        if task:
            return jsonify({
                "id": str(task["_id"]),
                "title": task["title"],
                "description": task["description"],
                "status": task["status"]
            }), 200
        else:
            return jsonify({"error": "Task not found"}), 404
    except InvalidId:
        return jsonify({"error": "Invalid task ID"}), 400


@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    updated_task = {}

    if 'title' in data:
        updated_task['title'] = data['title']
    if 'description' in data:
        updated_task['description'] = data['description']
    if 'status' in data:
        updated_task['status'] = data['status']
    
    result = mongo.db.tasks.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": updated_task}
    )

    if result.matched_count == 1:
        return jsonify({"msg": "Task updated successfully"}), 200
    else:
        return jsonify({"error": "No Changes or no Task not found"}), 404
    
@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    result = mongo.db.tasks.delete_one({"_id": ObjectId(task_id)})

    if result.deleted_count == 1:
        return jsonify({"msg": "Task deleted successfully"}), 200
    else:
        return jsonify({"error": "Task not found"}), 404    

if __name__ == "__main__":
    app.run(debug=True)
    