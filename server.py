from gameclass import *
from _thread import *
from pygame.time import Clock
from gameelements import TIERE, EVENTS, POINTS
from network import *

pygame.quit() # weil pygame gestartet wird
TIERCAP = 10000

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
print("ip Adresse: ", IPAddr)
server = IPAddr
port = 5555
mapNr = int(input("Map:"))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")
game = Game(mapNr)
activePlayers = []
forcePausing = []
doingTurn = []
gameover = False
over = False
points = []
notifications = []


def threaded_simulation():
    global forcePausing, over, points, gameover, notifications
    print("Simulation gestartet")
    uhr = Clock()
    gameLaeuft = True
    while gameLaeuft:
        uhr.tick(20)
        if not isBlocking():
            game.step()
            if game.frames >= 20 * GAMELENGTH:
                print("Gameaus")
                print(points)
                gameover = True
            elif game.frames % (20 * SEKUNDENZUG) == 0:
                forcePausing = playerCount * [True]
            if game.frames % (20 * SEKUNDENPUNKTE) == 0:
                pointsRN = game.getpoints(playerCount, POINTS)
                for i in range(len(points)):
                    points[i] += pointsRN[i]
        newNots = game.retrieveNotifications()
        for notf in newNots:
            for plI in activePlayers:
                notifications[plI].append(notf)
        if game.frames % 100 == 1:
            print("Game Laeuft, Kreaturen:", len(game.livingThings))


def isBlocking():
    if True in [forcePausing[i] for i in activePlayers]:
        return True
    if True in [doingTurn[i] for i in activePlayers]:
        return True
    return False


def threaded_client(conn, player):
    global forcePausing, over, doingTurn
    conn.send(pickle.dumps((player, mapNr)))
    print("Player %i joined" % player)
    reply = ""
    tile = (0, 0)
    infoAnimals = []
    error = False # Sent information had errors
    while True:
        try:
            data = conn.recv(2048)
        except:
            print("Disconnected")
            activePlayers.remove(player)
            break
        if not data:
            print("Disconnected")
            activePlayers.remove(player)
            break
        else:
            try:
                msg = pickle.loads(data)
            except:
                msg = [False]
                print("Couldn't unpickle")
            if msg == "Error":
                error = True
            else:
                amKartenSpielen = msg[0]
                doingTurn[player] = amKartenSpielen
                for i in range(1, len(msg)):
                    if msg[i][0] == SPAWNTIER:
                        for j in range(msg[i][3]):
                            game.addCreature(TIERE[msg[i][1]], msg[i][2], player)
                    elif msg[i][0] == GIVEMUTATION:
                        game.giveMutation(msg[i][1], msg[i][2])
                    elif msg[i][0] == DOEVENT:
                        EVENTS[msg[i][1]](game, msg[i][2])
                    elif msg[i][0] == MOUSETILE:
                        tile = msg[i][1]
                    elif msg[i][0] == ADVANCE:
                        game.mutate(msg[i][1])
                    elif msg[i][0] == INFOANIMALS:
                        infoAnimals = msg[i][1]
                    elif msg[i][0] == KILLSERVER:
                        over = True
        if not error: # If error, the same msg will be sent again
            msgTo = msgToClient(player, tile, infoAnimals)
        conn.sendall(pickle.dumps(msgTo))

    print("Lost connection")
    conn.close()


def msgToClient(player, tilemouse, infoAnimals):
    global forcePausing
    startturn = forcePausing[player]
    if startturn:
        forcePausing[player] = False
    stateall, statetile = game.encodeGameState(tilemouse, infoAnimals)
    sendNots = notifications[player]
    notifications[player] = notifications[player][len(sendNots):] # um keine notifications zu verlieren
    if len(stateall) > TIERCAP:
        stateall = stateall[:TIERCAP]
        print("Warnung: Zu viele Tiere")
    if gameover:
        action = GAMEOVER
    elif startturn:
        action = TURN
    else:
        action = NOTURN
    return [action, (points, playerCount), stateall, statetile, sendNots]

playerCount = 0
s.settimeout(10)
while True:
    print("Now listening to connections")
    connfound = True
    try:
        conn, addr = s.accept()
    except:
        connfound = False
    if connfound:
        print("Connected to:", addr)
        if playerCount == 0:
            start_new_thread(threaded_simulation, ())

        activePlayers.append(playerCount)
        doingTurn.append(False)
        forcePausing.append(True)
        points.append(0)
        notifications.append([])
        start_new_thread(threaded_client, (conn, playerCount))
        playerCount += 1
    if over:
        break
