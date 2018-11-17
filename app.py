from flask import Flask, request, jsonify, abort, send_from_directory, render_template
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
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


@application.route("/transactions/purchases", methods=["GET"])
def display_purchases():
    return dumps(purchasesDb.find())

@application.route("/transactions/densities", methods=["GET"])
def display_densities():
    return dumps(densitiesDb.find())

@application.route("/transactions/labors", methods=["GET"])
def display_labors():
    return dumps(laborsDb.find())

@application.route("/transactions/add", methods=["GET"])
def display_addTransactionsHtml():
    return send_from_directory('/templates', 'addTransactions.html')

@application.route("/transactions/add/purchase",methods=["POST"])
def add_Purchase():
    if(request.headers['Content-Type']=="application/json"):
        purchase = request.get_json()
        if(utilities.schemaSoapValidation(purchase,utilities.SCHEMA_SOAP_PURCHASE)):
            purchasesDb.insert_one(purchase)
        else:
            return jsonify(result="Failure",status="400",message="Purchase has the wrong content type!"),400
    else:
        return jsonify(result="Failure",status="400",message="Wrong content type!"),400    
    return jsonify(result="Success", status="200", message="Purchase add"),200


@application.route("/transactions/add/density",methods=["POST"])
def add_Density():
    if(request.headers['Content-Type']=="application/json"):
        purchase = request.get_json()
        if(utilities.schemaSoapValidation(purchase,utilities.SCHEMA_SOAP_DENSITY)):
            densitiesDb.insert_one(purchase)
        else:
            return jsonify(result="Failure",status="400",message="Density has the wrong content type!"),400
    else:
        return jsonify(result="Failure",status="400",message="Wrong content type!"),400    
    return jsonify(result="Success", status="200", message="Density add"),200


@application.route("/transactions/add/labor",methods=["POST"])
def add_Labor():
    if(request.headers['Content-Type']=="application/json"):
        purchase = request.get_json()
        if(utilities.schemaSoapValidation(purchase,utilities.SCHEMA_SOAP_LABOR)):
            laborsDb.insert_one(purchase)
        else:
            return jsonify(result="Failure",status="400",message="Labor has the wrong content type!"),400
    else:
        return jsonify(result="Failure",status="400",message="Wrong content type!"),400    
    return jsonify(result="Success", status="200", message="Labor add"), 200

@application.route("/transactions/modifyPurchase", methods=["GET"])
def display_modifyPurchaseHtml():
    return send_from_directory('/templates', 'modifyPurchase.html')

@application.route("/transactions/modify/purchase", methods=["PUT"])
def modify_Purchase():
    try:
        if(request.headers['Content-Type']=="application/json"):
            purchase = request.get_json()
            myquery = {"_id": ObjectId(purchase["id"])}
            newvalues = { "$set": {"date": purchase["date"], "item":purchase["item"], "qte": purchase["qte"], "total" : purchase["total"], "stotal" : purchase["stotal"], "tax" : purchase["tax"]}}
            purchasesDb.update_one(myquery,newvalues)
        else:
            return jsonify(result="Failure",status="400",message="Wrong content type!"),400 
    except Exception as e:
            return str(e)
    return jsonify(result="Success", status="200", message="Purchase modified"), 200

@application.route("/transactions/modifyDensity", methods=["GET"])
def display_modifyDensityHtml():
    return send_from_directory('/templates', 'modifyDensity.html')

@application.route("/transactions/modify/density", methods=["PUT"])
def modify_Density():
    try:
        if(request.headers['Content-Type']=="application/json"):
            density = request.get_json()
            myquery = {"_id": ObjectId(density["id"])}
            newvalues = { "$set": {"item":density["item"], "g" : density["g"], "ml" : density["ml"]}}
            densitiesDb.update_one(myquery,newvalues)
        else:
            return jsonify(result="Failure",status="400",message="Wrong content type!"),400 
    except Exception as e:
            return str(e)
    return jsonify(result="Success", status="200", message="Density modified"), 200

@application.route("/transactions/modifyLabors", methods=["GET"])
def display_modifyLaborsHtml():
    return send_from_directory('/templates', 'modifyLabors.html')

@application.route("/transactions/modify/labor", methods=["PUT"])
def modify_Labor():
    try:
        if(request.headers['Content-Type']=="application/json"):
            labor = request.get_json()
            myquery = {"_id": ObjectId(labor["id"])}
            newvalues = { "$set": {"date": labor["date"], "item":labor["item"], "qte": labor["qte"], "jobId" : labor["jobId"], "unit" : labor["unit"], "type" : labor["type"]}}
            laborsDb.update_one(myquery,newvalues)
        else:
            return jsonify(result="Failure",status="400",message="Wrong content type!"),400 
    except Exception as e:
            return str(e)
    return jsonify(result="Success", status="200", message="labor modified"), 200

@application.route("/transactions/delete/purchase", methods=["DELETE"])
def delete_purchase():
    try:
        if(request.headers['Content-Type']=="application/json"):
            purchase = request.get_json()
            myquery = {"_id": ObjectId(purchase["id"])}
            purchasesDb.delete_one(myquery)
        else:
            return jsonify(result="Failure",status="400",message="Wrong content type!"),400 
    except Exception as e:
            return str(e)
    return jsonify(result="Success", status="200", message="purchase deleted"), 200


@application.route("/transactions/delete/density", methods=["DELETE"])
def delete_density():
    try:
        if(request.headers['Content-Type']=="application/json"):
            density = request.get_json()
            myquery = {"_id": ObjectId(density["id"])}
            densitiesDb.delete_one(myquery)
        else:
            return jsonify(result="Failure",status="400",message="Wrong content type!"),400 
    except Exception as e:
            return str(e)
    return jsonify(result="Success", status="200", message="density deleted"), 200

@application.route("/transactions/delete/labors", methods=["DELETE"])
def delete_labor():
    try:
        if(request.headers['Content-Type']=="application/json"):
            labor = request.get_json()
            myquery = {"_id": ObjectId(labor["id"])}
            laborsDb.delete_one(myquery)
        else:
            return jsonify(result="Failure",status="400",message="Wrong content type!"),400 
    except Exception as e:
            return str(e)
    return jsonify(result="Success", status="200", message="labor deleted"), 200

@application.route("/totalCost", methods=["GET"])
def display_totalCostHtml():
    return send_from_directory('/templates', 'totalCost.html')

@application.route("/totalCost/purchase", methods=["POST"])
def totalCostPurchase():
    try:
        if(request.headers['Content-Type']=="application/json"):
            purchase = request.get_json()
            regex = "/%s/" % purchase["type"]
            myquery = {"$and":[{"date":purchase["date"]}, {"item" : {"$regex": regex}}]}
            return dumps(purchasesDb.find(myquery))
        else:
            return jsonify(result="Failure",status="400",message="Wrong content type!"),400 
    except Exception as e:
            return str(e)
    return jsonify(result="Success", status="200", message="labor deleted"), 200

if __name__ ==  "__main__":
    application.run(host="0.0.0.0", port = 80)
