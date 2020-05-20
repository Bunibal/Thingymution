#letzte Änderung:14.04.2020
#Sebastian Bittner, Stephan Buchner
SZABTEST = False
import pygame, random, sys, os, math, pytmx, numpy as np
from terrainstats import *

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
        # statsslug

        SCHNECKEV = 2.5
        SCHNECKEESSEN =  0.05 #Essen pro Tier und Sekunde
        SCHNECKEHUNGERRES = 2
        HUNGERSCHNECKE = 0.009
        FITNESS_SCHNECKE = 1.018 # ~ Chance eines Tiers sich zu teilen pro Sekunde
        SCHNECKEDECINTERVAL = 2
        TEILPOPGROESSESCHNECKE = 50
        SCHNECKEGROESSE = 1
        ANGRIFFSLISTESCHNECKE = []
        SCHNECKETEMP, SCHNECKETEMPRANGE = 25,20
        SCHNECKEEVASION = -4
        SCHNECKEPREC = -5
        # statsmouse

        MAUSV = 8
        MAUSESSEN = 0.5 #Essen pro Tier und Sekunde
        MAUSHUNGERRES = 1.2
        HUNGERMAUS = 0.09
        FITNESS_MAUS = 1.012 # ~ Chance einer Schnecke sich zu teilen pro Sekunde
        MAUSDECINTERVAL = 3
        TEILPOPGROESSEMAUS = 30
        MAUSGROESSE = 3
        ANGRIFFSLISTEMAUS = ["Schnecke", "Käfer"]
        MAUSTEMP, MAUSTEMPRANGE = 20,20
        MAUSINTELLIGENZ = 2
        MAUSSTAERKE = 1
        MAUSEVASION = 0
        MAUSPREC = 0
        #statskrabbe

        KRABBEV = 2
        KRABBEESSEN = 0.15 #Essen pro Tier und Sekunde
        KRABBEHUNGERRES = 3
        HUNGERKRABBE = 0.0045
        FITNESS_KRABBE = 1.016 # ~ Chance einer Schnecke sich zu teilen pro Sekunde
        KRABBEDECINTERVAL = 10
        TEILPOPGROESSEKRABBE = 40
        KRABBEGROESSE = 1.5
        ANGRIFFSLISTEKRABBE = ["Schnecke"]
        KRABBETEMP, KRABBETEMPRANGE = 10, 20
        KRABBEINTELLIGENZ = 1
        KRABBEEVASION = -2
        KRABBEPREC = -2
        #Falkestats

        FALKEVGEHEND = 5
        FALKEVFLIEGEND = 30
        FALKEESSEN = 1 #Essen pro Tier und Sekunde
        FALKEHUNGERRES = 0.7
        HUNGERFALKEGEHEND = 0.05
        HUNGERFALKEFLIEGEND = 0.09
        FITNESS_FALKE = 1.01 # ~ Chance einer Schnecke sich zu teilen pro Sekunde
        FALKEDECINTERVAL = 3
        TEILPOPGROESSEFALKE = 15
        FALKEGROESSE = 4
        ANGRIFFSLISTEFALKE = ["Maus", "Käfer", "Singvogel"]
        FALKETEMP, FALKETEMPRANGE = 15,20
        FALKEINTELLIGENZ = 2
        FALKESTAERKE = 5
        FALKEEVASION = 2
        FALKEPREC = 3
        #SINGVOGELstats

        SINGVOGELVGEHEND = 5
        SINGVOGELVFLIEGEND = 25
        SINGVOGELESSEN = 1.5 #Essen pro Tier und Sekunde
        SINGVOGELHUNGERRES = 1.2
        HUNGERSINGVOGELGEHEND = 0.04
        HUNGERSINGVOGELFLIEGEND = 0.06
        FITNESS_SINGVOGEL = 1.013 # ~ Chance einer Schnecke sich zu teilen pro Sekunde
        SINGVOGELDECINTERVAL = 4
        TEILPOPGROESSESINGVOGEL = 20
        SINGVOGELGROESSE = 5
        ANGRIFFSLISTESINGVOGEL = ["Schnecke", "Käfer"]
        SINGVOGELTEMP, SINGVOGELTEMPRANGE = 25,15
        SINGVOGELINTELLIGENZ = 2
        SINGVOGELSTAERKE = 2
        SINGVOGELEVASION = 1
        SINGVOGELPREC = 2
        #statskaefer

        KAEFERV = 4
        KAEFERESSEN = 0.05 #Essen pro Schnecke und Sekunde
        KAEFERHUNGERRES = 1.0
        HUNGERKAEFER = 0.018
        FITNESS_KAEFER = 1.023 # ~ Chance einer Schnecke sich zu teilen pro Sekunde
        KAEFERDECINTERVAL = 3
        TEILPOPGROESSEKAEFER = 60
        KAEFERGROESSE = 0.6
        ANGRIFFSLISTEKAEFER = []
        KAEFERTEMP, KAEFERTEMPRANGE = 20,30
        KAEFEREVASION = -3
        KAEFERPREC = -2

        #statsdoktorfisch

        DOKTORFISCHV = 5
        DOKTORFISCHESSEN = 0.1 #Essen pro Schnecke und Sekunde
        DOKTORFISCHHUNGERRES = 1.5
        HUNGERDOKTORFISCH = 0.006
        FITNESS_DOKTORFISCH = 1.018 # ~ Chance einer Schnecke sich zu teilen pro Sekunde
        DOKTORFISCHDECINTERVAL = 5
        TEILPOPGROESSEDOKTORFISCH = 60
        DOKTORFISCHGROESSE = 1
        ANGRIFFSLISTEDOKTORFISCH = []
        DOKTORFISCHTEMP, DOKTORFISCHTEMPRANGE = 7,20
        DOKTORFISCHINTELLIGENZ = 1
        DOKTORFISCHEVASION = -1
        DOKTORFISCHPREC = -3
        # statsFUCHS
        FUCHSV = 15
        FUCHSVHUNT = 40
        FUCHSESSEN = 2 #Essen pro Tier und Sekunde
        FUCHSHUNGERRES = 1.4
        HUNGERFUCHS = 0.1
        FITNESS_FUCHS = 1.007 # ~ Chance eines Tiers sich zu teilen pro Sekunde
        FUCHSDECINTERVAL = 3
        TEILPOPGROESSEFUCHS = 15
        FUCHSGROESSE = 10
        ANGRIFFSLISTEFUCHS = ["Maus", "Kaninchen"]
        FUCHSTEMP, FUCHSTEMPRANGE = 15,23
        FUCHSINTELLIGENZ = 2
        FUCHSEVASION = 1
        FUCHSPREC = 2

        # statskaninchen
        KANINCHENV = 15
        KANINCHENESSEN = 0.3 #Essen pro Schnecke und Sekunde
        KANINCHENHUNGERRES = 1.0
        HUNGERKANINCHEN = 0.08
        FITNESS_KANINCHEN = 1.011 # Chance sich zu teilen pro Sekunde
        KANINCHENDECINTERVAL = 3
        TEILPOPGROESSEKANINCHEN = 25
        KANINCHENGROESSE = 5
        ANGRIFFSLISTEKANINCHEN = []
        KANINCHENTEMP, KANINCHENTEMPRANGE = 20,20
        KANINCHENINTELLIGENZ = 2
        KANINCHENEVASION = 1
        KANINCHENPREC = -2

        # statsziege
        ZIEGEV = 20
        ZIEGEESSEN = 0.3 #Essen pro Tier und Sekunde
        ZIEGEHUNGERRES = 2
        HUNGERZIEGE = 0.15
        FITNESS_ZIEGE = 1.006 # ~ Chance eines Tiers sich zu teilen pro Sekunde
        ZIEGEDECINTERVAL = 3
        TEILPOPGROESSEZIEGE = 10
        ZIEGEGROESSE = 5
        ANGRIFFSLISTEZIEGE = []
        ZIEGETEMP, ZIEGETEMPRANGE = 0,10
        ZIEGEINTELLIGENZ = 3
        ZIEGEEVASION = 1
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
# allgemeine Funktionen
def abst(v1,v2):
        """Rechnet v2 minus v1"""
        return (v2[0] - v1[0], v2[1] - v1[1])

