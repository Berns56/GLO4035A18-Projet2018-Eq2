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
DensityDb = mongoDb.db.densitySoap

@application.route("/", methods=["GET"])
def index():
        return abort(400,description="Format Incorrect")
  

@application.route("/InsertionTransaction", methods=["GET","POST"])
def Insertions_transactions():
        if request.is_json:
                fichierJSON = request.get_json()
                dataSoap = []
                dataDensity=[]
                schema = Util.loaderFicherJSON("schema.json")
                numberField = 0
                itemDict = {}
                print(numberField)
                for key,value in fichierJSON.items():
                        if key != "information;item;g;ml":                                 
                               if numberField <=6:
                                       print(numberField)
                                       itemDict[key]=value
                                       numberField+=1
                               else:
                                       print(itemDict)
                                       dataSoap.append(itemDict)
                                       itemDict.clear()
                                       
                        else:
                               densintyValue = value.split(';')
                               densityKey = key.split(';')
                               dictDensity = {}
                               for i in range(0,len(densityKey)):
                                       dictDensity[densityKey[i]] = densintyValue[i]
                               dataDensity.append(dictDensity)
                for item in dataSoap:
                       
                        if jsonschema.Draft3Validator(schema).is_valid(item)==False:
                                abort(400,description="Format JSON Incorrect pour l'entrée {}".format(str(item)))
                        elif Util.validerFormat(item)==False:
                                abort(400,description="un ou plusieurs type de donnée est incorrect pour :{}".format(str(item)))
                        elif Util.validerTotal(item):
                                abort(400,description="Le total n'est pas égale à stoal+taxt, pour la donnée".format(str(item)))
                for item in dataSoap:
                        print(item)
                        transactDb.insert_one(item)
                for item in dataDensity:
                        DensityDb.insert_one(item)

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