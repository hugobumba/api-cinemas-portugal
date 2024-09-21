from flask import Flask, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

username = os.getenv('MONGODB_USERNAME')
password = os.getenv('MONGODB_PASSWORD')
database_name = "movies_db"
collection_name = "movies_info"

# Conectar ao MongoDB Atlas
client = MongoClient(f'mongodb+srv://{username}:{password}@cluster0.rkwdb.mongodb.net/{database_name}')
db = client[database_name]
collection = db[collection_name]

@app.route('/movies_info/<cinema>', methods=['GET'])
def get_all_info(cinema):
    if cinema == "all":
        result = list(collection.find({}, {'_id': 0}))
    else:
        result = list(collection.find({"source": cinema}, {'_id': 0}))
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