def norm(v):
        return math.sqrt(v[0]**2 + v[1]**2)

def normabst(v1, v2):
      return norm(abst(v1,v2))

def mult(v, a, toInteger = False):
    if toInteger:
        return (int(v[0]*a), int(v[1]*a))
    return (v[0]*a, v[1]*a)
def addieren(v1,v2):
    return (v1[0]+v2[0],v1[1]+v2[1])

def pInRect(p, rectInfo):
    return pygame.rect.Rect(rectInfo).collidepoint(p)
def getSpeeds(speed, angle):
    angle = angle * math.pi / 180
    return math.cos(angle) * speed, math.sin(angle) * speed

def calcAngle(pos):
    z = np.array(pos[0] + pos[1] * 1.j)
    return np.angle(z) *180 / math.pi

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

#unnoetig it seems
def createTileSetMatrix(info):
    map, tilenbr = info
    tilenbrx, tilenbry = tilenbr
    res = [[getTileTerrainAndSet(map, (x,y)) for y in range(tilenbry)] for x in range(tilenbrx)]
    return res, lulw

def getTile(pos):
    return mult(pos, 1/16, True)

#schneidet ein Bild zu, und skaliert es


#Landschaft


class Lebewesen:
  desc = "basicLebewesen"
  def __init__(self, game, startpos = (400,400), startangle = None, info = None):
    self.game = game
    self.posx, self.posy = startpos
    self.speed = self.standardSpeed = 20
    self.speedMultEssen = 1
    self.speedMultTerrain = 1
    self.speedMultMisc = 1
    self.angle = startangle
    if startangle == None:
        startangle = random.random() * 360
    self.changeAngle(startangle, True)
    if info == None:
        self.hunger = 0 #Durchschnittlicher Hunger der Lebewesen
        self.alter = 1
        self.mutationen = []
    else:
        self.hunger, self.alter, self.mutationen = info
    self.wachstumsf = 2
    self.vorherigesterrain = None
    self.terraincounter = 0
    self.affinitaet = []
    self.survivalin = []
    self.optimalTemp = 15
    self.tempRange = 10
    self.alive = True
    self.swim = 0
    self.imFlug = False
    self.testForTerrain()
    self.tile = getTile(startpos)
    self.game.tileMatrix[self.tile[0]][self.tile[1]]["Lebewesen"].append(self)
    self.groesse = 0
    self.W = 0
    self.standardW = 0
    self.pflanzenfresser = True
    self.fleischfresser = False
    self.standardStaerke = 0
    self.staerke = self.standardStaerke
    self.erlaubteTerrains = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    self.opferImAuge = None
    self.geboren = self.game.frames
    self.standardInt = 0
    self.intelligence = 0
    self.standardEvasion = 0
    self.standardPrecision = 0
    self.lastAttack = self.game.frames

  def moveBy(self, x, y, force = False):
      tileVorher = self.tile
      terrainVorher = self.terrain
      self.posx += x
      self.posy += y
      self.posx = max(0, min(self.posx, 16*self.game.tilenbrx-0.1))
      self.posy = max(0, min(self.posy, 16*self.game.tilenbry-0.1))
      if self.posx == 0 or self.posy == 0 or self.posx == 16*self.game.tilenbrx-0.1 or self.posy ==16*self.game.tilenbry-0.1:
          self.angle += 180
      self.testForTerrain()
      intbonustimes = self.mutationen.count("MUTINTBOOST")
      self.intelligence = (self.standardInt + intbonustimes * INTBOOSTBONUS) * INTBOOSTMULT ** intbonustimes
      if not force:
          if random.random() > np.power(2.0,-self.intelligence):
            if self.terrain not in self.erlaubteTerrains or (SWIMIN[self.terrain] > self.swim and not self.imFlug):
                self.angle += 180
                self.posx -= x
                self.posy -= y
                self.testForTerrain()
            elif terrainVorher in self.affinitaet and self.terrain not in self.affinitaet:
                self.angle += 180
                self.posx -= x
                self.posy -= y
                self.testForTerrain()
      self.tile = getTile((self.posx, self.posy))
      if tileVorher != self.tile:
          self.game.tileMatrix[self.tile[0]][self.tile[1]]["Lebewesen"].append(self)
          self.game.tileMatrix[tileVorher[0]][tileVorher[1]]["Lebewesen"].remove(self)

  def move(self):
      mutfaktor = 1 + GETFASTBONUS * self.mutationen.count("MUTGETFAST")
      self.setSpeed(self.standardSpeed * self.speedMultEssen * self.speedMultTerrain * self.speedMultMisc * mutfaktor)
      self.moveBy(self.vx/FPSGAME, self.vy/FPSGAME)

  def setSpeed(self, v):
      self.speed = v
      self.vx, self.vy = getSpeeds(self.speed, self.angle)

  def getPos(self):
      return self.posx, self.posy

  def changeAngle(self, angle, to = False):
      """if to is set to True, then the angle is set to angle,
      else it changes the angle by angle"""
      if to:
          self.angle = angle
      else:
          self.angle += angle
      self.vx, self.vy = getSpeeds(self.speed, self.angle)


  def everyFrame(self):
    if (self.game.frames - self.geboren)%POPANPASSENINTERVAL == 0:
        self.populationAnpassen()
    self.reactToTerrain()
    self.move()
    self.randomteilen()
    mutcounter = self.mutationen.count("MUTPOWERBOOST")
    if "MUTPOWERBOOST" in self.mutationen:
        self.staerke = (self.standardStaerke) * (mutcounter + 1) + mutcounter * 5

  def pflanzenfressen(self):
      if self.pflanzenfresser and self.alive:
          kapazitaet = self.hunger * self.popGroesse
          verfuegbar = self.game.getPflanzenEssen(getTile(self.getPos()))
          essenMenge = min(kapazitaet, verfuegbar,
                            self.eatSpeed*self.popGroesse/FPSGAME)
          self.game.setPflanzenEssen(getTile(self.getPos()),verfuegbar - essenMenge)
          self.hunger -= essenMenge/self.popGroesse

  def populationAnpassen(self):
      zeitVerg = POPANPASSENINTERVAL/FPSGAME
      if self.alive:
