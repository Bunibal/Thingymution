import random
from helpfunctions import *
from animalstats import *
from gameconstants import *
from terrainstats import *
from mutations import *

class Lebewesen:
    desc = "basicLebewesen"
    basestats = None

    def __init__(self, game, startpos=(400, 400), startangle=None, info=None):
        self.game = game
        self.posx, self.posy = startpos
        self.speed = self.standardSpeed = 20
        self.speedMultEssen = 1
        self.speedMultTerrain = 1
        self.angle = startangle
        if startangle == None:
            startangle = random.random() * 360
        self.changeAngle(startangle, True)
        if info == None:
            self.hunger = 0  # Durchschnittlicher Hunger der Lebewesen
            self.alter = 1
            self.mutationen = []
            self.mutierteStats = {}
            self.popGroesse = self.basestats["Startpop"]
        else:
            self.hunger, self.alter, self.mutationen, self.mutierteStats, self.popGroesse = info
        ## self.wachstumsf = 2
        self.direction = getSpeeds(1, startangle)
        self.vorherigesterrain = None
        self.terraincounter = 0
        self.affinitaet = []
        self.survivalin = []
        self.alive = True
        # self.swim = 0
        self.imFlug = False
        self.testForTerrain()
        self.tile = getTile(startpos)
        self.game.tileMatrix[self.tile[0]][self.tile[1]]["Lebewesen"].append(self)
        self.pflanzenfresser = True
        self.fleischfresser = False
        # self.standardStaerke = 0
        # self.staerke = self.standardStaerke
        # self.erlaubteTerrains = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        self.opferImAuge = None
        self.geboren = self.game.frames
        self.lastAttack = self.game.frames
        self.lastAngleChange = self.game.frames
        # Erstelle Dict von mutierten stats
        self.mutierteStats = {}
        self.stats = {}
        self.updateStats()
        self.skilltreepos = (-1, 0)

    def moveBy(self, x, y, force=False):
        tileVorher = self.tile
        terrainVorher = self.terrain
        self.posx += x
        self.posy += y
        self.posx = max(0, min(self.posx, 16 * self.game.tilenbrx - 0.1))  # testen ob langsamer
        self.posy = max(0, min(self.posy, 16 * self.game.tilenbry - 0.1))
        if self.posx == 0 or self.posy == 0 or self.posx == 16 * self.game.tilenbrx - 0.1 or self.posy == 16 * self.game.tilenbry - 0.1:
            self.angle += 180
        self.testForTerrain()
        if not force:
            if random.random() > np.power(2.0, -self.getInt()):
                if not self.terrainValid(self.terrain) or (SWIMIN[self.terrain] > self.getSwim() and not self.imFlug):
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
        vx, vy = mult(self.direction, self.getRealSpeed())
        self.moveBy(vx / FPSGAME, vy / FPSGAME)


    def everyFrame(self):
        if (self.game.frames - self.geboren) % POPANPASSENINTERVAL == 0:
            self.populationAnpassen()
        self.reactToTerrain()
        self.move()
        self.randomteilen()

    def pflanzenfressen(self):
        if self.isHerbivore() and self.alive:
            kapazitaet = self.hunger * self.popGroesse
            verfuegbar = self.game.getPflanzenEssen(getTile(self.getPos()))
            essenMenge = min(kapazitaet, verfuegbar,
                             self.getEatSpeed() * self.popGroesse / FPSGAME)
            self.game.setPflanzenEssen(getTile(self.getPos()), verfuegbar - essenMenge)
            self.hunger -= essenMenge / self.popGroesse

    def populationAnpassen(self):
        zeitVerg = POPANPASSENINTERVAL / FPSGAME
        if self.alive:
            # Wahrscheinlichkeit, dass ein Mitglied sich vermehrt
            w = self.getRealFitness()
            baseP = (0.001 * min(0, (1 - abs(w - 1))) * zeitVerg) * self.popGroesse
            if w >= 1:
                pEinesMehr = baseP + ((w - 1) * zeitVerg) * self.popGroesse
                pEinesWeniger = baseP
            else:
                pEinesWeniger = baseP + (1 - w) * zeitVerg * self.popGroesse
                pEinesMehr = baseP
            einsMehr = int(random.random() < pEinesMehr)
            aenderung = einsMehr - int(random.random() < pEinesWeniger)
            self.hunger += (self.getHungerpersec() / FPSGAME) + einsMehr / self.popGroesse
            self.changePop(aenderung)

    def randomteilen(self):
        if self.popGroesse >= self.getSplitpop() and 1 == random.randint(1, 10 * FPSGAME):
            groesse = random.randint(1, self.popGroesse - 1)
            starta = random.randint(0, 359)
            self.game.addCreature(type(self), (self.posx, self.posy), self.player, starta,
                [self.hunger, self.alter, self.mutationen[:], self.mutierteStats.copy(), groesse])
            self.popGroesse -= groesse

    def addMutation(self, mutation):
        self.mutationen.append(mutation["Name"])
        for stat in mutation["Stats"]:
            if stat in self.mutierteStats:
                self.mutierteStats[stat] += mutation["Stats"][stat]
            else:
                self.mutierteStats[stat] = mutation["Stats"][stat]
            self.updateStats(stat)

    def updateStats(self, stat = "all"):
        if stat == "all":
            for s in STATS:
                self.updateStats(s)
        else:
            base = flat = 0
            factor = 1
            if stat + "BASE" in self.mutierteStats:
                base = self.mutierteStats[stat+"BASE"]
            if stat in self.mutierteStats: # das heisst multiplikation
                factor = 1 + self.mutierteStats[stat]
            if stat + "FLAT" in self.mutierteStats:
                flat = self.mutierteStats[stat + "FLAT"]
            self.stats[stat] = (self.basestats[stat] + base) * factor + flat

    def testForTerrain(self):
        self.terrain = self.game.getTerrain((self.posx, self.posy))

    def reactToTerrain(self):
        # self.testForTerrain() # Wahrscheinlich unnötig, verlangsamt
        if self.vorherigesterrain == self.terrain:
            self.terraincounter += 1
            if self.terraincounter > ANPASSUNGSEKUNDEN * FPSGAME and self.terrain not in self.affinitaet:
                i = random.randint(1, ANPASSUNGSCHANCE)
                if i == 1:
                    self.affinitaet.append(self.terrain)
                    self.terraincounter = 0
        else:
            self.terraincounter = 0
            if not self.terrainValid(self.terrain):
                self.alive = False
        if SWIMIN[self.terrain] > self.getSwim() and not self.imFlug:
            self.alive = False
        self.speedMultTerrain = self.getSpeedMultInTerrain()
        if self.imFlug:
            self.speedMultTerrain = 1
        self.vorherigesterrain = self.terrain


    def tierfressen(self, arten):
        if self.isCarnivore() and self.alive:
            kapazitaet = self.hunger * self.popGroesse
            essenMenge = min(kapazitaet, self.getEatSpeed() * self.popGroesse / FPSGAME)
            gegessen = 0
            for stueck in self.game.getFrischFleischInfo(self.tile):
                if stueck[1] in arten:
                    if stueck[3] > essenMenge - gegessen:
                        stueck[3] -= essenMenge - gegessen
                        gegessen = essenMenge
                    else:
                        gegessen += stueck[3]
                        self.game.tileMatrix[self.tile[0]][self.tile[1]]["FrischFleisch"].remove(stueck)
            self.hunger -= gegessen / self.popGroesse

    def angriff(self, anderesObj, menge):
        if self.alive and (self.game.frames - self.lastAttack) > FPSGAME:
            menge = min(self.popGroesse, menge)
            self.hunger += ANGRIFFHUNGER * menge / self.popGroesse
            self.game.kampfaustragen(self, anderesObj, menge)

    def findeOpfer(self, searchsize):
        opfer = None
        minabstand = 320 * searchsize + 1
        for xtile in range(self.tile[0] - searchsize, self.tile[0] + searchsize + 1):
            for ytile in range(self.tile[1] - searchsize, self.tile[1] + searchsize + 1):
                for moegl in self.game.getLivingThingsInTile((xtile, ytile)):
                    if normabst(self.getPos(), moegl.getPos()) < minabstand and moegl.desc in self.opfer:
                        opfer = moegl
                        minabst = normabst(self.getPos(), moegl.getPos())
        return opfer


    def getMaxSpeed(self):
        return self.stats["Speed"]
    
    def getRealSpeed(self):
        return self.getMaxSpeed() * self.speedMultTerrain * self.speedMultEssen
        
    def changeAngle(self, angle, to=False):
        """if to is set to True, then the angle is set to angle,
        else it changes the angle by angle"""
        if to:
            self.angle = angle
        else:
            self.angle += angle
        self.direction = getSpeeds(1, self.angle)

    def getPos(self):
        return self.posx, self.posy

    def getRealFitness(self):
        tmp = self.game.getTemp(self.terrain, self.tile)
        temperaturAnpassung = np.exp(-((tmp - self.stats["OptimalTemp"]) / self.stats["Temprange"]) ** 2 / 2 * TEMPANPASSKOEFF)
        w1 = (self.stats["Fitness"] - (self.hunger / self.getHungerResistence()) ** 3 * TODFAKTOR)
        return w1 * temperaturAnpassung

    def getInt(self):
        return self.stats["Int"]

    def getPower(self):
        return self.stats["Power"]

    def getEatSpeed(self):
        return self.stats["Eatspeed"]

    def getSplitpop(self):
        return self.basestats["Splitpop"]

    def getEvasion(self):
        return self.stats["Evasion"]

    def getPrecision(self):
        return self.stats["Precision"]

    def getHungerResistence(self):
        return self.stats["Hungerres"]

    def getHungerpersec(self):
        return self.stats["Hungerpersec"]

    def getSize(self):
        return self.stats["Size"]

    def getSwim(self):
        return self.basestats["Swim"]

    def isCarnivore(self):
        return self.basestats["CarniV"]

    def isHerbivore(self):
        return self.basestats["HerbiV"]

    def getSpeedMultInTerrain(self):
        return SPEEDIN[self.terrain]

    def terrainValid(self, terrain):
        v = self.basestats["ValidTerrains"]
        return v == "all" or terrain in v

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
    basestats = SCHNECKEBASESTATS

    def __init__(self, game, startpos, startangle=0, info=None):
        Lebewesen.__init__(self, game, startpos, startangle, info)
        # self.standardSpeed = self.speed = SCHNECKEV
        # self.standardspeed = SCHNECKEV
        # self.eatSpeed = SCHNECKEESSEN
        # self.hungerResistenz = SCHNECKEHUNGERRES
        # self.standardW = FITNESS_SCHNECKE
        # self.hungerproframe = HUNGERSCHNECKE / FPSGAME
        # self.lastAngleChange = self.game.frames
        # self.groesse = SCHNECKEGROESSE
        # self.stats["OptimalTemp"], self.stats["Temprange"] = SCHNECKETEMP, SCHNECKETEMPRANGE
        # self.standardEvasion = SCHNECKEEVASION
        # self.standardPrecision = SCHNECKEPREC

    def everyFrame(self):
        if DESERT in self.affinitaet:
            self.stats["OptimalTemp"] = 30
            self.hungerResistenz = 4 #IDKWHATTODO
            self.fitness = 3
        if self.game.frames > self.lastAngleChange + self.stats["Decinterval"] * FPSGAME:
            self.lastAngleChange = self.game.frames
            self.changeAngle(random.random() * 90 - 45)
        if self.game.getPflanzenEssen(getTile(self.getPos())) > 0.01:
            self.speedMultEssen = 0.5
            self.pflanzenfressen()
        else:
            self.speedMultEssen = 1
        Lebewesen.everyFrame(self)

    # def randomteilen(self):
    #     if self.popGroesse >= TEILPOPGROESSESCHNECKE and 1 == random.randint(1, 10 * FPSGAME):
    #         groesse = random.randint(1, self.popGroesse - 1)
    #         starta = random.randint(0, 359)
    #         self.game.addCreature(Schnecke, (self.posx, self.posy), self.player,
    #                               starta, [self.hunger, self.alter, self.mutationen[:], groesse])
    #         self.popGroesse -= groesse


