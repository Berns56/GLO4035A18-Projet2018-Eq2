from flask import Flask, request, jsonify, abort, send_from_directory
from flask_pymongo import PyMongo
from bson.json_util import dumps
import hashlib
import jsonschema
import schema_resources
import util

application = Flask("my_glo4035_application")
application.config["MONGO_URI"] = "mongodb://admin:admin123@ds237563.mlab.com:37563/soap-inventory"
mongoDb = PyMongo(application)
transactDb = mongoDb.db.transactions
densityDb = mongoDb.db.densitySoap

@application.route("/", methods=["GET"])
def index():
     return send_from_directory('/Forms', 'main.html')

@application.route("/transactions", methods=["GET"])
def display_transactions():
    return dumps(transactDb.find())

@application.route("/transactions", methods=["POST"])
def import_transactions():
    if (request.headers['Content-Type'] == "application/json"):
        dataJSON = request.get_json()

        dataSoap = []
        dataDensity = []
        fieldCount = 0
        dictItems = {}

        for key, value in dataJSON.items():
            if (key != "information;item;g;ml"):
                if (fieldCount <= 6):
                    dictItems[key] = value
                    fieldCount += 1
                else:
                    dataSoap.append(dictItems)
                    dictItems.clear()
            else:
                densityValue = value.split(';')
                densityKey = key.split(';')
                dictDensity = {}
                for i in range(0, len(densityKey)):
                    dictDensity[densityKey[i]] = densityValue[i]
                break
                dataDensity.append(dictDensity)
            break

        for item in dataSoap:
            if (jsonschema.Draft3Validator(schema_resources.SCHEMA_SOAP_PRODUCT).is_valid(item) == False):
                abort(400, description = "Format JSON incorrect pour l'entrée {}".format(str(item)))
            elif (util.validerFormat(item) == False):
                abort(400,description="Un ou plusieurs types de donnée sont incorrects pour :{}".format(str(item)))
            elif (util.validerTotal(item)):
                abort(400,description="Le total n'est pas égal à (stoal + taxt) pour la donnée".format(str(item)))

        for itemDS in dataSoap:
            transactDb.insert_one(itemDS) 
            break
        for itemDD in dataDensity:
            densityDb.insert_one(itemDD)
            break

        transactDb.insert_one(dataJSON)

    return jsonify(result = "Success", status = "200", message = "Data imported!"), 200

@application.route("/transactions", methods=["DELETE"])
def delete_transactions():
    if (request.headers['Content-Type'] == "application/json"):
        encryptedPassword = hashlib.md5(request.get_json()["password"].encode("utf-8")).hexdigest()
        if (encryptedPassword == '0192023a7bbd73250516f069df18b500'):
            transactDb.drop()
            return jsonify(result = "Success", status = "200", message = "Database emptied!"), 200
        else:
            return jsonify(result = "Failure", status = "401", message = "Wrong password!"), 401

if __name__ ==  "__main__":
    application.run(host="0.0.0.0", port = 80)