# Wahrscheinlichkeit, dass ein Mitglied sich vermehrt
          w = self.getFitness()
          baseP = (0.001 * min(0,(1 - abs(w - 1)))*zeitVerg)*self.popGroesse
          if w >= 1:
              pEinesMehr = baseP + ((w - 1) * zeitVerg) * self.popGroesse
              pEinesWeniger = baseP
          else:
              pEinesWeniger = baseP + (1-w) * zeitVerg * self.popGroesse
              pEinesMehr = baseP
          einsMehr = int(random.random() < pEinesMehr)
          aenderung = einsMehr - int(random.random() < pEinesWeniger)
          self.hunger += self.hungerproframe + einsMehr / self.popGroesse
          self.changePop(aenderung)

  def testForTerrain(self):
      self.terrain = self.game.getTerrain((self.posx, self.posy))

  def reactToTerrain(self):
      self.testForTerrain()
      if self.vorherigesterrain == self.terrain:
          self.terraincounter += 1
          if self.terraincounter > ANPASSUNGSEKUNDEN*FPSGAME:
              i = random.randint(1, ANPASSUNGSCHANCE)
              if i == 1:
                  self.affinitaet.append(self.terrain)
                  self.terraincounter = 0
              else:
                  self.terraincounter = 0
      if SWIMIN[self.terrain] > self.swim and not self.imFlug:
          self.alive = False
      if not (self.terrain in self.erlaubteTerrains):
          self.alive = False
      self.speedMultTerrain = self.speedMultInTerrain()
      if self.imFlug:
          self.speedMultTerrain = 1
      self.vorherigesterrain = self.terrain

  def speedMultInTerrain(self):
      return SPEEDIN[self.terrain]

  def tierfressen(self, arten):
      if self.fleischfresser and self.alive:
          kapazitaet = self.hunger * self.popGroesse
          essenMenge = min(kapazitaet, self.eatSpeed * self.popGroesse/FPSGAME)
          gegessen = 0
          for stueck in self.game.getFrischFleischInfo(self.tile):
              if stueck[1] in arten:
                  if stueck[3] > essenMenge-gegessen:
                      stueck[3]-= essenMenge - gegessen
                      gegessen = essenMenge
                  else:
                      gegessen += stueck[3]
                      self.game.tileMatrix[self.tile[0]][self.tile[1]]["FrischFleisch"].remove(stueck)
          self.hunger -= gegessen/self.popGroesse


  def angriff(self, anderesObj, menge):
      if self.alive and (self.game.frames - self.lastAttack) > FPSGAME:
          menge = min(self.popGroesse, menge)
          self.hunger += ANGRIFFHUNGER*menge/self.popGroesse
          self.game.kampfaustragen(self, anderesObj, menge)

  def findeOpfer(self, searchsize):
      opfer = None
      minabstand = 320 * searchsize + 1
      for xtile in range(self.tile[0] - searchsize, self.tile[0] + searchsize + 1):
          for ytile in range(self.tile[1] - searchsize, self.tile[1] + searchsize + 1):
              for moegl in self.game.getLivingThingsInTile((xtile,ytile)):
                  if normabst(self.getPos(),moegl.getPos()) < minabstand and moegl.desc in self.opfer:
                      opfer = moegl
                      minabst = normabst(self.getPos(), moegl.getPos())
      return opfer

  def getFitness(self):
      mutboost = (self.standardW - 1) * FITNESSBOOSTBONUS * self.mutationen.count("MUTFITNESSBOOST")
      tmp = self.game.getTemp(self.terrain, self.tile)
      temperaturAnpassung = np.exp(-((tmp - self.optimalTemp)/self.tempRange)**2/2)
      w1 = (self.standardW + mutboost - (self.hunger / self.hungerResistenz)**3*TODFAKTOR)
      ##print(temperaturAnpassung, w1)
      return w1 * np.power(temperaturAnpassung, TEMPANPASSKOEFF)

  def getEvasion(self):
      mutbonus = self.mutationen.count("MUTEVASIONBOOST")
      return self.standardEvasion + mutbonus

  def getPrecision(self):
      mutbonus = self.mutationen.count("MUTPRECISIONBOOST")
      return self.standardPrecision + mutbonus

  def fliegen(self):
      self.imFlug = True

  def nichtFliegen(self):
      self.imFlug = False


  def verteidigen(self, anderesObj, menge):
      pass

  def changePop(self, change):
      self.popGroesse += change
      if self.popGroesse <= 0:
          self.alive = False
  def getPosTile(self):
      return getTile((self.posx, self.posy))

