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
    """Return water quantity in m3 of water in m3 of dry soil"""

    res = sensorLinearFit.strip("()").split(",")
    a = float(res[0])
    b = float(res[1])
    c = float(res[2])
    print(a)
    print(b)
    print(c)
    waterVolume = a*pow(soilMoisture, 2) + b*soilMoisture + c
    print(waterVolume)

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
