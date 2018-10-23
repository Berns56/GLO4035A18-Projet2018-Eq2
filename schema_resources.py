import jsonschema

SCHEMA_SOAP_PRODUCT = {
    "properties" : {
        "date" : {"type" : "string"},
        "item" : {"type" : "string"},
        "qte" : {"type" : "string"},
        "unit" :  {"type" : "string"},
        "total" : {"type" : "string"},
        "stotal" : {"type" : "string"},
        "tax" : {"type" : "string"} 
    },
    "required" : ["date","item","qte", "unit","total","stotal","tax"]
}