class Schnecke(Lebewesen):
    desc = "Schnecke"
    def __init__(self, game, startpos, startangle = 0, info = None):
        if info == None:
            self.popGroesse = 15
            infoweiter = None
        else:
            h,a,m,self.popGroesse = info
            infoweiter = (h,a,m)
        Lebewesen.__init__(self, game, startpos, startangle, infoweiter)
        self.standardSpeed = self.speed = SCHNECKEV
        self.standardspeed = SCHNECKEV
        self.eatSpeed = SCHNECKEESSEN
        self.hungerResistenz = SCHNECKEHUNGERRES
        self.standardW = FITNESS_SCHNECKE
        self.hungerproframe = HUNGERSCHNECKE/FPSGAME
        self.lastAngleChange = self.game.frames
        self.groesse = SCHNECKEGROESSE
        self.optimalTemp, self.tempRange = SCHNECKETEMP, SCHNECKETEMPRANGE
        self.standardEvasion = SCHNECKEEVASION
        self.standardPrecision = SCHNECKEPREC

    def everyFrame(self):
        if DESERT in self.affinitaet:
            self.optimalTemp = 30
            self.hungerResistenz = 4
            self.fitness = 3
        if self.game.frames > self.lastAngleChange + SCHNECKEDECINTERVAL*FPSGAME:
            self.lastAngleChange = self.game.frames
            self.changeAngle(random.random() * 90 - 45)
        if self.game.getPflanzenEssen(getTile(self.getPos())) > 0.01:
            self.speedMultEssen = 0.5
            self.pflanzenfressen()
        else:
            self.speedMultEssen = 1
        Lebewesen.everyFrame(self)

    def randomteilen(self):
        if self.popGroesse >= TEILPOPGROESSESCHNECKE and 1==random.randint(1,10*FPSGAME):
            groesse = random.randint(1,self.popGroesse - 1)
            starta = random.randint(0,359)
            self.game.addCreature(Schnecke, (self.posx,self.posy), self.player,
                starta, [self.hunger, self.alter,self.mutationen[:], groesse])
            self.popGroesse -= groesse

class Kaefer(Lebewesen):
    desc = "Käfer"
    def __init__(self, game, startpos, startangle = 0, info = None):
        if info == None:
            self.popGroesse = 20
            infoweiter = None
        else:
            h,a,m,self.popGroesse = info
            infoweiter = (h,a,m)
        Lebewesen.__init__(self, game, startpos, startangle, infoweiter)
        self.standardSpeed = self.speed = KAEFERV
        self.standardspeed = KAEFERV
        self.eatSpeed = self.popGroesse * KAEFERESSEN
        self.hungerResistenz = KAEFERHUNGERRES
        self.standardW = FITNESS_KAEFER
        self.hungerproframe = HUNGERKAEFER/FPSGAME
        self.lastAngleChange = self.game.frames
        self.groesse = KAEFERGROESSE
        self.optimalTemp, self.tempRange = KAEFERTEMP, KAEFERTEMPRANGE
        self.standardEvasion = KAEFEREVASION
        self.standardPrecision = KAEFERPREC


    def everyFrame(self):
        if self.game.frames > self.lastAngleChange + KAEFERDECINTERVAL*FPSGAME:
            self.lastAngleChange = self.game.frames
            self.changeAngle(random.random() * 90 - 45)
        if self.game.getPflanzenEssen(getTile(self.getPos())) > 0.01:
            self.speedMultEssen = 0.5
            self.pflanzenfressen()
        else:
            self.speedMultEssen = 1
        Lebewesen.everyFrame(self)

    def randomteilen(self):
        if self.popGroesse >= TEILPOPGROESSEKAEFER and 1==random.randint(1,10*FPSGAME):
            groesse = random.randint(1,self.popGroesse - 1)
            starta = random.randint(0,359)
            self.game.addCreature(Kaefer, (self.posx,self.posy),  self.player,
                    starta, [self.hunger, self.alter, self.mutationen[:], groesse])
            self.popGroesse -= groesse

class Maus(Lebewesen):
    desc = "Maus"
    def __init__(self, game, startpos, startangle = 0, info = None):
        if info == None:
            self.popGroesse = 5
            infoweiter = None
        else:
            h,a,m,self.popGroesse = info
            infoweiter = (h,a,m)
        Lebewesen.__init__(self, game, startpos, startangle, infoweiter)
        self.standardSpeed = self.speed = MAUSV
        self.eatSpeed = MAUSESSEN
        self.hungerResistenz = MAUSHUNGERRES
        self.standardW = FITNESS_MAUS
        self.hungerproframe = HUNGERMAUS/FPSGAME
        self.lastAngleChange = self.game.frames
        self.groesse = MAUSGROESSE
        self.fleischfresser = True
        self.standardStaerke = MAUSSTAERKE
        self.opfer = ANGRIFFSLISTEMAUS  #Die Objekte die es angreifen kann
        self.optimalTemp, self.tempRange = MAUSTEMP, MAUSTEMPRANGE
        self.standardInt = MAUSINTELLIGENZ
        self.standardEvasion = MAUSEVASION
        self.standardPrecision = MAUSPREC

    def everyFrame(self):
        if self.game.frames > self.lastAngleChange + MAUSDECINTERVAL*FPSGAME:
            self.lastAngleChange = self.game.frames
            self.changeAngle(random.random() * 90 - 45)
        amEssen = False
        moegl = self.game.getFrischFleischMenge(getTile(self.getPos()), self.opfer)
        if moegl > 0.1 and self.hunger > 0.1:
            self.speedMultEssen = 0
            self.tierfressen(self.opfer)
        elif self.game.getPflanzenEssen(getTile(self.getPos())) > 0.1:
            self.speedMultEssen = 0.5
            self.pflanzenfressen()
        else:
            self.speedMultEssen = 1
        lwInTile = self.game.getLivingThingsInTile(self.tile)
        for gegner in lwInTile:
            if gegner.desc in self.opfer and self.hunger > 0.3:
                self.angriff(gegner, min(self.popGroesse, gegner.popGroesse))
                break
        Lebewesen.everyFrame(self)
    def randomteilen(self):
        if self.popGroesse >= TEILPOPGROESSEMAUS and 1==random.randint(1,10*FPSGAME):
            groesse = random.randint(1,self.popGroesse - 1)
            starta = random.randint(0,359)
            self.game.addCreature(Maus, (self.posx,self.posy), self.player,
                    starta, [self.hunger, self.alter, self.mutationen[:], groesse])
            self.popGroesse -= groesse

