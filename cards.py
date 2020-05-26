from globalconstants import *
from Bildermusicsounds import *
# Kartenarten
MUTATIONEN = 0
UMWELT = 1
LANDTIERE = 3
WASSERTIERE = 4
FLIEGER = 2

class Karte:
    def __init__(self):
        self.image = defaultKarte


class SpawnTier(Karte):
    def __init__(self, art, image, typ, anzahl=1):
        self.image = image
        self.type = typ
        self.art = art
        self.desc = "Spawne " + self.art
        self.anz = anzahl

    def spielen(self, execlass):
        for i in range(self.anz):
            execlass.tiere.append(self.art)


class Spawnfalcon(SpawnTier):
    def __init__(self):
        SpawnTier.__init__(self, "Falke", cardfalcon, "Flieger", 2)
        ##self.type = "Flieger"
    ##def spielen(self, game):
    ##game.tiere.append("Falke")


class Spawnbird(SpawnTier):
    def __init__(self):
        SpawnTier.__init__(self, "Singvogel", carddefault, "Flieger", 3)


class Spawnslug(SpawnTier):
    def __init__(self):
        SpawnTier.__init__(self, "Schnecke",
                           cardslug, "Landtier", 3)


class Spawncrab(SpawnTier):
    def __init__(self):
        SpawnTier.__init__(self, "Krabbe",
                           cardcrab, "Wassertier", 2)


class Spawnmouse(SpawnTier):
    def __init__(self):
        SpawnTier.__init__(self, "Maus",
                           cardmouse, "Landtier", 2)


class Spawnbug(SpawnTier):
    def __init__(self):
        SpawnTier.__init__(self, "Käfer",
                           cardbug, "Landtier", 3)


class Spawndoctorfish(SpawnTier):
    def __init__(self):
        SpawnTier.__init__(self, "Doktorfisch",
                           carddoctorfish, "Wassertier", 3)


class Spawnfox(SpawnTier):
    def __init__(self):
        SpawnTier.__init__(self, "Fuchs",
                           carddefault, "Landtier", 2)


class Spawnrabbit(SpawnTier):
    def __init__(self):
        SpawnTier.__init__(self, "Kaninchen",
                           carddefault, "Landtier", 2)


class Spawngoat(SpawnTier):
    def __init__(self):
        SpawnTier.__init__(self, "Ziege",
                           carddefault, "Landtier", 1)


class Getfast(Karte):
    def __init__(self):
        self.image = cardgetfast
        self.type = "Mutation"
        self.desc = "Geschwindigkeitsboost"

    def spielen(self, game):
        for i in range(3):
            game.mutations_list.append("MUTGETFAST")


class Fitnessboost(Karte):
    def __init__(self):
        self.image = cardfitnessboost
        self.type = "Mutation"
        self.desc = "Fitnessboost"

    def spielen(self, game):
        for i in range(3):
            game.mutations_list.append("MUTFITNESSBOOST")


class Powerboost(Karte):
    def __init__(self):
        self.image = cardpowerboost
        self.type = "Mutation"
        self.desc = "Powerboost"

    def spielen(self, game):
        for i in range(3):
            game.mutations_list.append("MUTPOWERBOOST")


class IntBoost(Karte):
    def __init__(self):
        self.image = cardintboost
        self.type = "Mutation"
        self.desc = "Intelligenzboost"

    def spielen(self, game):
        for i in range(3):
            game.mutations_list.append("MUTINTBOOST")


class EvasionBoost(Karte):
    def __init__(self):
        self.image = carddefault
        self.type = "Mutation"
        self.desc = "Evasionboost"

    def spielen(self, game):
        for i in range(3):
            game.mutations_list.append("MUTEVASIONBOOST")


class PrecisionBoost(Karte):
    def __init__(self):
        self.image = carddefault
        self.type = "Mutation"
        self.desc = "Precisionboost"

    def spielen(self, game):
        for i in range(3):
            game.mutations_list.append("MUTPRECISIONBOOST")


class Getflying(Karte):
    def __init__(self):
        self.image = cardgetflying
        self.type = "Mutation"
        self.desc = "fliegt"

    def spielen(self, game):
        game.mutations_list.append("MUTGETFLYING")


class EventKarte(Karte):
    def __init__(self):
        pass


class Meteorshower(Karte):
    def __init__(self):
        self.image = cardmeteorshower
        self.type = "Umwelt"
        self.desc = "Meteorschauer"
        self.targeting = "NONE"

    def spielen(self, execlass):
        execlass.doevent("Meteor")


class Heatwave(Karte):
    def __init__(self):
        self.image = carddefault
        self.type = "Umwelt"
        self.desc = "Hitzewelle"
        self.targeting = "NONE"

    def spielen(self, execlass):
        execlass.doevent("Heatwave")


class Coolwave(Karte):
    def __init__(self):
        self.image = carddefault
        self.type = "Umwelt"
        self.desc = "Kältewelle"
        self.targeting = "NONE"

    def spielen(self, execlass):
        execlass.doevent("Coolwave")


class Granade(Karte):
    def __init__(self):
        self.image = carddefault
        self.type = "Umwelt"
        self.desc = "Granate"
        self.targeting = "TILE"
        self.targetNbr = 1

    def spielen(self, execlass, targets):
        execlass.doevent("Granade", targets)

KARTEN_VORHANDEN = {MUTATIONEN: [Getfast, Fitnessboost, EvasionBoost, PrecisionBoost, IntBoost],
                    UMWELT: [Meteorshower, Heatwave, Coolwave, Granade],
                    LANDTIERE: [Spawnslug, Spawnmouse, Spawnbug, Spawnfox, Spawnrabbit, Spawngoat],
                    WASSERTIERE: [Spawndoctorfish, Spawncrab], FLIEGER: [Spawnfalcon, Spawnbird]}

