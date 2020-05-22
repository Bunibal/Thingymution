#letzte Änderung:14.04.2020
#Sebastian Bittner, Stephan Buchner
SZABTEST = False
import pygame, random, sys, os, math, pytmx, numpy as np
from terrainstats import *
from helpfunctions import *
from animals import *

os.chdir(os.getcwd() + "/resources")
if True:# global variables
    FPSGAME = 20
    TERRAIN = {"hexagonal1":(RIVER, FOREST, RIVERBANK, DIRT, GREENFIELD),
        "berge": (HIGHMOUNTAIN, SNOWYMOUNTAIN), "grass":(DESERT, HILLS, STEPPE),
        "overworld": (FOREST1, LOWMOUNTAINS),"water": (OCEAN,),
        "watergrasssand": (COASTWATER, BEACH, COASTGRASS)}
    POINTS = {"Maus": 4, "Schnecke":1, "Krabbe": 1,
                "Doktorfisch": 1, "Falke": 9, "Käfer":1, "Fuchs": 10,
                "Kaninchen": 4, "Ziege": 20, "Singvogel": 3}
    mapFile0 = pytmx.TiledMap("maplvl1.tmx")
    mapFileKleiner = pytmx.TiledMap("maplvl2.tmx")
    MAPFILES = [(mapFile0, (200, 200)), (mapFileKleiner, (60,60))]
    SEKUNDENZUG = 30
    GAMELENGTH = 600
    SEKUNDENPUNKTE = 15
    POPANPASSENINTERVAL = 1 #soviele Frames pro populationAnpassen
    if True:#Modellfaktoren
        TODFAKTOR = 0.005
        TEMPANPASSKOEFF = 0.01 # Wie stark Temperaturanpassung sich auf die Fitness auswirkt
        ANGRIFFHUNGER = 0.1
        PFLANZENREGENERATION = 0.1
        MAXPFLANZEN = 2
        ANPASSUNGSEKUNDEN = 30
        ANPASSUNGSCHANCE = 3

        #Mutationenstats
        GETFASTBONUS = 0.2
        FITNESSBOOSTBONUS = 0.2
        EVASIONBOOSTBONUS = 1
        PRECISIONBOOSTBONUS = 1
        INTBOOSTBONUS = 1
        INTBOOSTMULT = 2
# Umwelkartenstats
        DEADDUDESMETEOR = 5
        HEATWAVEAMOUNT = 20
        HEATWAVEDURATION = 60
        COOLWAVEAMOUNT = 20
        COOLWAVEDURATION = 60


# Tiere, Objekte
# Ereignisse

def getTileTerrainAndSet(map, pos, layer = 3, schonGefunden = [-1,-1,-1,-1]):
    try:
        props = map.get_tile_properties(pos[0],pos[1],layer)
    except:
        print(pos,layer,"gibt er Fehler bei get_tile properties")
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

def getTileSet(mapFile, x,y, layer = 0):
    gid = mapFile.get_tile_gid(x,y,layer)
    if gid != 0:
        return mapFile.get_tileset_from_gid(gid).name
    return None

def createListofLists(x,y, initValue = 0):
    l = []
    for i in range(x):
        l.append(y*[initValue])
    return l


#schneidet ein Bild zu, und skaliert es


#Landschaft