class Kaefer(Lebewesen):
    desc = "Käfer"
    basestats = KAEFERBASESTATS

    def __init__(self, game, startpos, startangle=0, info=None):
        Lebewesen.__init__(self, game, startpos, startangle, info)
        # self.standardSpeed = self.speed = KAEFERV
        # self.standardspeed = KAEFERV
        # self.eatSpeed = self.popGroesse * KAEFERESSEN
        # self.hungerResistenz = KAEFERHUNGERRES
        # self.standardW = FITNESS_KAEFER
        # self.hungerproframe = HUNGERKAEFER / FPSGAME
        # self.lastAngleChange = self.game.frames
        # self.groesse = KAEFERGROESSE
        # self.stats["OptimalTemp"], self.stats["Temprange"] = KAEFERTEMP, KAEFERTEMPRANGE
        # self.standardEvasion = KAEFEREVASION
        # self.standardPrecision = KAEFERPREC

    def everyFrame(self):
        if self.game.frames > self.lastAngleChange + self.stats["Decinterval"] * FPSGAME:
            self.lastAngleChange = self.game.frames
            self.changeAngle(random.random() * 90 - 45)
        if self.game.getPflanzenEssen(getTile(self.getPos())) > 0.01:
            self.speedMultEssen = 0.5
            self.pflanzenfressen()
        else:
            self.speedMultEssen = 1
        Lebewesen.everyFrame(self)

    # def randomteilen(self):
    #     if self.popGroesse >= TEILPOPGROESSEKAEFER and 1 == random.randint(1, 10 * FPSGAME):
    #         groesse = random.randint(1, self.popGroesse - 1)
    #         starta = random.randint(0, 359)
    #         self.game.addCreature(Kaefer, (self.posx, self.posy), self.player,
    #                               starta, [self.hunger, self.alter, self.mutationen[:], groesse])
    #         self.popGroesse -= groesse


