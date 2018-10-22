from flask import Flask, request,abort,jsonify,Response
from flask_pymongo import PyMongo
from bson.json_util import dumps
import jsonschema
import json
import Util

application = Flask("my_glo4035_application")
application.config["MONGO_URI"] = "mongodb://admin:zxcv12345@ds237713.mlab.com:37713/soap-inventory"
mongoDb = PyMongo(application)
transactDb = mongoDb.db.transactions
Densenty = mongoDb.db.densitySoap

@application.route("/", methods=["GET"])
def index():
        return abort(400,description="Format Incorrect")
  

@application.route("/InsertionTransaction", methods=["GET","POST"])
def Insertions_transactions():
        if request.is_json:
               fichierJSON = request.get_json()
               dataSoap = []
               data.append(json.dumps(fichierJSON))
               schema = Util.loaderFicherJSON("schema.json")
               isDateField="date"
               itemDict = {}
               for key,value in fichierJSON.items():
                       if key == isItemField:
                               itemDict[key]=value
                               isDateField=key
                       else:
                               dataSoap.append(itemDict)
                               itemDict.clear()
                               itemDict[key]=value



                                               
            
                      
        else:
                return abort(400,description="Format JSOn Incorrect")
        return "200 Format JSON Correct"
            
               

@application.route("/transactions", methods=["POST"])
def import_transactions():
    if request.headers['Content-Type'] == "application/json":
        data = request.get_json()
        transactDb.insert_one(data)
@application.route("/transactions", methods=["GET"])
def display_transactions():
    return dumps(transactDb.find())

@application.errorhandler(400)
def format_JSON_incorrect(e):
        return "{},{}".format(400,e.description)


if __name__ ==  "__main__":
    application.run(host="0.0.0.0", port=80,debug=True)