class Krabbe(Lebewesen):
    desc = "Krabbe"
    def __init__(self, game, startpos, startangle = 0, info = None):
        if info == None:
            self.popGroesse = 10
            infoweiter = None
        else:
            h,a,m,self.popGroesse = info
            infoweiter = (h,a,m)
        Lebewesen.__init__(self, game, startpos, startangle, infoweiter)
        self.moveBy(0,0)
        self.standardSpeed = self.speed = KRABBEV
        self.eatSpeed = self.popGroesse * KRABBEESSEN
        self.hungerResistenz = KRABBEHUNGERRES
        self.standardW = FITNESS_KRABBE
        self.hungerproframe = HUNGERKRABBE/FPSGAME
        self.fleischfresser = True
        self.lastAngleChange = self.game.frames
        self.groesse = KRABBEGROESSE
        self.standardStaerke = 0.5
        self.opfer = ANGRIFFSLISTEKRABBE  #Die Objekte die es angreifen kann
        self.erlaubteTerrains = [RIVER, RIVERBANK, COASTWATER, COASTGRASS, BEACH]
        self.swim = 2
        self.optimalTemp, self.tempRange = KRABBETEMP, KRABBETEMPRANGE
        self.standardInt = KRABBEINTELLIGENZ
        self.standardEvasion = KRABBEEVASION
        self.standardPrecision = KRABBEPREC

    def everyFrame(self):
        if self.game.frames > self.lastAngleChange + KRABBEDECINTERVAL*FPSGAME:
            self.lastAngleChange = self.game.frames
            self.changeAngle(random.random() * 360-180)
        moegl = self.game.getFrischFleischMenge(getTile(self.getPos()), self.opfer)
        if moegl > 0.1 and self.hunger > 0.1:
            self.speedMultEssen = 0
            self.tierfressen(self.opfer)
        elif self.game.getPflanzenEssen(getTile(self.getPos())) > 0.01:
            self.speedMultEssen = 0.5
            self.pflanzenfressen()
        else:
            self.speedMultEssen = 1
        if (self.game.frames-self.geboren)%5 == 0 and self.hunger > 0.3:
            lwInTile = self.game.getLivingThingsInTile(self.tile)
            for gegner in lwInTile:
                if gegner.desc in self.opfer:
                    self.angriff(gegner, min(self.popGroesse, gegner.popGroesse))
                    break
        Lebewesen.everyFrame(self)

    def randomteilen(self):
        if self.popGroesse >= TEILPOPGROESSEKRABBE and 1==random.randint(1,10*FPSGAME):
            groesse = random.randint(1,self.popGroesse - 1)
            starta = random.randint(0,359)
            self.game.addCreature(Krabbe, (self.posx,self.posy),  self.player,
                    starta, [self.hunger, self.alter, self.mutationen[:], groesse])
            self.popGroesse -= groesse

class Falke(Lebewesen):
    desc = "Falke"
    def __init__(self, game, startpos, startangle = 0, info = None):
        if info == None:
            self.popGroesse = 5
            infoweiter = None
        else:
            h,a,m,self.popGroesse = info
            infoweiter = (h,a,m)
        Lebewesen.__init__(self, game, startpos, startangle, infoweiter)
        self.moveBy(0,0)
        self.standardSpeed = self.speed = FALKEVGEHEND
        self.essenProSekunde = FALKEESSEN
        self.hungerResistenz = FALKEHUNGERRES
        self.standardW = FITNESS_FALKE
        self.hungerproframe = HUNGERFALKEGEHEND/FPSGAME
        self.optimalTemp, self.tempRange = FALKETEMP, FALKETEMPRANGE
        self.lastAngleChange = self.game.frames
        self.groesse = FALKEGROESSE
        self.fleischfresser = True
        self.pflanzenfresser = False
        self.standardStaerke = FALKESTAERKE
        self.opfer = ANGRIFFSLISTEFALKE  #Die Objekte die es angreifen kann
        self.eatSpeed = FALKEESSEN
        self.standardInt = FALKEINTELLIGENZ
        self.standardEvasion = FALKEEVASION
        self.standardPrecision = FALKEPREC

    def everyFrame(self):
        moegl = self.game.getFrischFleischMenge(getTile(self.getPos()), self.opfer)
        if moegl > 0.1 and self.hunger > 0.001:
            self.nichtFliegen()
            self.speedMultEssen = 0
            self.tierfressen(self.opfer)
            self.opferImAuge = None
        else:
            self.speedMultEssen = 1
            if self.opferImAuge == None and ((self.game.frames-self.geboren)%
                        (FALKEDECINTERVAL/5 * FPSGAME) == 0 and self.hunger > 0.5):
                self.opferImAuge = self.findeOpfer(1)

            if self.opferImAuge != None:
                self.fliegen()
                self.changeAngle(calcAngle(abst(self.getPos(), self.opferImAuge.getPos())),True)
                if not self.opferImAuge.alive:
                    self.opferImAuge = None
            else:
                if self.game.frames > self.lastAngleChange + FALKEDECINTERVAL*FPSGAME:
                    self.lastAngleChange = self.game.frames
                    self.changeAngle(random.random() * 90 - 45)
                if self.hunger < FALKEHUNGERRES / 2:
                    self.nichtFliegen()
                else:
                    self.fliegen()
            lwInTile = self.game.getLivingThingsInTile(self.tile)
            for gegner in lwInTile:
                if gegner.desc in self.opfer and self.hunger > 0.3:
                    self.angriff(gegner, min(self.popGroesse, gegner.popGroesse))
                    break
        if self.imFlug:
            self.standardSpeed = FALKEVFLIEGEND
            self.hungerproframe = HUNGERFALKEFLIEGEND / FPSGAME
        else:
            self.standardSpeed = FALKEVGEHEND
            self.hungerproframe = HUNGERFALKEGEHEND / FPSGAME
        Lebewesen.everyFrame(self)

    def randomteilen(self):
        if self.popGroesse >= TEILPOPGROESSEFALKE and 1==random.randint(1,10*FPSGAME):
            groesse = random.randint(1,self.popGroesse - 1)
            starta = random.randint(0,359)
            self.game.addCreature(Falke, (self.posx,self.posy),  self.player,
                    starta, [self.hunger, self.alter, self.mutationen[:], groesse])
            self.popGroesse -= groesse

