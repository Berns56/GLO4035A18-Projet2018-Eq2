from flask import Flask, request, jsonify, abort
from flask_pymongo import PyMongo
from bson.json_util import dumps
import hashlib
import utilities

application = Flask("my_glo4035_application")
application.config["MONGO_URI"] = "mongodb://admin:admin123@ds237563.mlab.com:37563/soap-inventory"
mongoDb = PyMongo(application)
transactDb = mongoDb.db.transactions
purchasesDb = transactDb.purchases
densitiesDb = transactDb.densities
laborsDb = transactDb.labors

@application.route("/", methods=["GET"])
def index():
     return send_from_directory('/templates', 'main.html')

@application.route("/transactions", methods=["GET"])
def display_transactionsHtml():
    return send_from_directory('/templates', 'transactionsList.html')

@application.route("/transactions/list", methods=["GET"])
def display_transactionsList():
    return dumps(transactDb.find())

@application.route("/transactions", methods=["POST"])
def import_transactions():
    if (request.headers['Content-Type'] == "application/json"):
        if isinstance(request.get_json(), dict):
            dataJSON = [request.get_json()]
            for dataItem in dataJSON:
                if utilities.schemaSoapValidation(dataItem, utilities.SCHEMA_SOAP_PURCHASE):
                    purchasesDb.insert_one(dataItem)
                elif utilities.schemaSoapValidation(dataItem, utilities.SCHEMA_SOAP_DENSITY): 
                    densitiesDb.insert_one(dataItem)
                elif utilities.schemaSoapValidation(dataItem, utilities.SCHEMA_SOAP_LABOR): 
                    laborsDb.insert_one(dataItem)
                else:
                    return jsonify(result = "Failure", status = "400", message = "Wrong transaction format!"), 400 
            return jsonify(result = "Success", status = "200", message = "Data imported!"), 200
        else:
            return jsonify(result = "Failure", status = "400", message = "Wrong content format!"), 400
    else:
        return jsonify(result = "Failure", status = "400", message = "Wrong content type!"), 400

@application.route("/transactions", methods=["DELETE"])
def delete_transactions():
    if (request.headers['Content-Type'] == "application/json"):
        encryptedPassword = hashlib.md5(request.get_json()["password"].encode("utf-8")).hexdigest()
        if (encryptedPassword == '0192023a7bbd73250516f069df18b500'):
            transactDb.drop()
            purchasesDb.drop()
            densitiesDb.drop()
            laborsDb.drop()
            return jsonify(result = "Success", status = "200", message = "Database emptied!"), 200
        else:
            return jsonify(result = "Failure", status = "401", message = "Wrong password!"), 401

if __name__ ==  "__main__":
    application.run(host="0.0.0.0", port = 80)