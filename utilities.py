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

def dateFormat(p_dateToFormat):
	try:
		dateInProcess = p_dateToFormat.split(" ")
		if len(dateInProcess) == 3:
			dateInProcess[1] = convertStrMonthToStrMonthNumber(dateInProcess[1].upper())
			return str(dateInProcess[2] + "-" + dateInProcess[1] + "-" + dateInProcess[0])
	except Exception as e:
		return str(e)

def convertStrMonthToStrMonthNumber(p_monthToConvert):
    return {
        "JANUARY" : "01",
        "FEBRUARY" : "02",
        "MARCH" : "03",
        "APRIL" : "04",
        "MAY" : "05",
        "JUNE" : "06",
        "JULY" : "07",
        "AUGUST" : "08",
        "SEPTEMBER" : "09",
        "OCTOBER" : "10",
        "NOVEMBER" : "11",
        "DECEMBER" : "12"
	}.get(p_monthToConvert)