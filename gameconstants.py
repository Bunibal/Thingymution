# Spielmodifier
FPSGAME = 30
BIGSTEPEVERY = 3
CFPSGAME = FPSGAME / BIGSTEPEVERY
PFLANZENSECTIONS = 2 * int(CFPSGAME)
SEKUNDENZUG = 30
GAMELENGTH = 600
SEKUNDENPUNKTE = 15

HANDKARTEN = 6
STONEGEWICHTUNG = 4
STEINEANZAHL = 5
ANZAHLKARTENSPIELEN = 3

# menu
FPSMENU = 60

# Modellfaktoren
TODFAKTOR = 0.005
TEMPANPASSKOEFF = 0.01  # Wie stark Temperaturanpassung sich auf die Fitness auswirkt
ANGRIFFHUNGER = 0.1
PFLANZENREGENERATION = 0.1
MAXPFLANZEN = 2
ANPASSUNGSEKUNDEN = 30
ANPASSUNGSCHANCE = 3

# Kartenarten
MUTATIONEN = 0
UMWELT = 1
LANDTIERE = 3
WASSERTIERE = 4
FLIEGER = 2


# Umwelkartenstats
DEADDUDESMETEOR = 5
HEATWAVEAMOUNT = 20
HEATWAVEDURATION = 60
COOLWAVEAMOUNT = 20
COOLWAVEDURATION = 60

# Konstanten für Kommunikation
# Client to server
SPAWNTIER = 0
GIVEMUTATION = 1
DOEVENT = 2
MOUSETILE = 3
ADVANCE = 4
INFOANIMALS = 5
UNLOCK = 6
KILLSERVER = 322
#Server to client
NOTURN = 100
TURN = 101
GAMEOVER = 102