class Singvogel(Lebewesen):
    desc = "Singvogel"
    def __init__(self, game, startpos, startangle = 0, info = None):
        if info == None:
            self.popGroesse = 7
            infoweiter = None
        else:
            h,a,m,self.popGroesse = info
            infoweiter = (h,a,m)
        Lebewesen.__init__(self, game, startpos, startangle, infoweiter)
        self.moveBy(0,0)
        self.standardSpeed = self.speed = SINGVOGELVGEHEND
        self.essenProSekunde = SINGVOGELESSEN
        self.hungerResistenz = SINGVOGELHUNGERRES
        self.standardW = FITNESS_SINGVOGEL
        self.hungerproframe = HUNGERSINGVOGELGEHEND/FPSGAME
        self.optimalTemp, self.tempRange = SINGVOGELTEMP, SINGVOGELTEMPRANGE
        self.lastAngleChange = self.game.frames
        self.groesse = SINGVOGELGROESSE
        self.fleischfresser = True
        self.pflanzenfresser = True
        self.standardStaerke = SINGVOGELSTAERKE
        self.opfer = ANGRIFFSLISTESINGVOGEL  #Die Objekte die es angreifen kann
        self.eatSpeed = SINGVOGELESSEN
        self.standardInt = SINGVOGELINTELLIGENZ
        self.standardEvasion = SINGVOGELEVASION
        self.standardPrecision = SINGVOGELPREC

    def everyFrame(self):
        moegl = self.game.getFrischFleischMenge(getTile(self.getPos()), self.opfer)
        if moegl > 0.1 and self.hunger > 0.001:
            self.nichtFliegen()
            self.speedMultEssen = 0
            self.tierfressen(self.opfer)
            self.opferImAuge = None
        else:
            self.speedMultEssen = 1
            if self.opferImAuge != None:
                self.fliegen()
                self.changeAngle(calcAngle(abst(self.getPos(), self.opferImAuge.getPos())),True)
                if not self.opferImAuge.alive:
                    self.opferImAuge = None
            elif self.opferImAuge == None and ((self.game.frames-self.geboren)%
                        (SINGVOGELDECINTERVAL/5 * FPSGAME) == 0 and self.hunger > 0.5):
                self.opferImAuge = self.findeOpfer(1)
            elif self.game.getPflanzenEssen(getTile(self.getPos())) > 0.01 and self.hunger > 0.01:
                self.nichtFliegen()
                self.speedMultEssen = 0.5
                self.pflanzenfressen()
            else:
                if self.game.frames > self.lastAngleChange + SINGVOGELDECINTERVAL*FPSGAME:
                    self.lastAngleChange = self.game.frames
                    self.changeAngle(random.random() * 90 - 45)
                if self.hunger < SINGVOGELHUNGERRES / 2:
                    self.nichtFliegen()
                else:
                    self.fliegen()
            lwInTile = self.game.getLivingThingsInTile(self.tile)
            for gegner in lwInTile:
                if gegner.desc in self.opfer and self.hunger > 0.5:
                    self.angriff(gegner, min(self.popGroesse, gegner.popGroesse))
                    break
        if self.imFlug:
            self.standardSpeed = SINGVOGELVFLIEGEND
            self.hungerproframe = HUNGERSINGVOGELFLIEGEND / FPSGAME
        else:
            self.standardSpeed = SINGVOGELVGEHEND
            self.hungerproframe = HUNGERSINGVOGELGEHEND / FPSGAME
        Lebewesen.everyFrame(self)

    def randomteilen(self):
        if self.popGroesse >= TEILPOPGROESSESINGVOGEL and 1==random.randint(1,10*FPSGAME):
            groesse = random.randint(1,self.popGroesse - 1)
            starta = random.randint(0,359)
            self.game.addCreature(Singvogel, (self.posx,self.posy),  self.player,
                    starta, [self.hunger, self.alter, self.mutationen[:], groesse])
            self.popGroesse -= groesse