class Maus(Lebewesen):
    desc = "Maus"
    basestats = MAUSBASESTATS

    def __init__(self, game, startpos, startangle=0, info=None):
        Lebewesen.__init__(self, game, startpos, startangle, info)
        # self.standardSpeed = self.speed = MAUSV
        # self.eatSpeed = MAUSESSEN
        # self.hungerResistenz = MAUSHUNGERRES
        # self.standardW = FITNESS_MAUS
        # self.hungerproframe = HUNGERMAUS / FPSGAME
        # self.lastAngleChange = self.game.frames
        # self.groesse = MAUSGROESSE
        # self.fleischfresser = True
        # self.standardStaerke = MAUSSTAERKE
        # self.opfer = ANGRIFFSLISTEMAUS  # Die Objekte die es angreifen kann
        # self.stats["OptimalTemp"], self.stats["Temprange"] = MAUSTEMP, MAUSTEMPRANGE
        # self.standardInt = MAUSINTELLIGENZ
        # self.standardEvasion = MAUSEVASION
        # self.standardPrecision = MAUSPREC

    def everyFrame(self):
        if self.game.frames > self.lastAngleChange + self.stats["Decinterval"] * FPSGAME:
            self.lastAngleChange = self.game.frames
            self.changeAngle(random.random() * 90 - 45)
        amFleischEssen = False
        moegl = self.game.getFrischFleischMenge(getTile(self.getPos()), self.basestats["Targets"])
        if moegl > 0.1 and self.hunger > 0.1:
            self.speedMultEssen = 0
            self.tierfressen(self.basestats["Targets"])
            amFleischEssen = True
        elif self.game.getPflanzenEssen(getTile(self.getPos())) > 0.1:
            self.speedMultEssen = 0.5
            self.pflanzenfressen()
        else:
            self.speedMultEssen = 1
        lwInTile = self.game.getLivingThingsInTile(self.tile)
        if self.hunger > 0.3 and not amFleischEssen:
            for gegner in lwInTile:
                if gegner.desc in self.basestats["Targets"] and self.hunger > 0.3:
                    self.angriff(gegner, min(self.popGroesse, gegner.popGroesse))
                break
        Lebewesen.everyFrame(self)

    # def randomteilen(self):
    #     if self.popGroesse >= TEILPOPGROESSEMAUS and 1 == random.randint(1, 10 * FPSGAME):
    #         groesse = random.randint(1, self.popGroesse - 1)
    #         starta = random.randint(0, 359)
    #         self.game.addCreature(type(self), (self.posx, self.posy), self.player,
    #                               starta, [self.hunger, self.alter, self.mutationen[:], groesse])
    #         self.popGroesse -= groesse


