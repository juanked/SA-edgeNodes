class MQTTConnection:

    def __init__(self, id: str, name: str, host: str, port: int, clientID: str, username: str, pwd: str):
        self.id = id
        self.name = name
        self.host = host
        self.port = port
        self.clientID = clientID
        self.username = username
        self.pwd = pwd

    def __repr__(self) -> str:
        return (f"host:{self.host}, port:{self.port}, "
                f"clientID:{self.clientID}, username:{self.username}, pwd:{self.pwd}")
