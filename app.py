from flask import Flask, request, jsonify, abort, send_from_directory, render_template
from flask_pymongo import PyMongo
from bson.json_util import dumps
import hashlib
import utilities

application = Flask("my_glo4035_application")
application.config["MONGO_URI"] = "mongodb://admin:admin123@ds237563.mlab.com:37563/soap-inventory"
mongoDb = PyMongo(application)
transactDb = mongoDb.db.transactions
purchasesDb = transactDb.purchases ##
densitiesDb = transactDb.densities ##
laborsDb = transactDb.labors##

@application.route("/", methods=["GET"])
def index():
     return send_from_directory('/templates', 'main.html')

@application.route("/transactions", methods=["GET"])
def display_transactionsHtml():
    return send_from_directory('/templates', 'transactionsList.html')

@application.route("/transactions/modifyPurchase", methods=["GET"])
def display_modifyPurchaseHtml():
    return send_from_directory('/templates', 'modifyPurchase.html')

@application.route("/transactions/modifyDensity", methods=["GET"])
def display_modifyDensityHtml():
    return send_from_directory('/templates', 'modifyDensity.html')

@application.route("/transactions/modifyLabors", methods=["GET"])
def display_modifyLaborsHtml():
    return send_from_directory('/templates', 'modifyLabors.html')

@application.route("/transactions/purchases", methods=["GET"])
def display_purchases():
    return dumps(purchasesDb.find())

@application.route("/transactions/densities", methods=["GET"])
def display_densities():
    return dumps(densitiesDb.find())

@application.route("/transactions/labors", methods=["GET"])
def display_labors():
    return dumps(laborsDb.find())



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

@application.route("/transactions/add/purchase",methods=["POST,GET"])
def add_Purchase():
    if(request.headers['Content-Type']=="application/json"):
        purchase = request.get_json()
        if(utilities.schemaSoapValidation(purchase,utilities.SCHEMA_SOAP_PURCHASE)):
            purchasesDb.insert_one(purchase)
        else:
            return jsonify(result="Failure",status="400",message="Purchase has the wrong content type!"),400
    else:
        return jsonify(result="Failure",status="400",message="Wrong content type!"),400    
    return jsonify(result = "Success", status = "200", message = "Purchase add"), 200


@application.route("/transactions/add/density",methods=["POST,GET"])
def add_Density():
    if(request.headers['Content-Type']=="application/json"):
        purchase = request.get_json()
        if(utilities.schemaSoapValidation(purchase,utilities.SCHEMA_SOAP_DENSITY)):
            purchasesDb.insert_one(purchase)
        else:
            return jsonify(result="Failure",status="400",message="Density has the wrong content type!"),400
    else:
        return jsonify(result="Failure",status="400",message="Wrong content type!"),400    
    return jsonify(result = "Success", status = "200", message = "Density add"), 200


@application.route("/transactions/add/labor",methods=["POST,GET"])
def add_Labor():
    if(request.headers['Content-Type']=="application/json"):
        purchase = request.get_json()
        if(utilities.schemaSoapValidation(purchase,utilities.SCHEMA_SOAP_LABOR)):
            purchasesDb.insert_one(purchase)
        else:
            return jsonify(result="Failure",status="400",message="Labor has the wrong content type!"),400
    else:
        return jsonify(result="Failure",status="400",message="Wrong content type!"),400    
    return jsonify(result = "Success", status = "200", message = "Labor add"), 200

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