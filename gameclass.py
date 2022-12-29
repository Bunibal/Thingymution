from animals import *
from gameconstants import *
from terrainstats import *
from Bildermusicsounds import MAPFILES
from skilltreeclass import *

import numpy as np


def getTileTerrainAndSet(map, pos, layer=3, schonGefunden=[-1, -1, -1, -1]):
    try:
        props = map.get_tile_properties(pos[0], pos[1], layer)
    except:
        print(pos, layer, "gibt er Fehler bei get_tile properties")
    if props == None and layer >= 0:
        return getTileTerrainAndSet(map, pos, layer - 1, schonGefunden[:])
    terrStr = props["terrain"].split(",")
    terrains = schonGefunden[:]
    for i in range(4):
        if terrains[i] == -1 and terrStr[i] != "":
            terrains[i] = TERRAIN[getTileSet(map, pos[0], pos[1], layer)][int(terrStr[i])]
    if -1 in terrains:
        return getTileTerrainAndSet(map, pos, layer - 1, terrains)
    return terrains


def getTileSet(mapFile, x, y, layer=0):
    gid = mapFile.get_tile_gid(x, y, layer)
    if gid != 0:
        return mapFile.get_tileset_from_gid(gid).name
    return None


def createListofLists(x, y, initValue=0):
    l = []
    for i in range(x):
        l.append(y * [initValue])
    return l


class Modifier:
    def __init__(self, effectType, starttime, duration=-1):
        self.effectType, self.starttime, self.duration = effectType, starttime, duration


class TempModifier(Modifier):
    def __init__(self, starttime, duration, amount, location):
        Modifier.__init__(self, "MODTEMPCHANGE", starttime, duration)
        self.amount, self.location = amount, location
        self.rect = pygame.rect.Rect(location)


