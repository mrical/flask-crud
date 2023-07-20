from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

connection_string = "mongodb+srv://<user>:<password>@cluster0.wjwkw.gcp.mongodb.net/?retryWrites=true&w=majority"
database = "python-starter"
db_collection = "user"

client = MongoClient(connection_string)
db = client[database]
collection = db[db_collection]


@app.route('/users', methods=['GET'])
def get_users():
    users = list(collection.find())
    return dumps(users)


@app.route("/users/<id>", methods=['GET'])
def get_user_with_id(id):
    user = collection.find_one({'_id': ObjectId(id)})
    if user:
        return dumps(user)
    else:
        return jsonify({'error': "User not found"}), 400


@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if 'name' in data and 'email' in data and 'password' in data:
        user = {
            'name': data['name'],
            'email': data['email'],
            'password': data['password']
        }
        result = collection.insert_one(user)
        return jsonify({'message': 'User created', 'id': str(result.inserted_id)}), 201
    else:
        return jsonify({'error': 'Missing required fields'}), 400


@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    data = request.json
    if 'name' in data and 'email' in data and 'password' in data:
        updated_fields = {}
        if 'name' in data:
            updated_fields['name'] = data['name']
        if 'email' in data:
            updated_fields['email'] = data['email']
        if 'password' in data:
            updated_fields['password'] = data['password']
        result = collection.update_one({"_id": ObjectId(id)}, {
                                       "$set": updated_fields})
        if result.modified_count > 0:
            return jsonify({'message': "User updated"})
        else:
            return jsonify({'error': 'User not found'}), 404

    else:
        return jsonify({'error': 'Missing fields to update'}), 400


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    result = collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'User deleted'})
    else:
        return jsonify({'error': 'User not found'}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
