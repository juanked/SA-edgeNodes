class ActuatorConfiguration:
    def __init__(self, actuatorID, actuatorSerial):
        self.actuatorID = actuatorID
        self.actuatorSerial = actuatorSerial

    def __repr__(self) -> str:
        return (f"actuatorID:{self.actuatorID}, actuatorSerial:{self.actuatorSerial}")
