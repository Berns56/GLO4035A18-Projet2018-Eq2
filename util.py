import json
import datetime

def validerFormat(dataJson):
    if dataJson["qte"].isdigit() is False:
        print("qte")
        return False
    if dataJson["stotal"].replace('.','',1).isdigit() is False:
        print("stoal")
        return False
    if dataJson["total"].replace('.','',1).isdigit() is False:
        print("total")
        return False
    if dataJson["tax"].replace('.','',1).isdigit() is False:
        print("tax")
        return False
    return True

def validerTotal(dataJson):
    return float(dataJson["total"]) == float(dataJson["stotal"])+float(dataJson["tax"])
