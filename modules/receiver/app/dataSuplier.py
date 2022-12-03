from typing import List
import requests
from datetime import timedelta, datetime
from dateutil import tz
import xxtea

from EdgeNodeConfiguration import EdgeNodeConfiguration
from ActuatorConfiguration import ActuatorConfiguration
from MQTTConnection import MQTTConnection

apiDir = "https://sa-api.azurewebsites.net/api/"
# apiDir = "http://172.31.16.1:7180/api/"
# dateformat = "%Y-%m-%d %H:%M:%S"
date = "2000-01-01 00:00:00"
oldDatetimeConfig = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
oldDatetimeActuator = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
oldDatetimeMQTT = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

config = None
actuatorList = []
actuatorCache = {}
mqttCache = {}


def getEdgeNodeID(hostname) -> int:
    query = {"hostname": str(hostname)}
    try:
        getEdgeNode = requests.get(apiDir+"edgeNodes", params=query)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e.response)
        return -1
    if getEdgeNode.status_code == 404:
        print("Error 404")
        return False
    jsonEdgeNode = getEdgeNode.json()
    edgeNodeID = jsonEdgeNode[0]["id"]
    return edgeNodeID


def getConfig(edgeNodeID) -> bool:
    global oldDatetimeConfig
    global sensorIDArray, sensorSerialArray, sensorLinearFitArray
    global plantationIDArray, fieldCapacityArray, optimalWaterArray

    if (datetimeChecker(oldDatetimeConfig)):
        return True

    sensorIDArray = []
    sensorSerialArray = []
    sensorLinearFitArray = []
    plantationIDArray = []
    fieldCapacityArray = []
    optimalWaterArray = []
    try:
        edgeNodeConfig = requests.get(apiDir +
                                      f"edgeNodes/{edgeNodeID}/config")
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e.response)
        return False
    if edgeNodeConfig.status_code == 404:
        print("Error 404")
        return False
    date = edgeNodeConfig.headers.get('Date').removesuffix(" GMT")
    oldDatetimeConfig = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S")
    jsonEdgeNodeConfig = edgeNodeConfig.json()
    for entry in jsonEdgeNodeConfig:
        sensorIDArray.append(entry["sensorID"])
        sensorSerialArray.append(entry["sensorSerial"])
        sensorLinearFitArray.append(entry["sensorLinearFit"])
        plantationIDArray.append(entry["plantationID"])
        fieldCapacityArray.append(entry["fieldCapacity"])
        optimalWaterArray.append(entry["optimalWater"])
    return True


def searchConfig(serial, edgeNodeID) -> EdgeNodeConfiguration:
    global sensorIDArray, sensorSerialArray, sensorLinearFitArray
    global plantationIDArray, fieldCapacityArray, optimalWaterArray
    global config

    if not getConfig(edgeNodeID):
        return None
    if serial in sensorSerialArray:
        index = sensorSerialArray.index(serial)
        sensorID = sensorIDArray[index]
        sensorSerial = sensorSerialArray[index]
        sensorLinearFit = sensorLinearFitArray[index]
        plantationID = plantationIDArray[index]
        fieldCapacity = fieldCapacityArray[index]
        optimalWater = optimalWaterArray[index]
        config = EdgeNodeConfiguration(
            edgeNodeID, sensorID, sensorSerial, sensorLinearFit, plantationID, fieldCapacity, optimalWater)
        return config
    return None


def getActuators(plantationID) -> bool:
    global oldDatetimeActuator
    global actuatorIDArray, actuatorSerialArray, actuatorList
    global actuatorCache

    if plantationID in actuatorCache:
        if datetimeChecker(actuatorCache.get(plantationID)[0]):
            return True
    actuatorList = []
    try:
        actuatorResponse = requests.get(apiDir +
                                        f"plantation/{plantationID}/actuators")
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e.response)
        return False
    if actuatorResponse.status_code == 404:
        print("Error 404")
        return False
    date = actuatorResponse.headers.get('Date').removesuffix(" GMT")
    oldDatetimeActuator = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S")
    jsonEdgeNodeConfig = actuatorResponse.json()
    for entry in jsonEdgeNodeConfig:
        actuatorList.append(ActuatorConfiguration(
            entry["actuatorID"], entry["actuatorSerial"]))
    actuatorCache[plantationID] = [oldDatetimeActuator, actuatorList]
    return True


def searchActuators(plantationID) -> List[ActuatorConfiguration]:
    global actuatorIDArray, actuatorSerialArray
    global actuatorList

    if not getActuators(plantationID):
        return None
    actuator = actuatorCache.get(plantationID)[1]
    return actuator


def getMQTT(mqttConfigID) -> bool:
    global oldDatetimeMQTT
    global mqttCache
    if mqttConfigID in mqttCache:
        if datetimeChecker(mqttCache.get(mqttConfigID)[0]):
            return True
    try:
        mqttResponse = requests.get(apiDir +
                                    f"plantation/{mqttConfigID}/mqtt")
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e.response)
        return False
    if mqttResponse.status_code == 404:
        print("Error 404")
        return False
    date = mqttResponse.headers.get('Date').removesuffix(" GMT")
    oldDatetimeMQTT = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S")
    jsonEdgeNodeConfig = mqttResponse.json()
    print(jsonEdgeNodeConfig)
    for entry in jsonEdgeNodeConfig:
        mqttCache[mqttConfigID] = [oldDatetimeMQTT, MQTTConnection(entry["mqttConnID"], entry["mqttConnName"], entry["mqttHost"],
                                                                   entry["mqttPort"], entry["mqttClientID"], entry["mqttUserName"], entry["mqttPassword"])]
    return True


def searchMQTT(mqttConfigID) -> MQTTConnection:
    if not getMQTT(mqttConfigID):
        return None
    mqtt = mqttCache.get(mqttConfigID)[1]
    return mqtt


def datetimeChecker(oldDatetime) -> bool:
    oldDatetime = oldDatetime.astimezone(
        tz.gettz("Europe/Madrid"))
    now = datetime.utcnow().astimezone(tz.gettz("Europe/Madrid"))
    pastDatetime = oldDatetime + timedelta(hours=1)
    if (now < pastDatetime):
        return True
    return False
