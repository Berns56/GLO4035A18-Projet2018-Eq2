from jsonschema import validate, ValidationError

def schemaSoapValidation(p_item, p_schema):
    try:
        validate(p_item, p_schema)
    except ValidationError:
        return False
    else:
        return True

SCHEMA_SOAP_PURCHASE = {
    "properties" : {
        "date" : {
			"type" : "string"
		},
        "item" : {
			"type" : "string"
		},
        "qte" : {
			"type" : "string"
		},
        "unit" :  {
			"type" : "string"
		},
        "total" : {
			"type" : "string"
		},
        "stotal" : {
			"type" : "string"
		},
        "tax" : {
			"type" : "string"
		} 
    },
    "required" : ["date", "item", "qte", "unit", "total", "stotal", "tax"]
}

SCHEMA_SOAP_DENSITY = {
    "properties" : {
        "Information" : {
			"type" : "string"
		},
        "item" : {
			"type" : "string"
		},
        "g" : {
			"type" : "string"
		},
        "ml" :  {
			"type" : "string"
		}
    },
    "required" : ["item", "g", "ml"]
}

SCHEMA_SOAP_LABOR = {
    "properties" : {
        "date" : {
			"type" : "string"
		},
        "item" : {
			"type" : "string"
		},
        "qte" : {
			"type" : "string"
		},
        "unit" :  {
			"type" : "string"
		},
        "job_id" : {
			"type" : "string"
		},
        "type" : {
			"type" : "string"
		} 
    },
    "required" : ["date", "item", "qte", "unit", "type"]
}