class Krabbe(Lebewesen):
    desc = "Krabbe"

    def __init__(self, game, startpos, startangle=0, info=None):
        Lebewesen.__init__(self, game, startpos, startangle, info)
        # self.moveBy(0, 0)
        # self.standardSpeed = self.speed = KRABBEV
        # self.eatSpeed = self.popGroesse * KRABBEESSEN
        # self.hungerResistenz = KRABBEHUNGERRES
        # self.standardW = FITNESS_KRABBE
        # self.hungerproframe = HUNGERKRABBE / FPSGAME
        # self.fleischfresser = True
        # self.lastAngleChange = self.game.frames
        # self.groesse = KRABBEGROESSE
        # self.standardStaerke = 0.5
        # self.opfer = ANGRIFFSLISTEKRABBE  # Die Objekte die es angreifen kann
        # self.erlaubteTerrains = [RIVER, RIVERBANK, COASTWATER, COASTGRASS, BEACH]
        # self.swim = 2
        # self.stats["OptimalTemp"], self.stats["Temprange"] = KRABBETEMP, KRABBETEMPRANGE
        # self.standardInt = KRABBEINTELLIGENZ
        # self.standardEvasion = KRABBEEVASION
        # self.standardPrecision = KRABBEPREC

    def everyFrame(self):
        if self.game.frames > self.lastAngleChange + self.stats["Decinterval"] * FPSGAME:
            self.lastAngleChange = self.game.frames
            self.changeAngle(random.random() * 360 - 180)
        moegl = self.game.getFrischFleischMenge(getTile(self.getPos()), self.basestats["Targets"])
        if moegl > 0.1 and self.hunger > 0.1:
            self.speedMultEssen = 0
            self.tierfressen(self.basestats["Targets"])
        elif self.game.getPflanzenEssen(getTile(self.getPos())) > 0.01:
            self.speedMultEssen = 0.5
            self.pflanzenfressen()
        else:
            self.speedMultEssen = 1
        if (self.game.frames - self.geboren) % 5 == 0 and self.hunger > 0.3:
            lwInTile = self.game.getLivingThingsInTile(self.tile)
            for gegner in lwInTile:
                if gegner.desc in self.basestats["Targets"]:
                    self.angriff(gegner, min(self.popGroesse, gegner.popGroesse))
                    break
        Lebewesen.everyFrame(self)

    # def randomteilen(self):
    #     if self.popGroesse >= TEILPOPGROESSEKRABBE and 1 == random.randint(1, 10 * FPSGAME):
    #         groesse = random.randint(1, self.popGroesse - 1)
    #         starta = random.randint(0, 359)
    #         self.game.addCreature(Krabbe, (self.posx, self.posy), self.player,
    #                               starta, [self.hunger, self.alter, self.mutationen[:], groesse])
    #         self.popGroesse -= groesse


