from typing import List

# Import RFM9x
import adafruit_rfm9x

from EdgeNodeConfiguration import *
from ActuatorConfiguration import *


def isWateringNecessary(config: EdgeNodeConfiguration,
                        airTemperature: float, airHumidity: float, soilMoisture: int, leafMoisture: int) -> bool:
    waterVolume = moistureConverter(soilMoisture, config.sensorLinearFit)
    if waterVolume > (config.fieldCapacity * 0.9):
        return False
    elif leafMoisture > 80 and airHumidity > 80:
        return False
    elif waterVolume < config.optimalWater:
        return True
    elif airTemperature < 30 and airHumidity < 70 and leafMoisture < 20:
        return True
    else:
        return False


def moistureConverter(soilMoisture, sensorLinearFit) -> float:
    """Return a percentage value between 0 and 100%"""
    sensorLinearFit = sensorLinearFit.replace("(", "")
    sensorLinearFit = sensorLinearFit.replace(")", "")
    param = sensorLinearFit.split(",")

    slope = float(param[0])
    intercept = float(param[1])
    waterVolume = ((1.0/int(soilMoisture))*slope)+intercept
    # In cm^3/cm^3
    return waterVolume


def watering(actuator: List[ActuatorConfiguration], necessary: bool) -> list:
    packet = []
    boolean = "false"
    if necessary:
        boolean = "true"
    for entry in actuator:
        serial = entry.actuatorSerial
        packet.append(f"{serial}#water={boolean};timeout=3600")
    return packet
