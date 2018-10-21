import jsonschema
import Util
import re
try:
    schema = Util.loaderFicherJSON("schema.json")
    data = Util.loaderFicherJSON("data.json")
    
    jsonschema.Draft3Validator(schema).is_valid(data)
    print(Util.validerFormat(data))
    print(Util.validerTotal(data))
   

except Exception as e:
    print(e)