class Falke(Lebewesen):
    desc = "Falke"
    basestats = FALKEBASESTATS

    def __init__(self, game, startpos, startangle=0, info=None):
        Lebewesen.__init__(self, game, startpos, startangle, info)
        # self.moveBy(0, 0)
        # self.standardSpeed = self.speed = FALKEVGEHEND
        # self.essenProSekunde = FALKEESSEN
        # self.hungerResistenz = FALKEHUNGERRES
        # self.standardW = FITNESS_FALKE
        # self.hungerproframe = HUNGERFALKEGEHEND / FPSGAME
        # self.stats["OptimalTemp"], self.stats["Temprange"] = FALKETEMP, FALKETEMPRANGE
        # self.lastAngleChange = self.game.frames
        # self.groesse = FALKEGROESSE
        # self.fleischfresser = True
        # self.pflanzenfresser = False
        # self.standardStaerke = FALKESTAERKE
        # self.opfer = ANGRIFFSLISTEFALKE  # Die Objekte die es angreifen kann
        # self.eatSpeed = FALKEESSEN
        # self.standardInt = FALKEINTELLIGENZ
        # self.standardEvasion = FALKEEVASION
        # self.standardPrecision = FALKEPREC

    def everyFrame(self):
        moegl = self.game.getFrischFleischMenge(getTile(self.getPos()), self.basestats["Targets"])
        if moegl > 0.1 and self.hunger > 0.001:
            self.nichtFliegen()
            self.speedMultEssen = 0
            self.tierfressen(self.basestats["Targets"])
            self.opferImAuge = None
        else:
            self.speedMultEssen = 1
            if self.opferImAuge == None and ((self.game.frames - self.geboren) %
                                             (self.stats["Decinterval"] / 5 * FPSGAME) == 0 and self.hunger > 0.5):
                self.opferImAuge = self.findeOpfer(1)

            if self.opferImAuge != None:
                self.fliegen()
                self.changeAngle(calcAngle(abst(self.getPos(), self.opferImAuge.getPos())), True)
                if not self.opferImAuge.alive:
                    self.opferImAuge = None
            else:
                if self.game.frames > self.lastAngleChange + self.stats["Decinterval"] * FPSGAME:
                    self.lastAngleChange = self.game.frames
                    self.changeAngle(random.random() * 90 - 45)
                if self.hunger < FALKEHUNGERRES / 2:
                    self.nichtFliegen()
                else:
                    self.fliegen()
            lwInTile = self.game.getLivingThingsInTile(self.tile)
            for gegner in lwInTile:
                if gegner.desc in self.basestats["Targets"] and self.hunger > 0.3:
                    self.angriff(gegner, min(self.popGroesse, gegner.popGroesse))
                    break
        if self.imFlug:
            self.standardSpeed = FALKEVFLIEGEND
            self.hungerproframe = HUNGERFALKEFLIEGEND / FPSGAME
        else:
            self.standardSpeed = FALKEVGEHEND
            self.hungerproframe = HUNGERFALKEGEHEND / FPSGAME
        Lebewesen.everyFrame(self)

    # def randomteilen(self):
    #     if self.popGroesse >= TEILPOPGROESSEFALKE and 1 == random.randint(1, 10 * FPSGAME):
    #         groesse = random.randint(1, self.popGroesse - 1)
    #         starta = random.randint(0, 359)
    #         self.game.addCreature(Falke, (self.posx, self.posy), self.player,
    #                               starta, [self.hunger, self.alter, self.mutationen[:], groesse])
    #         self.popGroesse -= groesse


