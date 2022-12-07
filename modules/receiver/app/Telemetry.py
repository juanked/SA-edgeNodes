class Telemetry:
    def __init__(self, batteryConnect: bool, batteryVoltage: float, locationLat: float,
                 locationLng: float, locationAltitude: float, locationSatellites: int,
                 airTemperature: float, airHumidity: float, waterContent: int, fieldCapacity: float, leafMoisture: int):
        self.batteryConnect = batteryConnect
        self.batteryVoltage = batteryVoltage
        self.locationLat = locationLat
        self.locationLng = locationLng
        self.locationAltitude = locationAltitude
        self.locationSatellites = locationSatellites
        self.airTemperature = airTemperature
        self.airHumidity = airHumidity
        self.waterContent = waterContent
        self.fieldCapacity = fieldCapacity
        self.leafMoisture = leafMoisture

    def __repr__(self) -> str:
        return (f"batConn:{self.batteryConnect}, batVolt:{self.batteryConnect}, lat:{self.locationLat}, "
                f"lng:{self.locationLng},alt:{self.locationAltitude},sat:{self.locationSatellites}, "
                f"airTemp:{self.airTemperature},airHumi:{self.airHumidity},soilMois:{self.waterContent}, "
                f"leafMois:{self.leafMoisture}")

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
            "waterContent": self.waterContent,
            "fieldCapacity": self.fieldCapacity,
            "leafMoisture": self.leafMoisture
        }
