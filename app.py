from flask import Flask, request
from flask_pymongo import PyMongo
from bson.json_util import dumps

application = Flask("my_glo4035_application")
application.config["MONGO_URI"] = "mongodb://admin:zxcv12345@ds237563.mlab.com:37563/soap-inventory"
mongoDb = PyMongo(application)
transactDb = mongoDb.db.transactions

@application.route("/", methods=["GET"])
def index():
    return "Accueil"

@application.route("/transactions", methods=["POST"])
def import_transactions():
    if request.headers['Content-Type'] == "application/json":
        data = request.get_json()
        transactDb.insert_one(data)

@application.route("/transactions", methods=["GET"])
def display_transactions():
    return dumps(transactDb.find())

if __name__ ==  "__main__":
    application.run(host="0.0.0.0", port=80)