class Singvogel(Lebewesen):
    desc = "Singvogel"
    basestats = SINGVOGELBASESTATS

    def __init__(self, game, startpos, startangle=0, info=None):
        Lebewesen.__init__(self, game, startpos, startangle, info)
        # self.moveBy(0, 0)
        # self.standardSpeed = self.speed = SINGVOGELVGEHEND
        # self.essenProSekunde = SINGVOGELESSEN
        # self.hungerResistenz = SINGVOGELHUNGERRES
        # self.standardW = FITNESS_SINGVOGEL
        # self.hungerproframe = HUNGERSINGVOGELGEHEND / FPSGAME
        # self.stats["OptimalTemp"], self.stats["Temprange"] = SINGVOGELTEMP, SINGVOGELTEMPRANGE
        # self.lastAngleChange = self.game.frames
        # self.groesse = SINGVOGELGROESSE
        # self.fleischfresser = True
        # self.pflanzenfresser = True
        # self.standardStaerke = SINGVOGELSTAERKE
        # self.opfer = ANGRIFFSLISTESINGVOGEL  # Die Objekte die es angreifen kann
        # self.eatSpeed = SINGVOGELESSEN
        # self.standardInt = SINGVOGELINTELLIGENZ
        # self.standardEvasion = SINGVOGELEVASION
        # self.standardPrecision = SINGVOGELPREC

    def everyFrame(self):
        moegl = self.game.getFrischFleischMenge(getTile(self.getPos()), self.basestats["Targets"])
        if moegl > 0.1 and self.hunger > 0.001:
            self.nichtFliegen()
            self.speedMultEssen = 0
            self.tierfressen(self.basestats["Targets"])
            self.opferImAuge = None
        else:
            self.speedMultEssen = 1
            if self.opferImAuge != None:
                self.fliegen()
                self.changeAngle(calcAngle(abst(self.getPos(), self.opferImAuge.getPos())), True)
                if not self.opferImAuge.alive:
                    self.opferImAuge = None
            elif self.opferImAuge == None and ((self.game.frames - self.geboren) %
                                               (self.stats["Decinterval"] / 5 * FPSGAME) == 0 and self.hunger > 0.5):
                self.opferImAuge = self.findeOpfer(1)
            elif self.game.getPflanzenEssen(getTile(self.getPos())) > 0.01 and self.hunger > 0.01:
                self.nichtFliegen()
                self.speedMultEssen = 0.5
                self.pflanzenfressen()
            else:
                if self.game.frames > self.lastAngleChange + self.stats["Decinterval"] * FPSGAME:
                    self.lastAngleChange = self.game.frames
                    self.changeAngle(random.random() * 90 - 45)
                if self.hunger < SINGVOGELHUNGERRES / 2:
                    self.nichtFliegen()
                else:
                    self.fliegen()
            lwInTile = self.game.getLivingThingsInTile(self.tile)
            for gegner in lwInTile:
                if gegner.desc in self.basestats["Targets"] and self.hunger > 0.5:
                    self.angriff(gegner, min(self.popGroesse, gegner.popGroesse))
                    break
        if self.imFlug:
            self.standardSpeed = SINGVOGELVFLIEGEND
            self.hungerproframe = HUNGERSINGVOGELFLIEGEND / FPSGAME
        else:
            self.standardSpeed = SINGVOGELVGEHEND
            self.hungerproframe = HUNGERSINGVOGELGEHEND / FPSGAME
        Lebewesen.everyFrame(self)

    # def randomteilen(self):
    #     if self.popGroesse >= TEILPOPGROESSESINGVOGEL and 1 == random.randint(1, 10 * FPSGAME):
    #         groesse = random.randint(1, self.popGroesse - 1)
    #         starta = random.randint(0, 359)
    #         self.game.addCreature(Singvogel, (self.posx, self.posy), self.player,
    #                               starta, [self.hunger, self.alter, self.mutationen[:], groesse])
    #         self.popGroesse -= groesse


class Doktorfisch(Lebewesen):
    desc = "Doktorfisch"

    def __init__(self, game, startpos, startangle=0, info=None):
        Lebewesen.__init__(self, game, startpos, startangle, info)
        # self.standardSpeed = self.speed = DOKTORFISCHV
        # self.moveBy(0, 0)
        # self.standardspeed = DOKTORFISCHV
        # self.eatSpeed = DOKTORFISCHESSEN
        # self.hungerResistenz = DOKTORFISCHHUNGERRES
        # self.standardW = FITNESS_DOKTORFISCH
        # self.hungerproframe = HUNGERDOKTORFISCH / FPSGAME
        # self.lastAngleChange = self.game.frames
        # self.groesse = DOKTORFISCHGROESSE
        # self.stats["OptimalTemp"], self.stats["Temprange"] = DOKTORFISCHTEMP, DOKTORFISCHTEMPRANGE
        # self.swim = 3
        # self.erlaubteTerrains = [OCEAN, COASTWATER]
        # self.standardInt = DOKTORFISCHINTELLIGENZ
        # self.standardEvasion = DOKTORFISCHEVASION
        # self.standardPrecision = DOKTORFISCHPREC

    def everyFrame(self):
        if self.game.frames > self.lastAngleChange + self.stats["Decinterval"] * FPSGAME:
            self.lastAngleChange = self.game.frames
            self.changeAngle(random.random() * 90 - 45)
        if self.game.getPflanzenEssen(getTile(self.getPos())) > 0.01:
            self.speedMultEssen = 0.5
            self.pflanzenfressen()
        else:
            self.speedMultEssen = 1
        Lebewesen.everyFrame(self)



