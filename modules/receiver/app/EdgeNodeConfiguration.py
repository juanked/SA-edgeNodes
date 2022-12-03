class EdgeNodeConfiguration:

    def __init__(self, edgeNodeID, sensorID, sensorSerial, sensorLinearFit, plantationID, fieldCapacity, optimalWater):
        self.edgeNodeID = edgeNodeID
        self.sensorID = sensorID
        self.sensorSerial = sensorSerial
        self.sensorLinearFit = sensorLinearFit
        self.plantationID = plantationID
        self.fieldCapacity = fieldCapacity
        self.optimalWater = optimalWater

    def __repr__(self) -> str:
        return (f"edgeNodeID:{self.edgeNodeID}, sensorID:{self.sensorID}, sensorSerial:{self.sensorSerial}, "
                f"sensorLinearFit:{self.sensorLinearFit}, plantationID:{self.plantationID}, "
                f"fieldCapacity:{self.fieldCapacity}, optimalWater:{self.optimalWater}")
