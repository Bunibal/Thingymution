import socket, pickle
#Konstanten für Kommunikation
SPAWNTIER = 0
GIVEMUTATION = 1
DOEVENT = 2
MOUSETILE = 3
KILLSERVER = 322

NOTURN = 100
TURN = 101
GAMEOVER = 102

class Network:
    def __init__(self, serverIp):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = serverIp
        self.port = 5555
        self.addr = (self.server, self.port)
        self.startInfo = self.connect()

    def getStartInfo(self):
        return self.startInfo

    def connect(self):
        self.client.connect(self.addr)
        try:
            msg = pickle.loads(self.client.recv(4096*128))
        except:
            print("Fehler: Zu viele Daten")
            msg = None
        return msg
        ##return self.recvData()

    def recvData(self):
        print("receiving data")
        data = []
        i = 0
        while True:
            packet = self.client.recv(4096)
            i +=1
            if not packet: break
        print("Anzahl Pckges:", i)
        data.append(packet)
        data_arr = pickle.loads(b"".join(data))
        return data_arr
        ##except:
        ##    print("Connection could not be established")

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            data = self.client.recv(4096*128)
        except socket.error as e:
            print(e)
        try:
            msg = pickle.loads(data)
        except:
            msg = None
        return msg
