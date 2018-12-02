from jsonschema import validate, ValidationError

ENCRYPTED_PASSWORD = "0192023a7bbd73250516f069df18b500"

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
			dateInProcess[0] = convertStrDaytoStrDayNumber(dateInProcess[0])
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

def convertStrDayToStrDayNumber(p_dayToConvert):
    if len(p_dayToConvert) > 1:
        return p_dayToConvert
    else:
        return "0" + p_dayToConvert
        
def purchaseFormat(p_purchaseToFormat):
    strQte = p_purchaseToFormat["qte"]
    p_purchaseToFormat["qte"] = int(strQte)
    strTotal = p_purchaseToFormat["total"]
    p_purchaseToFormat["total"] = float(strTotal)
    strSTotal = p_purchaseToFormat["stotal"]
    p_purchaseToFormat["stotal"] = float(strSTotal)
    strTax = p_purchaseToFormat["tax"]
    p_purchaseToFormat["tax"] = float(strTax)
    strDate = p_purchaseToFormat["date"]
    p_purchaseToFormat["date"] = dateFormat(strDate)
    return p_purchaseToFormat

def densityFormat(p_densityToFormat):
    strG = p_densityToFormat["g"]
    p_densityToFormat["g"] = float(strG)
    strML = p_densityToFormat["ml"]
    p_densityToFormat["ml"] = float(strML)
    return p_densityToFormat

def laborFormat(p_laborToFormat):
    strQte = p_laborToFormat["qte"]
    p_laborToFormat["qte"] = int(strQte)
    strJobId = p_laborToFormat["job_id"]
    p_laborToFormat["job_id"] = int(strJobId)
    strDate = p_laborToFormat["date"]
    p_laborToFormat["date"] = dateFormat(strDate)
    return p_laborToFormat