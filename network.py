import pickle
import socket


class Network:
    def __init__(self, serverIp):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = serverIp
        self.port = 5555
        self.addr = (self.server, self.port)
        self.startInfo = self.connect()
        self.msgId = 0

    def getStartInfo(self):
        return self.startInfo

    def connect(self):
        self.client.connect(self.addr)
        try:
            msg = pickle.loads(self.client.recv(4096 * 128))
        except:
            print("Fehler: Zu viele Daten")
            msg = None
        return msg

    def recvData(self):
        print("receiving data")
        data = []
        i = 0
        while True:
            packet = self.client.recv(4096)
            i += 1
            if not packet: break
        print("Anzahl Pckges:", i)
        data.append(packet)
        data_arr = pickle.loads(b"".join(data))
        return data_arr

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
        except socket.error as e:
            print(e)
        success = False
        while not success:
            try:
                data = self.client.recv(4096 * 128)
            except socket.error as e:
                print(e)
                self.client.send(pickle.dumps("Error"))
                continue
            try:
                msg = pickle.loads(data)
            except:
                self.client.send(pickle.dumps("Error"))
                continue
            msg = self.interpretMsg(msg)
            if msg:
                success = True
        return msg

    def interpretMsg(self, incMsg):
        if incMsg is not None:
            try:
                action = incMsg[0]
                points = incMsg[1][0]
                playerCount = incMsg[1][1]
                gameInfo = incMsg[2]
                plantFoodInTile = incMsg[3][0]
                objectInfoInTile = incMsg[3][1:]
                notifications = incMsg[4]
            except:
                print(incMsg, "does not have the right format.")
                return False

        else:
            print("Empfangene Information fehlerhaft")
            return False
        return action, points, playerCount, gameInfo, plantFoodInTile, objectInfoInTile, notifications