class Aal(Lebewesen):
    desc = "Falke"

    def __init__(self, game, startpos, startangle=0, info=None):
        Lebewesen.__init__(self, game, startpos, startangle, info)
        self.moveBy(0, 0)
        self.standardSpeed = self.speed = FALKEVGEHEND
        self.essenProSekunde = FALKEESSEN
        self.hungerResistenz = FALKEHUNGERRES
        self.standardW = FITNESS_FALKE
        self.hungerproframe = HUNGERFALKEGEHEND / FPSGAME
        self.stats["OptimalTemp"], self.stats["Temprange"] = FALKETEMP, FALKETEMPRANGE
        self.lastAngleChange = self.game.frames
        self.groesse = FALKEGROESSE
        self.fleischfresser = True
        self.pflanzenfresser = False
        self.standardStaerke = 5
        self.opfer = ANGRIFFSLISTEFALKE  # Die Objekte die es angreifen kann
        self.eatSpeed = FALKEESSEN
        self.standardInt = 1
        self.standardEvasion = FALKEEVASION
        self.standardPrecision = FALKEPREC

    def everyFrame(self):
        moegl = self.game.getFrischFleischMenge(getTile(self.getPos()), self.basestats["Targets"])
        if moegl > 0.1 and self.hunger > 0.001:
            self.nichtFliegen()
            self.speedMultEssen = 0
            self.tierfressen(self.basestats["Targets"])
            self.opferImAuge = None
        else:
            self.speedMultEssen = 1
            if self.opferImAuge == None and (self.game.frames - self.geboren) % (
                    self.stats["Decinterval"] / 5 * FPSGAME) == 0 and self.hunger > 0.5:
                self.opferImAuge = self.findeOpfer(2)

            if self.opferImAuge != None:
                self.fliegen()
                self.changeAngle(calcAngle(abst(self.getPos(), self.opferImAuge.getPos())), True)
                if not self.opferImAuge.alive:
                    self.opferImAuge = None
            else:
                if self.game.frames > self.lastAngleChange + self.stats["Decinterval"] * FPSGAME:
                    self.lastAngleChange = self.game.frames
                    self.changeAngle(random.random() * 90 - 45)
                if self.hunger < FALKEHUNGERRES / 2:
                    self.nichtFliegen()
                else:
                    self.fliegen()
        lwInTile = self.game.getLivingThingsInTile(self.tile)
        for gegner in lwInTile:
            if gegner.desc in self.basestats["Targets"] and self.hunger > 0.5:
                self.angriff(gegner, min(self.popGroesse, gegner.popGroesse))
                break
        if self.imFlug:
            self.standardSpeed = FALKEVFLIEGEND
            self.hungerproframe = HUNGERFALKEFLIEGEND / FPSGAME
        else:
            self.standardSpeed = FALKEVGEHEND
            self.hungerproframe = HUNGERFALKEGEHEND / FPSGAME
        Lebewesen.everyFrame(self)



