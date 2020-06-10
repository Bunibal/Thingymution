from Bildermusicsounds import *
from mutations import *

class Karte:
    def __init__(self):
        self.image = carddefault
        self.showAOE = False


class SpawnTier(Karte):
    def __init__(self, art, image, typ, anzahl=1):
        super().__init__()
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
        super().__init__()
        self.image = cardgetfast
        self.type = "Mutation"
        self.desc = "Geschwindigkeitsboost"

    def spielen(self, game):
        for i in range(3):
            game.mutations_list.append(getFast)


class Fitnessboost(Karte):
    def __init__(self):
        super().__init__()
        self.image = cardfitnessboost
        self.type = "Mutation"
        self.desc = "Fitnessboost"

    def spielen(self, game):
        for i in range(3):
            game.mutations_list.append(getFitness)


class Powerboost(Karte):
    def __init__(self):
        super().__init__()
        self.image = cardpowerboost
        self.type = "Mutation"
        self.desc = "Powerboost"

    def spielen(self, game):
        for i in range(3):
            game.mutations_list.append(getPower) # Existiert noch nicht


class IntBoost(Karte):
    def __init__(self):
        super().__init__()
        self.image = cardintboost
        self.type = "Mutation"
        self.desc = "Intelligenzboost"

    def spielen(self, game):
        for i in range(3):
            game.mutations_list.append(getInt)


class EvasionBoost(Karte):
    def __init__(self):
        super().__init__()
        self.image = carddefault
        self.type = "Mutation"
        self.desc = "Evasionboost"

    def spielen(self, game):
        for i in range(3):
            game.mutations_list.append(getEvasion)


class PrecisionBoost(Karte):
    def __init__(self):
        super().__init__()
        self.image = carddefault
        self.type = "Mutation"
        self.desc = "Precisionboost"

    def spielen(self, game):
        for i in range(3):
            game.mutations_list.append(getPrecision)


class Getflying(Karte):
    def __init__(self):
        super().__init__()
        self.image = cardgetflying
        self.type = "Mutation"
        self.desc = "fliegt"

    def spielen(self, game):
        game.mutations_list.append(getFlying)

class Mutate(Karte):
    def __init__(self):
        super(Mutate, self).__init__()
        self.image = carddefault
        self.type = "Umwelt"
        self.desc = "Granate"
        self.targeting = "TILE"
        self.targetNbr = 1

class EventKarte(Karte):
    def __init__(self):
        pass


class Meteorshower(Karte):
    def __init__(self):
        super(Meteorshower, self).__init__()
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
        self.showAOE = True
        self.aoe = (4,4)

    def spielen(self, execlass, targets):
        execlass.doevent("Granade", targets)


    def spielen(self, execlass, targets):
        execlass.doevent("Granade", targets)