class Doktorfisch(Lebewesen):
    desc = "Doktorfisch"
    def __init__(self, game, startpos, startangle = 0, info = None):
        if info == None:
            self.popGroesse = 10
            infoweiter = None
        else:
            h,a,m,self.popGroesse = info
            infoweiter = (h,a,m)
        Lebewesen.__init__(self, game, startpos, startangle, infoweiter)
        self.standardSpeed = self.speed = DOKTORFISCHV
        self.moveBy(0,0)
        self.standardspeed = DOKTORFISCHV
        self.eatSpeed = DOKTORFISCHESSEN
        self.hungerResistenz = DOKTORFISCHHUNGERRES
        self.standardW = FITNESS_DOKTORFISCH
        self.hungerproframe = HUNGERDOKTORFISCH/FPSGAME
        self.lastAngleChange = self.game.frames
        self.groesse = DOKTORFISCHGROESSE
        self.optimalTemp, self.tempRange = DOKTORFISCHTEMP, DOKTORFISCHTEMPRANGE
        self.swim = 3
        self.erlaubteTerrains = [OCEAN, COASTWATER]
        self.standardInt = DOKTORFISCHINTELLIGENZ
        self.standardEvasion = DOKTORFISCHEVASION
        self.standardPrecision = DOKTORFISCHPREC

    def everyFrame(self):
        if self.game.frames > self.lastAngleChange + DOKTORFISCHDECINTERVAL*FPSGAME:
            self.lastAngleChange = self.game.frames
            self.changeAngle(random.random() * 90 - 45)
        if self.game.getPflanzenEssen(getTile(self.getPos())) > 0.01:
            self.speedMultEssen = 0.5
            self.pflanzenfressen()
        else:
            self.speedMultEssen = 1
        Lebewesen.everyFrame(self)

    def randomteilen(self):
        if self.popGroesse >= TEILPOPGROESSEDOKTORFISCH and 1==random.randint(1,10*FPSGAME):
            groesse = random.randint(1,self.popGroesse - 1)
            starta = random.randint(0,359)
            self.game.addCreature(Doktorfisch, (self.posx,self.posy),  self.player,
                        starta, [self.hunger, self.alter,self.mutationen[:], groesse])
            self.popGroesse -= groesse

class Aal(Lebewesen):
    desc = "Falke"
    def __init__(self, game, startpos, startangle = 0, info = None):
        if info == None:
            self.popGroesse = 5
            infoweiter = None
        else:
            h,a,m,self.popGroesse = info
            infoweiter = (h,a,m)
        Lebewesen.__init__(self, game, startpos, startangle, infoweiter)
        self.moveBy(0,0)
        self.standardSpeed = self.speed = FALKEVGEHEND
        self.essenProSekunde = FALKEESSEN
        self.hungerResistenz = FALKEHUNGERRES
        self.standardW = FITNESS_FALKE
        self.hungerproframe = HUNGERFALKEGEHEND/FPSGAME
        self.optimalTemp, self.tempRange = FALKETEMP, FALKETEMPRANGE
        self.lastAngleChange = self.game.frames
        self.groesse = FALKEGROESSE
        self.fleischfresser = True
        self.pflanzenfresser = False
        self.standardStaerke = 5
        self.opfer = ANGRIFFSLISTEFALKE  #Die Objekte die es angreifen kann
        self.eatSpeed = FALKEESSEN
        self.standardInt = 1
        self.standardEvasion = FALKEEVASION
        self.standardPrecision = FALKEPREC


    def everyFrame(self):
        moegl = self.game.getFrischFleischMenge(getTile(self.getPos()), self.opfer)
        if moegl > 0.1 and self.hunger > 0.001:
            self.nichtFliegen()
            self.speedMultEssen = 0
            self.tierfressen(self.opfer)
            self.opferImAuge = None
        else:
            self.speedMultEssen = 1
            if self.opferImAuge == None and (self.game.frames-self.geboren)%(FALKEDECINTERVAL/5 * FPSGAME) == 0 and self.hunger > 0.5:
                self.opferImAuge = self.findeOpfer(2)

            if self.opferImAuge != None:
                self.fliegen()
                self.changeAngle(calcAngle(abst(self.getPos(), self.opferImAuge.getPos())),True)
                if not self.opferImAuge.alive:
                    self.opferImAuge = None
            else:
                if self.game.frames > self.lastAngleChange + FALKEDECINTERVAL*FPSGAME:
                    self.lastAngleChange = self.game.frames
                    self.changeAngle(random.random() * 90 - 45)
                if self.hunger < FALKEHUNGERRES / 2:
                    self.nichtFliegen()
                else:
                    self.fliegen()
        lwInTile = self.game.getLivingThingsInTile(self.tile)
        for gegner in lwInTile:
            if gegner.desc in self.opfer and self.hunger > 0.5:
                self.angriff(gegner, min(self.popGroesse, gegner.popGroesse))
                break
        if self.imFlug:
            self.standardSpeed = FALKEVFLIEGEND
            self.hungerproframe = HUNGERFALKEFLIEGEND / FPSGAME
        else:
            self.standardSpeed = FALKEVGEHEND
            self.hungerproframe = HUNGERFALKEGEHEND / FPSGAME
        Lebewesen.everyFrame(self)

    def randomteilen(self):
        if self.popGroesse >= TEILPOPGROESSEFALKE and 1==random.randint(1,10*FPSGAME):
            groesse = random.randint(1,self.popGroesse - 1)
            starta = random.randint(0,359)
            self.game.addCreature(Falke, (self.posx,self.posy),  self.player,
                    starta, [self.hunger, self.alter, self.mutationen[:], groesse])
            self.popGroesse -= groesse

