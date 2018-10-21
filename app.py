from flask import Flask, request,abort
from flask_pymongo import PyMongo
from bson.json_util import dumps
import jsonschema
import Util
application = Flask("my_glo4035_application")
application.config['MONGO_HOST'] = 'ds237563.mlab.com'
application.config['MONGO_PORT'] = '37563'
application.config['MONGO_DBNAME'] = 'soap-inventory'
application.config['MONGO_USERNAME'] = 'admin'
application.config['MONGO_PASSWORD'] = 'zxcv12345'
application.config['MONGO_AUTH_SOURCE'] = 'admin'

application.config["MONGO_URI"] = "mongodb://admin:zxcv12345@ds237713.mlab.com:37713/soap-inventory"
##application.config["MONGO_URI"] = 'mongodb://'+application.config["MONGO_USERNAME"]+":"+application.config['MONGO_PASSWORD']+"@"+application.config['MONGO_HOST']+":"+application.config['MONGO_PORT'] +"/"+application.config['MONGO_DBNAME']
mongoDb = PyMongo(application)
transactDb = mongoDb.db.transactions

@application.route("/", methods=["GET"])
def index():
    return "Accueil"

@application.route("/transactions", methods=["POST"])
def import_transactions():
        if request.headers['Content-Type'] == "application/json":
                data = request.get_json()
                schema = Util.loaderFicherJSON("schema.json")
                for target_list in data:
                        if jsonschema.Draft3Validator(schema).is_valid(target_list)==False:
                                return "400 JSON INVALID"
                        elif Util.validerFormat(target_list)==False:
                                return "400 Format de donnée Invalid"
                        elif Util.validerTotal(target_list)==False:
                                return "400 total est différent de stotal+tax"
                else:
                     transactDb.insertOne(data)
                     return "200"   

@application.route("/transactions", methods=["GET"])
def display_transactions():
    return dumps(transactDb.find())


if __name__ ==  "__main__":
    application.run(host="0.0.0.0", port=80,debug=True)