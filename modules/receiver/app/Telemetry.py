class Telemetry:
    def __init__(self, batteryConnect: bool, batteryVoltage: float, locationLat: float,
                 locationLng: float, locationAltitude: float, locationSatellites: int,
                 airTemperature: float, airHumidity: float, soilMoisture: int, leafMoisture: int):
        self.batteryConnect = batteryConnect
        self.batteryVoltage = batteryVoltage
        self.locationLat = locationLat
        self.locationLng = locationLng
        self.locationAltitude = locationAltitude
        self.locationSatellites = locationSatellites
        self.airTemperature = airTemperature
        self.airHumidity = airHumidity
        self.soilMoisture = soilMoisture
        self.leafMoisture = leafMoisture

    def __repr__(self) -> str:
        return (f"batConn:{self.batteryConnect}, batVolt:{self.batteryConnect}, lat:{self.locationLat}, "
                f"lng:{self.locationLng},alt:{self.locationAltitude},sat:{self.locationSatellites}, "
                f"airTemp:{self.airTemperature},airHumi:{self.airHumidity},soilMois:{self.soilMoisture}, "
                f"leafMois:{self.leafMoisture}, plantID:{self.plantationID}")

    def getTelemetry(self) -> dict:
        return {
            "batteryConnect": self.batteryConnect,
            "batteryVoltage": self.batteryVoltage,
            "latitude": self.locationLat,
            "longitude": self.locationLng,
            "altitude": self.locationAltitude,
            "satellites": self.locationSatellites,
            "airTemperature": self.airTemperature,
            "airHumidity": self.airHumidity,
            "soilMoisture": self.soilMoisture,
            "leafMoisture": self.leafMoisture
        }