class Fuchs(Lebewesen):
    desc = "Fuchs"
    def __init__(self, game, startpos, startangle = 0, info = None):
        if info == None:
            self.popGroesse = 3
            infoweiter = None
        else:
            h,a,m,self.popGroesse = info
            infoweiter = (h,a,m)
        Lebewesen.__init__(self, game, startpos, startangle, infoweiter)
        self.standardSpeed = self.speed = FUCHSV
        self.eatSpeed = FUCHSESSEN
        self.hungerResistenz = FUCHSHUNGERRES
        self.standardW = FITNESS_FUCHS
        self.hungerproframe = HUNGERFUCHS/FPSGAME
        self.lastAngleChange = self.game.frames
        self.groesse = FUCHSGROESSE
        self.fleischfresser = True
        self.pflanzenfresser = False
        self.standardStaerke = 5
        self.opfer = ANGRIFFSLISTEFUCHS  #Die Objekte die es angreifen kann
        self.optimalTemp, self.tempRange = FUCHSTEMP, FUCHSTEMPRANGE
        self.standardInt = FUCHSINTELLIGENZ
        self.standardEvasion = FUCHSEVASION
        self.standardPrecision = FUCHSPREC

    def everyFrame(self):
        moegl = self.game.getFrischFleischMenge(getTile(self.getPos()), self.opfer)
        if moegl > 0.1 and self.hunger > 0:
            self.speedMultEssen = 0
            self.tierfressen(self.opfer)
            self.opferImAuge = None
        else:
            self.speedMultEssen = 1
            if self.opferImAuge == None and ((self.game.frames-self.geboren)%
                        (FUCHSDECINTERVAL/5 * FPSGAME) == 0 and self.hunger > 0.5):
                self.opferImAuge = self.findeOpfer(1)

            if self.opferImAuge != None:
                self.changeAngle(calcAngle(abst(self.getPos(), self.opferImAuge.getPos())),True)
                if not self.opferImAuge.alive:
                    self.opferImAuge = None
                self.standardSpeed = FUCHSVHUNT
            else:
                if self.game.frames > self.lastAngleChange + MAUSDECINTERVAL*FPSGAME:
                    self.lastAngleChange = self.game.frames
                    self.changeAngle(random.random() * 90 - 45)
                self.standardSpeed = FUCHSV
            if self.hunger > 0.3:
                lwInTile = self.game.getLivingThingsInTile(self.tile)
                for gegner in lwInTile:
                    if gegner.desc in self.opfer:
                        self.angriff(gegner, min(self.popGroesse, gegner.popGroesse))
                        break
        Lebewesen.everyFrame(self)

    def randomteilen(self):
        if self.popGroesse >= TEILPOPGROESSEFUCHS and 1==random.randint(1,10*FPSGAME):
            groesse = random.randint(1,self.popGroesse - 1)
            starta = random.randint(0,359)
            self.game.addCreature(Fuchs, (self.posx,self.posy), self.player,
                    starta, [self.hunger, self.alter, self.mutationen[:], groesse])
            self.popGroesse -= groesse


class Kaninchen(Lebewesen):
    desc = "Kaninchen"
    def __init__(self, game, startpos, startangle = 0, info = None):
        if info == None:
            self.popGroesse = 5
            infoweiter = None
        else:
            h,a,m,self.popGroesse = info
            infoweiter = (h,a,m)
        Lebewesen.__init__(self, game, startpos, startangle, infoweiter)
        self.standardSpeed = self.speed = KANINCHENV
        self.standardspeed = KANINCHENV
        self.eatSpeed = KANINCHENESSEN
        self.hungerResistenz = KANINCHENHUNGERRES
        self.standardW = FITNESS_KANINCHEN
        self.hungerproframe = HUNGERKANINCHEN/FPSGAME
        self.lastAngleChange = self.game.frames
        self.groesse = KANINCHENGROESSE
        self.optimalTemp, self.tempRange = KANINCHENTEMP, KANINCHENTEMPRANGE
        self.standardInt = KANINCHENINTELLIGENZ
        self.standardEvasion = KANINCHENEVASION
        self.standardPrecision = KANINCHENPREC


    def everyFrame(self):
        if self.game.frames > self.lastAngleChange + KANINCHENDECINTERVAL*FPSGAME:
            self.lastAngleChange = self.game.frames
            self.changeAngle(random.random() * 90 - 45)
        if self.game.getPflanzenEssen(getTile(self.getPos())) > 0.01:
            self.speedMultEssen = 0
            self.pflanzenfressen()
        else:
            self.speedMultEssen = 1
        Lebewesen.everyFrame(self)

    def randomteilen(self):
        if self.popGroesse >= TEILPOPGROESSEKANINCHEN and 1==random.randint(1,10*FPSGAME):
            groesse = random.randint(1,self.popGroesse - 1)
            starta = random.randint(0,359)
            self.game.addCreature(Kaninchen, (self.posx,self.posy),  self.player,
                    starta, [self.hunger, self.alter, self.mutationen[:], groesse])
            self.popGroesse -= groesse

class Ziege(Lebewesen):
    desc = "Ziege"
    def __init__(self, game, startpos, startangle = 0, info = None):
        if info == None:
            self.popGroesse = 4
            infoweiter = None
        else:
            h,a,m,self.popGroesse = info
            infoweiter = (h,a,m)
        Lebewesen.__init__(self, game, startpos, startangle, infoweiter)
        self.standardSpeed = self.speed = ZIEGEV
        self.standardspeed = ZIEGEV
        self.eatSpeed = ZIEGEESSEN
        self.hungerResistenz = ZIEGEHUNGERRES
        self.standardW = FITNESS_ZIEGE
        self.hungerproframe = HUNGERZIEGE/FPSGAME
        self.lastAngleChange = self.game.frames
        self.groesse = ZIEGEGROESSE
        self.optimalTemp, self.tempRange = ZIEGETEMP, ZIEGETEMPRANGE
        self.standardInt = ZIEGEINTELLIGENZ
        self.affinitaet = [SNOWYMOUNTAIN, LOWMOUNTAINS, HIGHMOUNTAIN]
        self.standardEvasion = ZIEGEEVASION

    def everyFrame(self):
        if self.game.frames > self.lastAngleChange + ZIEGEDECINTERVAL*FPSGAME:
            self.lastAngleChange = self.game.frames
            self.changeAngle(random.random() * 90 - 45)
        if self.game.getPflanzenEssen(getTile(self.getPos())) > 0.01:
            self.speedMultEssen = 0.5
            self.pflanzenfressen()
        else:
            self.speedMultEssen = 1
        Lebewesen.everyFrame(self)

    def randomteilen(self):
        if self.popGroesse >= TEILPOPGROESSEZIEGE and 1==random.randint(1,10*FPSGAME):
            groesse = random.randint(1,self.popGroesse - 1)
            starta = random.randint(0,359)
            self.game.addCreature(Ziege, (self.posx,self.posy),  self.player,
                    starta, [self.hunger, self.alter, self.mutationen[:], groesse])
            self.popGroesse -= groesse

    def speedMultInTerrain(self):
        if self.terrain in (HIGHMOUNTAIN, SNOWYMOUNTAIN, LOWMOUNTAINS):
            return 1
        return Lebewesen.speedMultInTerrain(self)

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