# Spiel, animieren
class Game:
    def __init__(self, mapNr):
        self.mapFile, self.tilenbr = MAPFILES[mapNr]
        self.tilenbrx, self.tilenbry = self.tilenbr
        self.frames = 0
        self.tileMatrix = createListofLists(self.tilenbrx, self.tilenbry, 0)
        self.livingThings = []
        for x in range(self.tilenbrx):
            for y in range(self.tilenbry):
                self.tileMatrix[x][y] = {"PflanzenEssen": 0, "FrischFleisch": [], "Lebewesen": [],
                                         "Terrain": getTileTerrainAndSet(self.mapFile, (x, y))}
        self.terrainFoodRegen = np.zeros((self.tilenbrx, self.tilenbry))
        for x in range(self.tilenbrx):
            for y in range(self.tilenbry):
                terrains = self.tileMatrix[x][y]["Terrain"]
                mean = sum([PLANTGROWTH[t] for t in terrains]) / 4
                self.terrainFoodRegen[x, y] = mean
        self.pflanzenMenge = [np.zeros((self.tilenbrx, self.tilenbry)),
                              np.zeros((self.tilenbrx, self.tilenbry)),
                              np.zeros((self.tilenbrx, self.tilenbry))]
        # Von klein nach Gross geordnet
        self.mutations_list = []
        self.creatureIdCount = 0
        self.modifiers = []
        self.notifications = []
        self.unlockedMutations = []

    def levelmenu(self):
        pass

    def step(self):
        self.frames += 1
        self.pflanzenRegenerieren(1)
        for obj in self.livingThings[:]:
            if obj.alive:
                obj.everyFrame()
            if not obj.alive:
                self.livingThings.remove(obj)
                self.tileMatrix[obj.tile[0]][obj.tile[1]]["Lebewesen"].remove(obj)
        for mod in self.modifiers[:]:
            if mod.duration >= 0 and (self.frames - mod.starttime) >= mod.duration * FPSGAME:
                print(mod.effectType, "has ended")
                self.modifiers.remove(mod)

    def addCreature(self, type, startpos, player=-1, startangle=None, info=None):
        newCreature = type(self, startpos, startangle, info)
        newCreature.id = self.creatureIdCount
        newCreature.player = player
        self.creatureIdCount += 1
        self.livingThings.append(newCreature)
        self.sendNotification("Tier gespawnt", newCreature.desc)
        return newCreature

    def addModifier(self, effectType, duration=-1):
        mod = Modifier(effectType, self.frames, duration)
        self.modifiers.append(mod)

    def addTempModifier(self, amount, location, duration=-1):
        mod = TempModifier(self.frames, duration, amount, location)
        self.modifiers.append(mod)

    def getPflanzenEssen(self, tile, groesse = "ges"):
        if groesse == "ges":
            return sum(art[tile[0], tile[1]] for art in self.pflanzenMenge)
        return self.pflanzenMenge[groesse][tile[0], tile[1]]

    def setPflanzenEssen(self, tile, amount, size):
        self.pflanzenMenge[size][tile[0], tile[1]] = amount

    def essePflanzen(self, tile, amount, size):
        self.setPflanzenEssen(tile, self.getPflanzenEssen(tile) - amount, size)

    def getFrischFleischInfo(self, tile):
        return self.tileMatrix[tile[0]][tile[1]]["FrischFleisch"]

    def getFrischFleischMenge(self, tile, arten):
        gefunden = 0
        for stueck in self.getFrischFleischInfo(tile):
            if stueck[1] in arten:
                gefunden += stueck[3]
        return gefunden

    def getTemp(self, terrain, tile):
        extra = 0
        for mod in self.modifiers:
            if mod.effectType == "MODTEMPCHANGE" and mod.rect.collidepoint(tile):
                extra += mod.amount
        return TEMP[terrain] + extra

    # Frisst fleisch von den moeglichen Arten, gibt zurueck wieviel gegessen wurde
    def macheZuEssen(self, obj, menge):
        if menge > obj.popGroesse:
            print("Warnung! Zuviel zu essen gemacht!")
        obj.changePop(-menge)
        tilex, tiley = getTile(obj.getPos())
        self.tileMatrix[tilex][tiley]["FrischFleisch"].append([self.frames, obj.desc, 0, menge * obj.groesse])

    def kampfaustragen(self, objekte1, objekte2, menge):
        prec1, ev2 = objekte1.getPrecision(), objekte2.getEvasion()
        if prec1 >= ev2:
            evchance = np.power(2.0, ev2 - prec1)
        else:
            evchance = 1 - np.power(2.0, prec1 - ev2)
        if random.random() > evchance:  # If not evaded
            if objekte1.staerke > objekte2.staerke:
                self.macheZuEssen(objekte2, menge)

            elif objekte2.staerke > objekte1.staerke:
                self.macheZuEssen(objekte1, menge)
            else:
                tode1 = np.random.binomial(menge, 0.5)
                self.macheZuEssen(objekte2, tode1)
                self.macheZuEssen(objekte2, menge - tode1)
        else:
            print(objekte1.desc, "evades", objekte2.desc)

    def pflanzenRegenerieren(self, frames):
        # for x in range(section, self.tilenbrx, numberofSections):
        #     for y in range(self.tilenbry):
        #         terrains = self.tileMatrix[x][y]["Terrain"]
        #         mean = sum([PLANTGROWTH[t] for t in terrains]) / 4
        #         essen = self.getPflanzenEssen((x, y))
        #         neuEssen = min(mean * MAXPFLANZEN, essen + mean * PFLANZENREGENERATION)
        #         self.tileMatrix[x][y]["PflanzenEssen"] = neuEssen
        added = self.pflanzenMenge[0] + \
                self.terrainFoodRegen * PFLANZENREGENERATION * frames / FPSGAME
        self.pflanzenMenge[0] = np.minimum(self.terrainFoodRegen * MAXPFLANZEN, added)

    def getLivingThingsInTile(self, tile):
        if not ((0 <= tile[0] < self.tilenbrx) and (0 <= tile[1] < self.tilenbry)):
            return []
        return self.tileMatrix[tile[0]][tile[1]]["Lebewesen"]

    def getTerrain(self, pos, mapCoords=True):
        if not mapCoords:
            pos = self.getMapPos(pos)
        x, y = mult(pos, 1 / 16, True)
        x1, y1 = mult(pos, 1 / 8, True)
        xx, yy = x1 % 2, y1 % 2
        return self.tileMatrix[x][y]["Terrain"][xx + 2 * yy]

    def giveMutation(self, creatureId, mutation):
        target = self.getCreatureById(creatureId)
        if target == None:
            return False
        target.addMutation(mutation)

    def mutate(self, creatureId, player):
        creature = self.getCreatureById(creatureId)
        indizes = creature.skilltreepos
        new = newMutationAndPos(skilltreeslug, indizes)
        if new == None:
            return
        newMutation, newIndizes = new
        if self.isUnlocked(newIndizes, player):
            creature.addMutation(newMutation)
            creature.skilltreepos = newIndizes
        else:
            self.sendNotification("IDK", f"Mutation nicht freigeschalten, {new}, {player}, {self.unlockedMutations[player]}")

    def unlockMutation(self, skilltreepos, playerNbr):
        self.unlockedMutations[playerNbr].append(skilltreepos)

    def isUnlocked(self, skilltreepos, playerNbr):
        return skilltreepos in self.unlockedMutations[playerNbr]

    # noch recht slow weil ich faul bin

    def getCreatureById(self, id):
        for c in self.livingThings:
            if c.id == id:
                return c
        return None

    def encodeGameState(self, tile, animalIds):
        stateall = [(obj.desc, obj.getPos(), obj.popGroesse,
                     obj.id, obj.player, obj.imFlug) for obj in self.livingThings]
        if (0 <= tile[0] < self.tilenbrx) and (0 <= tile[1] < self.tilenbry):
            stateextra = [self.getPflanzenEssen(tile)] + [(obj.desc, obj.getPos(), obj.popGroesse,
                                                          obj.id, obj.player, obj.imFlug,
                                                          obj.hunger, obj.getFitness(),
                                                           obj.getMutationNames()) for obj in
                                                         self.livingThings
                                                         if obj.id in animalIds or obj.tile == tile]
        else:
            stateextra = [None]
        return (stateall, stateextra)

    def addPlayer(self):
        self.unlockedMutations.append([])

    def retrieveNotifications(self):
        nots = self.notifications
        self.notifications = []
        return nots

    def sendNotification(self, type, content = None):
        self.notifications.append((type, content))

    def getpoints(self, players, amount):
        playerPts = players * [0]
        for tier in self.livingThings:
            if tier.player != -1:
                playerPts[tier.player] += (amount[tier.desc] * tier.popGroesse)
        return playerPts

    # Events die durch Karten ausgelöst werden können
    def meteorShower(self, targetDummy=None):
        for tier in self.livingThings:
            alter = self.frames - tier.geboren
            if random.randint(1, DEADDUDESMETEOR) == 1 and alter > 0:
                tier.alive = False

    def heatWave(self, targetDummy=None):
        self.addTempModifier(HEATWAVEAMOUNT, (0, 0, 200, 200), HEATWAVEDURATION)

    def coolWave(self, targetDummy=None):
        self.addTempModifier(COOLWAVEAMOUNT, (0, 0, 200, 200), COOLWAVEDURATION)

    def granade(self, targets):
        target = targets[0]
        for tier in self.livingThings:
            alter = self.frames - tier.geboren
            if pInRect(tier.tile, (target[0], target[1], 4, 4)) and alter > 0:
                tier.alive = False


if __name__ == "__main__":
    def createAndMonitor(typ, pos, mutations=[], steps=2000, printint=200):
        cr = game.addCreature(typ, pos)
        for mut in mutations:
            cr.mutationen.append(mut)
        for i in range(steps):
            game.step()
            if game.frames % printint == 0:
                print(cr.getPos(), cr.popGroesse, cr.hunger)
        print("Anzahl:", len(game.livingThings))


    def doSteps(n):
        for i in range(n):
            game.step()


    game = Game(0)
    for i in range(999):
        game.addCreature(Schnecke, (200, 1200))
    createAndMonitor(Schnecke, (200, 1200),
                     ["MUTGETFAST", "MUTFITNESSBOOST", "MUTFITNESSBOOST", "MUTFITNESSBOOST", "MUTFITNESSBOOST"],
                     steps=5000)
    game = Game()
    createAndMonitor(Schnecke, (200, 1200), ["MUTFITNESSBOOST", "MUTGETFAST"], steps=5000)
    game = Game()
    createAndMonitor(Schnecke, (200, 1200), ["MUTGETFAST"], steps=5000)
    game = Game()
    createAndMonitor(Schnecke, (200, 1200), ["MUTFITNESSBOOST"], steps=5000)