class Fuchs(Lebewesen):
    desc = "Fuchs"
    basestats = FUCHSBASESTATS

    def __init__(self, game, startpos, startangle=0, info=None):
        Lebewesen.__init__(self, game, startpos, startangle, info)
        self.standardSpeed = self.speed = FUCHSV
        self.eatSpeed = FUCHSESSEN
        self.hungerResistenz = FUCHSHUNGERRES
        self.standardW = FITNESS_FUCHS
        self.hungerproframe = HUNGERFUCHS / FPSGAME
        self.lastAngleChange = self.game.frames
        self.groesse = FUCHSGROESSE
        self.fleischfresser = True
        self.pflanzenfresser = False
        self.standardStaerke = 5
        self.opfer = ANGRIFFSLISTEFUCHS  # Die Objekte die es angreifen kann
        self.stats["OptimalTemp"], self.stats["Temprange"] = FUCHSTEMP, FUCHSTEMPRANGE
        self.standardInt = FUCHSINTELLIGENZ
        self.standardEvasion = FUCHSEVASION
        self.standardPrecision = FUCHSPREC

    def everyFrame(self):
        moegl = self.game.getFrischFleischMenge(getTile(self.getPos()), self.basestats["Targets"])
        if moegl > 0.1 and self.hunger > 0:
            self.speedMultEssen = 0
            self.tierfressen(self.basestats["Targets"])
            self.opferImAuge = None
        else:
            self.speedMultEssen = 1
            if self.opferImAuge == None and ((self.game.frames - self.geboren) %
                                             (self.stats["Decinterval"] / 5 * FPSGAME) == 0 and self.hunger > 0.5):
                self.opferImAuge = self.findeOpfer(1)

            if self.opferImAuge != None:
                self.changeAngle(calcAngle(abst(self.getPos(), self.opferImAuge.getPos())), True)
                if not self.opferImAuge.alive:
                    self.opferImAuge = None
                self.standardSpeed = FUCHSVHUNT
            else:
                if self.game.frames > self.lastAngleChange + self.stats["Decinterval"] * FPSGAME:
                    self.lastAngleChange = self.game.frames
                    self.changeAngle(random.random() * 90 - 45)
                self.standardSpeed = FUCHSV
            if self.hunger > 0.3:
                lwInTile = self.game.getLivingThingsInTile(self.tile)
                for gegner in lwInTile:
                    if gegner.desc in self.basestats["Targets"]:
                        self.angriff(gegner, min(self.popGroesse, gegner.popGroesse))
                        break
        Lebewesen.everyFrame(self)

class Kaninchen(Lebewesen):
    desc = "Kaninchen"
    basestats = KANINCHENBASESTATS

    def __init__(self, game, startpos, startangle=0, info=None):
        Lebewesen.__init__(self, game, startpos, startangle, info)
        self.standardSpeed = self.speed = KANINCHENV
        self.standardspeed = KANINCHENV
        self.eatSpeed = KANINCHENESSEN
        self.hungerResistenz = KANINCHENHUNGERRES
        self.standardW = FITNESS_KANINCHEN
        self.hungerproframe = HUNGERKANINCHEN / FPSGAME
        self.lastAngleChange = self.game.frames
        self.groesse = KANINCHENGROESSE
        self.stats["OptimalTemp"], self.stats["Temprange"] = KANINCHENTEMP, KANINCHENTEMPRANGE
        self.standardInt = KANINCHENINTELLIGENZ
        self.standardEvasion = KANINCHENEVASION
        self.standardPrecision = KANINCHENPREC

    def everyFrame(self):
        if self.game.frames > self.lastAngleChange + self.stats["Decinterval"] * FPSGAME:
            self.lastAngleChange = self.game.frames
            self.changeAngle(random.random() * 90 - 45)
        if self.game.getPflanzenEssen(getTile(self.getPos())) > 0.01:
            self.speedMultEssen = 0
            self.pflanzenfressen()
        else:
            self.speedMultEssen = 1
        Lebewesen.everyFrame(self)



class Ziege(Lebewesen):
    desc = "Ziege"
    basestats = ZIEGEBASESTATS

    def __init__(self, game, startpos, startangle=0, info=None):
        Lebewesen.__init__(self, game, startpos, startangle, info)
        self.standardSpeed = self.speed = ZIEGEV
        self.standardspeed = ZIEGEV
        self.eatSpeed = ZIEGEESSEN
        self.hungerResistenz = ZIEGEHUNGERRES
        self.standardW = FITNESS_ZIEGE
        self.hungerproframe = HUNGERZIEGE / FPSGAME
        self.lastAngleChange = self.game.frames
        self.groesse = ZIEGEGROESSE
        self.stats["OptimalTemp"], self.stats["Temprange"] = ZIEGETEMP, ZIEGETEMPRANGE
        self.standardInt = ZIEGEINTELLIGENZ
        self.affinitaet = [SNOWYMOUNTAIN, LOWMOUNTAINS, HIGHMOUNTAIN]
        self.standardEvasion = ZIEGEEVASION

    def everyFrame(self):
        if self.game.frames > self.lastAngleChange + self.stats["Decinterval"] * FPSGAME:
            self.lastAngleChange = self.game.frames
            self.changeAngle(random.random() * 90 - 45)
        if self.game.getPflanzenEssen(getTile(self.getPos())) > 0.01:
            self.speedMultEssen = 0.5
            self.pflanzenfressen()
        else:
            self.speedMultEssen = 1
        Lebewesen.everyFrame(self)

    def getSpeedMultInTerrain(self):
        if self.terrain in (HIGHMOUNTAIN, SNOWYMOUNTAIN, LOWMOUNTAINS):
            return 1
        return Lebewesen.getSpeedMultInTerrain(self)
