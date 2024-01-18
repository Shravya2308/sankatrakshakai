from pymongo import MongoClient
from flask import Flask ,render_template
from app import app
import json
from bson import json_util
client = MongoClient('localhost',27017)

db = client['sankatrakshak']

results = db.results

@app.route('/')
def dashboard():
    return render_template("index.html")

@app.route("/getinfo")
def fetchall():
    callsindb = results.find()
    all_calls = []
    for data in results.find():
        all_calls.append(data)
        # print(
    return json.loads(json_util.dumps(all_calls))
