import jsonschema
import Util
import re
try:
    schema = Util.loaderFicherJSON("schema.json")
    data = Util.loaderFicherJSON("data.json")
    jsonschema.validate(data,schema)
    print(Util.validerFormat(data))
    print(Util.validerTotal(data))
   

except Exception as e:
    print(e)
