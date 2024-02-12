"""
Simple FastApi Application
"""
import os
import json
# For Routes
from flask import Flask, jsonify, request
from bson import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Create App
base_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

uri = "mongodb+srv://f20190652:f20190652@gplan-graph-floorplan-c.gpydngh.mongodb.net/?retryWrites=true&w=majority"
db_name = 'levels'

client = MongoClient(uri, server_api=ServerApi('1'))
db = client[db_name]

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Convert ObjectId to string for JSON serialization
def json_serial(obj):
    """JSON serializer for objects not serializable by default JSON encoder."""
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError("Type not serializable")


@app.route('/api/<shape>/get_all_levels', methods=['GET'])
def get_data_by_id(shape):
    collection = db[shape]
    all_entries = list(collection.find())
    return jsonify(json.loads(json.dumps(all_entries, default=json_serial)))


@app.route('/')
@app.route('/index')
def index():
    return '<h1> Hooray! Game\'s flask backend up and running!</h1>'


if __name__ == '__main__':
    app.run()