class Modifier:
    def __init__(self, effectType,starttime, duration = -1):
        self.effectType, self.starttime, self.duration = effectType,starttime, duration

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
            self.tileMatrix[x][y] = {"PflanzenEssen" : 0, "FrischFleisch":[], "Lebewesen":[],
            "Terrain":getTileTerrainAndSet(self.mapFile, (x,y))}
    self.mutations_list = []
    self.creatureIdCount = 0
    self.modifiers = []


  def levelmenu(self):
    pass

  def step(self):
    self.frames +=1
    self.pflanzenRegenerieren(self.frames%FPSGAME, FPSGAME)
    for obj in self.livingThings[:]:
        if obj.alive:
            obj.everyFrame()
        if not obj.alive:
            self.livingThings.remove(obj)
            self.tileMatrix[obj.tile[0]][obj.tile[1]]["Lebewesen"].remove(obj)
    for mod in self.modifiers[:]:
        if mod.duration >= 0 and (self.frames-mod.starttime) >= mod.duration * FPSGAME:
            print(mod.effectType, "has ended")
            self.modifiers.remove(mod)



 #NEUERZUG ###################################################################################################################



  def addCreature(self, type, startpos, player = -1, startangle = None, info = None):
      newCreature = type(self, startpos, startangle, info)
      newCreature.id = self.creatureIdCount
      newCreature.player = player
      self.creatureIdCount += 1
      self.livingThings.append(newCreature)
      return newCreature

  def addModifier(self, effectType, duration = -1):
      mod = Modifier(effectType, self.frames, duration)
      self.modifiers.append(mod)

  def addTempModifier(self, amount, location, duration = -1):
      mod = TempModifier(self.frames, duration, amount, location)
      self.modifiers.append(mod)

  def getPflanzenEssen(self,tile):
      return self.tileMatrix[tile[0]][tile[1]]["PflanzenEssen"]

  def setPflanzenEssen(self, tile, essen):
      self.tileMatrix[tile[0]][tile[1]]["PflanzenEssen"] = essen

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

#Frisst fleisch von den moeglichen Arten, gibt zurueck wieviel gegessen wurde


  def macheZuEssen(self, obj, menge):
      if menge > obj.popGroesse:
          print("Warnung! Zuviel zu essen gemacht!")
      obj.changePop(-menge)
      tilex, tiley = getTile(obj.getPos())
      self.tileMatrix[tilex][tiley]["FrischFleisch"].append([self.frames,obj.desc, 0, menge*obj.groesse])

  def kampfaustragen(self, objekte1, objekte2, menge):
      prec1, ev2 = objekte1.getPrecision(), objekte2.getEvasion()
      if prec1 >= ev2:
          evchance = np.power(2.0,ev2-prec1)
      else:
          evchance = 1 - np.power(2.0,prec1 - ev2)
      if random.random() > evchance: # If not evaded
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

  def pflanzenRegenerieren(self, section, numberofSections):
      for x in range(section, self.tilenbrx, numberofSections):
          for y in range(self.tilenbry):
              terrains = self.tileMatrix[x][y]["Terrain"]
              mean = sum([PLANTGROWTH[t] for t in terrains])/4
              essen = self.getPflanzenEssen((x,y))
              neuEssen = min(mean*MAXPFLANZEN, essen + mean * PFLANZENREGENERATION)
              self.tileMatrix[x][y]["PflanzenEssen"]  = neuEssen


  def getLivingThingsInTile(self, tile):
      if not ((0 <= tile[0] < self.tilenbrx) and (0 <= tile[1] < self.tilenbry)):
          ##print("Warnung: Tile gibts nicht!")
          return []
      return self.tileMatrix[tile[0]][tile[1]]["Lebewesen"]



  def getTerrain(self,pos, mapCoords = True):
      if not mapCoords:
          pos = self.getMapPos(pos)
      x,y = mult(pos, 1/16, True)
      x1,y1 = mult(pos, 1/8, True)
      xx, yy = x1%2, y1%2
      return self.tileMatrix[x][y]["Terrain"][xx+2*yy]

  def giveMutation(self, creatureId, mutation):
      target = self.getCreatureById(creatureId)
      if target == None:
          return False
      target.mutationen.append(mutation)

