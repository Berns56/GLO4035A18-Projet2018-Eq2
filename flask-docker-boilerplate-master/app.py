from flask import Flask
application = Flask("my_glo4035_application")

@application.route("/", methods=["GET","POST"])
def index():
    return "Damn Son"

@application.route('/db', methods=["GET","POST"])
def db():
    return "Dah Phuc"

if __name__ ==  "__main__":
    application.run(host="0.0.0.0", port=80)
