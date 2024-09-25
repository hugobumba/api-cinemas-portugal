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
client = MongoClient(f'mongodb+srv://{username}:{password}@cluster0.rkwdb.mongodb.net/{database_name}?retryWrites=true&w=majority')
#client = MongoClient('mongodb+srv://hugobumba:mhungo@cluster0.rkwdb.mongodb.net/')
db = client[database_name]
collection = db[collection_name]

@app.route('/movies', methods=['GET'])
def get_all_movies():
    result = list(collection.find({}, {'_id': 0}))
    return jsonify(result)  # Transformar a lista em um objeto JSON

@app.route('/cinema/<cinema>', methods=['GET'])
def get_cinema_movies(cinema):
    if cinema == "all":
        result = list(collection.find({}, {'_id': 0}))
    else:
        result = list(collection.find({"source": cinema}, {'_id': 0}))
    return jsonify(result)

@app.route('/status/<status>', methods=['GET'])
def get_status_movies(status):
    if status == "all":
        result = list(collection.find({}, {'_id': 0}))
    else:
        result = list(collection.find({"source": status}, {'_id': 0}))
    return jsonify(result)

@app.route('/genre/<genre>', methods=['GET'])
def get_genre_movies(genre):
    if genre == "all":
        result = list(collection.find({}, {'_id': 0}))
    else:
        result = list(collection.find({"source": genre}, {'_id': 0}))
    return jsonify(result)

@app.route('/year/<year>', methods=['GET'])
def get_year_movies(year):
    if year == "all":
        result = list(collection.find({}, {'_id': 0}))
    else:
        result = list(collection.find({"source": year}, {'_id': 0}))
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