# noch recht slow weil ich faul bin
  def getCreatureById(self, id):
      for c in self.livingThings:
          if c.id == id:
              return c
      return None

  def encodeGameState(self, tile):
      stateall = [(obj.desc, obj.getPos(), obj.popGroesse,
                obj.id, obj.player, obj.imFlug) for obj in self.livingThings]
      if ((0 <= tile[0] < self.tilenbrx) and (0 <= tile[1] < self.tilenbry)):
          statetile = [self.getPflanzenEssen(tile)] + [(obj.desc, obj.getPos(), obj.popGroesse,
                obj.id, obj.player, obj.imFlug,
                    obj.hunger, obj.getFitness(), obj.mutationen) for obj in self.livingThings
                if obj.tile == tile]
      else:
          statetile = [None]
      return (stateall, statetile)

  def getpoints(self, players, amount):
      playerPts = players * [0]
      for tier in self.livingThings:
          if tier.player != -1:
              playerPts[tier.player] +=(amount[tier.desc] * tier.popGroesse)
      return playerPts

# Events die durch Karten ausgelöst werden können
  def meteorShower(self, targetDummy = None):
      for tier in self.livingThings:
          alter = self.frames - tier.geboren
          if random.randint(1,DEADDUDESMETEOR) == 1 and alter > 0:
              tier.alive = False

  def heatWave(self, targetDummy = None):
      self.addTempModifier(HEATWAVEAMOUNT,(0,0,200,200), HEATWAVEDURATION)

  def coolWave(self, targetDummy = None):
      self.addTempModifier(COOLWAVEAMOUNT,(0,0,200,200), COOLWAVEDURATION)

  def granade(self, targets):
      target = targets[0]
      for tier in self.livingThings:
          alter = self.frames - tier.geboren
          if pInRect(tier.tile, (target[0],target[1], 4 ,4)) and alter > 0:
              tier.alive = False



#some Konstanten und Listen

#BUTTONSGAME = {"Maus":Maus, "Schnecke":Schnecke, "Krabbe": Krabbe,
#    "Doktorfisch": Doktorfisch, "Falke": Falke, "Käfer":Kaefer,
#    "Fuchs":Fuchs}
TIERE = {"Maus":Maus, "Schnecke":Schnecke, "Krabbe": Krabbe,
    "Doktorfisch": Doktorfisch, "Falke": Falke, "Singvogel": Singvogel,
    "Käfer":Kaefer, "Fuchs":Fuchs, "Kaninchen": Kaninchen,
    "Ziege": Ziege,}
EVENTS = {"Meteor": Game.meteorShower, "Coolwave": Game.coolWave,
        "Heatwave":Game.heatWave, "Granade": Game.granade}
ZUGBUTTONS =["Mutationen","Umwelt","Flieger","Landtiere","Wassertiere"]

if __name__ == "__main__":
    def createAndMonitor(typ, pos, mutations = [], steps = 2000, printint = 200):
        cr = game.addCreature(typ, pos)
        for mut in mutations:
            cr.mutationen.append(mut)
        for i in range(steps):
            game.step()
            if game.frames%printint == 0:
                print(cr.getPos(), cr.popGroesse, cr.hunger)
        print("Anzahl:", len(game.livingThings))
    def doSteps(n):
        for i in range(n):
            game.step()
    game = Game()
    createAndMonitor(Schnecke, (200,1200),
        ["MUTGETFAST", "MUTFITNESSBOOST", "MUTFITNESSBOOST", "MUTFITNESSBOOST","MUTFITNESSBOOST"],
         steps = 5000)
    game = Game()
    createAndMonitor(Schnecke, (200,1200), ["MUTFITNESSBOOST", "MUTGETFAST"], steps = 5000)
    game = Game()
    createAndMonitor(Schnecke, (200,1200), ["MUTGETFAST"], steps = 5000)
    game = Game()
    createAndMonitor(Schnecke, (200,1200), ["MUTFITNESSBOOST"], steps = 5000)
##    anzM = input("Wieviele Mäuse?")
##    for i in range(int(anzM)):
##        game.addCreature(Maus, (random.randint(0,1000), 1500))
##    while True:
##        schritte = input("Schritte:")
##        try:
##            for i in range(int(schritte)):
##                game.step()
##        except:
##            break
##        print("Kreaturen:", len(game.livingThings))