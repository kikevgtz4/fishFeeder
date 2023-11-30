#app.py

from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import datetime
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file


app = Flask(__name__)

# MongoDB setup
mongo_uri = os.environ.get("MONGO_URI", "your_default_mongo_uri")
client = MongoClient(mongo_uri)
db = client['fish_feeder']  # Replace with your database name
feed_collection = db['feeding_log']   # Replace with your collection name

@app.route('/')
def index():
    feed_log = list(feed_collection.find({}, {"_id": 0}))
    return render_template('index.html', feed_log=feed_log)

@app.route('/feed_log_data')
def feed_log_data():
    feed_log = list(feed_collection.find({}, {"_id": 0}))
    return jsonify(feed_log=feed_log)

@app.route('/log_feed', methods=['GET', 'POST'])
def log_feed():
    if request.method == 'GET':
        user = request.args.get('user', 'DefaultUser')
        data = {'user': user}
    else:  # POST request
        data = request.json

    data['time'] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    feed_collection.insert_one(data)
    return jsonify(success=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
