import random
from helpfunctions import *
from animalstats import *
from gameconstants import *
from terrainstats import *
from mutations import *

class Lebewesen:
    desc = "basicLebewesen"

    def __init__(self, game, startpos=(400, 400), startangle=None, info=None):
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
            self.hunger = 0  # Durchschnittlicher Hunger der Lebewesen
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
        self.erlaubteTerrains = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        self.opferImAuge = None
        self.geboren = self.game.frames
        self.standardInt = 0
        self.intelligence = 0
        self.standardEvasion = 0
        self.standardPrecision = 0
        self.lastAttack = self.game.frames
        # Erstelle Dict von mutierten stats
        self.mutierteStats = {}
        for stat in STATSZUMUTIEREN:
            self.mutierteStats[stat] = 0
        for mut in self.mutationen:
            for stat in mut:
                self.mutierteStats[stat] += mut[stat]

    def moveBy(self, x, y, force=False):
        tileVorher = self.tile
        terrainVorher = self.terrain
        self.posx += x
        self.posy += y
        self.posx = max(0, min(self.posx, 16 * self.game.tilenbrx - 0.1))
        self.posy = max(0, min(self.posy, 16 * self.game.tilenbry - 0.1))
        if self.posx == 0 or self.posy == 0 or self.posx == 16 * self.game.tilenbrx - 0.1 or self.posy == 16 * self.game.tilenbry - 0.1:
            self.angle += 180
        self.testForTerrain()
        self.intelligence = (self.standardInt + self.mutierteStats["INTFLAT"]) * (1 + self.mutierteStats["INTMULT"])
        if not force:
            if random.random() > np.power(2.0, -self.intelligence):
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
        mutfaktor = 1 + self.mutierteStats["SPEED"]
        self.setSpeed(self.standardSpeed * self.speedMultEssen * self.speedMultTerrain * self.speedMultMisc * mutfaktor)
        self.moveBy(self.vx / FPSGAME, self.vy / FPSGAME)

    def setSpeed(self, v):
        self.speed = v
        self.vx, self.vy = getSpeeds(self.speed, self.angle)

    def getPos(self):
        return self.posx, self.posy

    def changeAngle(self, angle, to=False):
        """if to is set to True, then the angle is set to angle,
        else it changes the angle by angle"""
        if to:
            self.angle = angle
        else:
            self.angle += angle
        self.vx, self.vy = getSpeeds(self.speed, self.angle)

    def everyFrame(self):
        if (self.game.frames - self.geboren) % POPANPASSENINTERVAL == 0:
            self.populationAnpassen()
        self.reactToTerrain()
        self.move()
        self.randomteilen()
        self.staerke = self.standardStaerke

    def pflanzenfressen(self):
        if self.pflanzenfresser and self.alive:
            kapazitaet = self.hunger * self.popGroesse
            verfuegbar = self.game.getPflanzenEssen(getTile(self.getPos()))
            essenMenge = min(kapazitaet, verfuegbar,
                             self.eatSpeed * self.popGroesse / FPSGAME)
            self.game.setPflanzenEssen(getTile(self.getPos()), verfuegbar - essenMenge)
            self.hunger -= essenMenge / self.popGroesse

    def populationAnpassen(self):
        zeitVerg = POPANPASSENINTERVAL / FPSGAME
        if self.alive:
            # Wahrscheinlichkeit, dass ein Mitglied sich vermehrt
            w = self.getFitness()
            baseP = (0.001 * min(0, (1 - abs(w - 1))) * zeitVerg) * self.popGroesse
            if w >= 1:
                pEinesMehr = baseP + ((w - 1) * zeitVerg) * self.popGroesse
                pEinesWeniger = baseP
            else:
                pEinesWeniger = baseP + (1 - w) * zeitVerg * self.popGroesse
                pEinesMehr = baseP
            einsMehr = int(random.random() < pEinesMehr)
            aenderung = einsMehr - int(random.random() < pEinesWeniger)
            self.hunger += self.hungerproframe + einsMehr / self.popGroesse
            self.changePop(aenderung)

    def mutate(self, mutation):
        self.mutationen.append(mutation)
        for stat in mutation:
            self.mutierteStats[stat] += mutation[stat]

    def testForTerrain(self):
        self.terrain = self.game.getTerrain((self.posx, self.posy))

    def reactToTerrain(self):
        self.testForTerrain()
        if self.vorherigesterrain == self.terrain:
            self.terraincounter += 1
            if self.terraincounter > ANPASSUNGSEKUNDEN * FPSGAME:
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
            essenMenge = min(kapazitaet, self.eatSpeed * self.popGroesse / FPSGAME)
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

    def getFitness(self):
        mutboost = (self.standardW - 1) * self.mutierteStats["FITNESS"]
        tmp = self.game.getTemp(self.terrain, self.tile)
        temperaturAnpassung = np.exp(-((tmp - self.optimalTemp) / self.tempRange) ** 2 / 2)
        w1 = (self.standardW + mutboost - (self.hunger / self.hungerResistenz) ** 3 * TODFAKTOR)
        ##print(temperaturAnpassung, w1)
        return w1 * np.power(temperaturAnpassung, TEMPANPASSKOEFF)

    def getEvasion(self):
        mutbonus = self.mutierteStats["EVASION"]
        return self.standardEvasion + mutbonus

    def getPrecision(self):
        mutbonus = self.mutierteStats["PRECISION"]
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

    def __init__(self, game, startpos, startangle=0, info=None):
        if info == None:
            self.popGroesse = 15
            infoweiter = None
        else:
            h, a, m, self.popGroesse = info
            infoweiter = (h, a, m)
        Lebewesen.__init__(self, game, startpos, startangle, infoweiter)
        self.standardSpeed = self.speed = SCHNECKEV
        self.standardspeed = SCHNECKEV
        self.eatSpeed = SCHNECKEESSEN
        self.hungerResistenz = SCHNECKEHUNGERRES
        self.standardW = FITNESS_SCHNECKE
        self.hungerproframe = HUNGERSCHNECKE / FPSGAME
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
        if self.game.frames > self.lastAngleChange + SCHNECKEDECINTERVAL * FPSGAME:
            self.lastAngleChange = self.game.frames
            self.changeAngle(random.random() * 90 - 45)
        if self.game.getPflanzenEssen(getTile(self.getPos())) > 0.01:
            self.speedMultEssen = 0.5
            self.pflanzenfressen()
        else:
            self.speedMultEssen = 1
        Lebewesen.everyFrame(self)

    def randomteilen(self):
        if self.popGroesse >= TEILPOPGROESSESCHNECKE and 1 == random.randint(1, 10 * FPSGAME):
            groesse = random.randint(1, self.popGroesse - 1)
            starta = random.randint(0, 359)
            self.game.addCreature(Schnecke, (self.posx, self.posy), self.player,
                                  starta, [self.hunger, self.alter, self.mutationen[:], groesse])
            self.popGroesse -= groesse


class Kaefer(Lebewesen):
    desc = "Käfer"

    def __init__(self, game, startpos, startangle=0, info=None):
        if info == None:
            self.popGroesse = 20
            infoweiter = None
        else:
            h, a, m, self.popGroesse = info
            infoweiter = (h, a, m)
        Lebewesen.__init__(self, game, startpos, startangle, infoweiter)
        self.standardSpeed = self.speed = KAEFERV
        self.standardspeed = KAEFERV
        self.eatSpeed = self.popGroesse * KAEFERESSEN
        self.hungerResistenz = KAEFERHUNGERRES
        self.standardW = FITNESS_KAEFER
        self.hungerproframe = HUNGERKAEFER / FPSGAME
        self.lastAngleChange = self.game.frames
        self.groesse = KAEFERGROESSE
        self.optimalTemp, self.tempRange = KAEFERTEMP, KAEFERTEMPRANGE
        self.standardEvasion = KAEFEREVASION
        self.standardPrecision = KAEFERPREC

    def everyFrame(self):
        if self.game.frames > self.lastAngleChange + KAEFERDECINTERVAL * FPSGAME:
            self.lastAngleChange = self.game.frames
            self.changeAngle(random.random() * 90 - 45)
        if self.game.getPflanzenEssen(getTile(self.getPos())) > 0.01:
            self.speedMultEssen = 0.5
            self.pflanzenfressen()
        else:
            self.speedMultEssen = 1
        Lebewesen.everyFrame(self)

    def randomteilen(self):
        if self.popGroesse >= TEILPOPGROESSEKAEFER and 1 == random.randint(1, 10 * FPSGAME):
            groesse = random.randint(1, self.popGroesse - 1)
            starta = random.randint(0, 359)
            self.game.addCreature(Kaefer, (self.posx, self.posy), self.player,
                                  starta, [self.hunger, self.alter, self.mutationen[:], groesse])
            self.popGroesse -= groesse


class Maus(Lebewesen):
    desc = "Maus"

    def __init__(self, game, startpos, startangle=0, info=None):
        if info == None:
            self.popGroesse = 5
            infoweiter = None
        else:
            h, a, m, self.popGroesse = info
            infoweiter = (h, a, m)
        Lebewesen.__init__(self, game, startpos, startangle, infoweiter)
        self.standardSpeed = self.speed = MAUSV
        self.eatSpeed = MAUSESSEN
        self.hungerResistenz = MAUSHUNGERRES
        self.standardW = FITNESS_MAUS
        self.hungerproframe = HUNGERMAUS / FPSGAME
        self.lastAngleChange = self.game.frames
        self.groesse = MAUSGROESSE
        self.fleischfresser = True
        self.standardStaerke = MAUSSTAERKE
        self.opfer = ANGRIFFSLISTEMAUS  # Die Objekte die es angreifen kann
        self.optimalTemp, self.tempRange = MAUSTEMP, MAUSTEMPRANGE
        self.standardInt = MAUSINTELLIGENZ
        self.standardEvasion = MAUSEVASION
        self.standardPrecision = MAUSPREC

    def everyFrame(self):
        if self.game.frames > self.lastAngleChange + MAUSDECINTERVAL * FPSGAME:
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
        if self.popGroesse >= TEILPOPGROESSEMAUS and 1 == random.randint(1, 10 * FPSGAME):
            groesse = random.randint(1, self.popGroesse - 1)
            starta = random.randint(0, 359)
            self.game.addCreature(Maus, (self.posx, self.posy), self.player,
                                  starta, [self.hunger, self.alter, self.mutationen[:], groesse])
            self.popGroesse -= groesse


class Krabbe(Lebewesen):
    desc = "Krabbe"

    def __init__(self, game, startpos, startangle=0, info=None):
        if info == None:
            self.popGroesse = 10
            infoweiter = None
        else:
            h, a, m, self.popGroesse = info
            infoweiter = (h, a, m)
        Lebewesen.__init__(self, game, startpos, startangle, infoweiter)
        self.moveBy(0, 0)
        self.standardSpeed = self.speed = KRABBEV
        self.eatSpeed = self.popGroesse * KRABBEESSEN
        self.hungerResistenz = KRABBEHUNGERRES
        self.standardW = FITNESS_KRABBE
        self.hungerproframe = HUNGERKRABBE / FPSGAME
        self.fleischfresser = True
        self.lastAngleChange = self.game.frames
        self.groesse = KRABBEGROESSE
        self.standardStaerke = 0.5
        self.opfer = ANGRIFFSLISTEKRABBE  # Die Objekte die es angreifen kann
        self.erlaubteTerrains = [RIVER, RIVERBANK, COASTWATER, COASTGRASS, BEACH]
        self.swim = 2
        self.optimalTemp, self.tempRange = KRABBETEMP, KRABBETEMPRANGE
        self.standardInt = KRABBEINTELLIGENZ
        self.standardEvasion = KRABBEEVASION
        self.standardPrecision = KRABBEPREC

    def everyFrame(self):
        if self.game.frames > self.lastAngleChange + KRABBEDECINTERVAL * FPSGAME:
            self.lastAngleChange = self.game.frames
            self.changeAngle(random.random() * 360 - 180)
        moegl = self.game.getFrischFleischMenge(getTile(self.getPos()), self.opfer)
        if moegl > 0.1 and self.hunger > 0.1:
            self.speedMultEssen = 0
            self.tierfressen(self.opfer)
        elif self.game.getPflanzenEssen(getTile(self.getPos())) > 0.01:
            self.speedMultEssen = 0.5
            self.pflanzenfressen()
        else:
            self.speedMultEssen = 1
        if (self.game.frames - self.geboren) % 5 == 0 and self.hunger > 0.3:
            lwInTile = self.game.getLivingThingsInTile(self.tile)
            for gegner in lwInTile:
                if gegner.desc in self.opfer:
                    self.angriff(gegner, min(self.popGroesse, gegner.popGroesse))
                    break
        Lebewesen.everyFrame(self)

    def randomteilen(self):
        if self.popGroesse >= TEILPOPGROESSEKRABBE and 1 == random.randint(1, 10 * FPSGAME):
            groesse = random.randint(1, self.popGroesse - 1)
            starta = random.randint(0, 359)
            self.game.addCreature(Krabbe, (self.posx, self.posy), self.player,
                                  starta, [self.hunger, self.alter, self.mutationen[:], groesse])
            self.popGroesse -= groesse


class Falke(Lebewesen):
    desc = "Falke"

    def __init__(self, game, startpos, startangle=0, info=None):
        if info == None:
            self.popGroesse = 5
            infoweiter = None
        else:
            h, a, m, self.popGroesse = info
            infoweiter = (h, a, m)
        Lebewesen.__init__(self, game, startpos, startangle, infoweiter)
        self.moveBy(0, 0)
        self.standardSpeed = self.speed = FALKEVGEHEND
        self.essenProSekunde = FALKEESSEN
        self.hungerResistenz = FALKEHUNGERRES
        self.standardW = FITNESS_FALKE
        self.hungerproframe = HUNGERFALKEGEHEND / FPSGAME
        self.optimalTemp, self.tempRange = FALKETEMP, FALKETEMPRANGE
        self.lastAngleChange = self.game.frames
        self.groesse = FALKEGROESSE
        self.fleischfresser = True
        self.pflanzenfresser = False
        self.standardStaerke = FALKESTAERKE
        self.opfer = ANGRIFFSLISTEFALKE  # Die Objekte die es angreifen kann
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
            if self.opferImAuge == None and ((self.game.frames - self.geboren) %
                                             (FALKEDECINTERVAL / 5 * FPSGAME) == 0 and self.hunger > 0.5):
                self.opferImAuge = self.findeOpfer(1)

            if self.opferImAuge != None:
                self.fliegen()
                self.changeAngle(calcAngle(abst(self.getPos(), self.opferImAuge.getPos())), True)
                if not self.opferImAuge.alive:
                    self.opferImAuge = None
            else:
                if self.game.frames > self.lastAngleChange + FALKEDECINTERVAL * FPSGAME:
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
        if self.popGroesse >= TEILPOPGROESSEFALKE and 1 == random.randint(1, 10 * FPSGAME):
            groesse = random.randint(1, self.popGroesse - 1)
            starta = random.randint(0, 359)
            self.game.addCreature(Falke, (self.posx, self.posy), self.player,
                                  starta, [self.hunger, self.alter, self.mutationen[:], groesse])
            self.popGroesse -= groesse


class Singvogel(Lebewesen):
    desc = "Singvogel"

    def __init__(self, game, startpos, startangle=0, info=None):
        if info == None:
            self.popGroesse = 7
            infoweiter = None
        else:
            h, a, m, self.popGroesse = info
            infoweiter = (h, a, m)
        Lebewesen.__init__(self, game, startpos, startangle, infoweiter)
        self.moveBy(0, 0)
        self.standardSpeed = self.speed = SINGVOGELVGEHEND
        self.essenProSekunde = SINGVOGELESSEN
        self.hungerResistenz = SINGVOGELHUNGERRES
        self.standardW = FITNESS_SINGVOGEL
        self.hungerproframe = HUNGERSINGVOGELGEHEND / FPSGAME
        self.optimalTemp, self.tempRange = SINGVOGELTEMP, SINGVOGELTEMPRANGE
        self.lastAngleChange = self.game.frames
        self.groesse = SINGVOGELGROESSE
        self.fleischfresser = True
        self.pflanzenfresser = True
        self.standardStaerke = SINGVOGELSTAERKE
        self.opfer = ANGRIFFSLISTESINGVOGEL  # Die Objekte die es angreifen kann
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
                self.changeAngle(calcAngle(abst(self.getPos(), self.opferImAuge.getPos())), True)
                if not self.opferImAuge.alive:
                    self.opferImAuge = None
            elif self.opferImAuge == None and ((self.game.frames - self.geboren) %
                                               (SINGVOGELDECINTERVAL / 5 * FPSGAME) == 0 and self.hunger > 0.5):
                self.opferImAuge = self.findeOpfer(1)
            elif self.game.getPflanzenEssen(getTile(self.getPos())) > 0.01 and self.hunger > 0.01:
                self.nichtFliegen()
                self.speedMultEssen = 0.5
                self.pflanzenfressen()
            else:
                if self.game.frames > self.lastAngleChange + SINGVOGELDECINTERVAL * FPSGAME:
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
        if self.popGroesse >= TEILPOPGROESSESINGVOGEL and 1 == random.randint(1, 10 * FPSGAME):
            groesse = random.randint(1, self.popGroesse - 1)
            starta = random.randint(0, 359)
            self.game.addCreature(Singvogel, (self.posx, self.posy), self.player,
                                  starta, [self.hunger, self.alter, self.mutationen[:], groesse])
            self.popGroesse -= groesse


class Doktorfisch(Lebewesen):
    desc = "Doktorfisch"

    def __init__(self, game, startpos, startangle=0, info=None):
        if info == None:
            self.popGroesse = 10
            infoweiter = None
        else:
            h, a, m, self.popGroesse = info
            infoweiter = (h, a, m)
        Lebewesen.__init__(self, game, startpos, startangle, infoweiter)
        self.standardSpeed = self.speed = DOKTORFISCHV
        self.moveBy(0, 0)
        self.standardspeed = DOKTORFISCHV
        self.eatSpeed = DOKTORFISCHESSEN
        self.hungerResistenz = DOKTORFISCHHUNGERRES
        self.standardW = FITNESS_DOKTORFISCH
        self.hungerproframe = HUNGERDOKTORFISCH / FPSGAME
        self.lastAngleChange = self.game.frames
        self.groesse = DOKTORFISCHGROESSE
        self.optimalTemp, self.tempRange = DOKTORFISCHTEMP, DOKTORFISCHTEMPRANGE
        self.swim = 3
        self.erlaubteTerrains = [OCEAN, COASTWATER]
        self.standardInt = DOKTORFISCHINTELLIGENZ
        self.standardEvasion = DOKTORFISCHEVASION
        self.standardPrecision = DOKTORFISCHPREC

    def everyFrame(self):
        if self.game.frames > self.lastAngleChange + DOKTORFISCHDECINTERVAL * FPSGAME:
            self.lastAngleChange = self.game.frames
            self.changeAngle(random.random() * 90 - 45)
        if self.game.getPflanzenEssen(getTile(self.getPos())) > 0.01:
            self.speedMultEssen = 0.5
            self.pflanzenfressen()
        else:
            self.speedMultEssen = 1
        Lebewesen.everyFrame(self)

    def randomteilen(self):
        if self.popGroesse >= TEILPOPGROESSEDOKTORFISCH and 1 == random.randint(1, 10 * FPSGAME):
            groesse = random.randint(1, self.popGroesse - 1)
            starta = random.randint(0, 359)
            self.game.addCreature(Doktorfisch, (self.posx, self.posy), self.player,
                                  starta, [self.hunger, self.alter, self.mutationen[:], groesse])
            self.popGroesse -= groesse


class Aal(Lebewesen):
    desc = "Falke"

    def __init__(self, game, startpos, startangle=0, info=None):
        if info == None:
            self.popGroesse = 5
            infoweiter = None
        else:
            h, a, m, self.popGroesse = info
            infoweiter = (h, a, m)
        Lebewesen.__init__(self, game, startpos, startangle, infoweiter)
        self.moveBy(0, 0)
        self.standardSpeed = self.speed = FALKEVGEHEND
        self.essenProSekunde = FALKEESSEN
        self.hungerResistenz = FALKEHUNGERRES
        self.standardW = FITNESS_FALKE
        self.hungerproframe = HUNGERFALKEGEHEND / FPSGAME
        self.optimalTemp, self.tempRange = FALKETEMP, FALKETEMPRANGE
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
        moegl = self.game.getFrischFleischMenge(getTile(self.getPos()), self.opfer)
        if moegl > 0.1 and self.hunger > 0.001:
            self.nichtFliegen()
            self.speedMultEssen = 0
            self.tierfressen(self.opfer)
            self.opferImAuge = None
        else:
            self.speedMultEssen = 1
            if self.opferImAuge == None and (self.game.frames - self.geboren) % (
                    FALKEDECINTERVAL / 5 * FPSGAME) == 0 and self.hunger > 0.5:
                self.opferImAuge = self.findeOpfer(2)

            if self.opferImAuge != None:
                self.fliegen()
                self.changeAngle(calcAngle(abst(self.getPos(), self.opferImAuge.getPos())), True)
                if not self.opferImAuge.alive:
                    self.opferImAuge = None
            else:
                if self.game.frames > self.lastAngleChange + FALKEDECINTERVAL * FPSGAME:
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
        if self.popGroesse >= TEILPOPGROESSEFALKE and 1 == random.randint(1, 10 * FPSGAME):
            groesse = random.randint(1, self.popGroesse - 1)
            starta = random.randint(0, 359)
            self.game.addCreature(Falke, (self.posx, self.posy), self.player,
                                  starta, [self.hunger, self.alter, self.mutationen[:], groesse])
            self.popGroesse -= groesse


class Fuchs(Lebewesen):
    desc = "Fuchs"

    def __init__(self, game, startpos, startangle=0, info=None):
        if info == None:
            self.popGroesse = 3
            infoweiter = None
        else:
            h, a, m, self.popGroesse = info
            infoweiter = (h, a, m)
        Lebewesen.__init__(self, game, startpos, startangle, infoweiter)
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
            if self.opferImAuge == None and ((self.game.frames - self.geboren) %
                                             (FUCHSDECINTERVAL / 5 * FPSGAME) == 0 and self.hunger > 0.5):
                self.opferImAuge = self.findeOpfer(1)

            if self.opferImAuge != None:
                self.changeAngle(calcAngle(abst(self.getPos(), self.opferImAuge.getPos())), True)
                if not self.opferImAuge.alive:
                    self.opferImAuge = None
                self.standardSpeed = FUCHSVHUNT
            else:
                if self.game.frames > self.lastAngleChange + MAUSDECINTERVAL * FPSGAME:
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
        if self.popGroesse >= TEILPOPGROESSEFUCHS and 1 == random.randint(1, 10 * FPSGAME):
            groesse = random.randint(1, self.popGroesse - 1)
            starta = random.randint(0, 359)
            self.game.addCreature(Fuchs, (self.posx, self.posy), self.player,
                                  starta, [self.hunger, self.alter, self.mutationen[:], groesse])
            self.popGroesse -= groesse


class Kaninchen(Lebewesen):
    desc = "Kaninchen"

    def __init__(self, game, startpos, startangle=0, info=None):
        if info == None:
            self.popGroesse = 5
            infoweiter = None
        else:
            h, a, m, self.popGroesse = info
            infoweiter = (h, a, m)
        Lebewesen.__init__(self, game, startpos, startangle, infoweiter)
        self.standardSpeed = self.speed = KANINCHENV
        self.standardspeed = KANINCHENV
        self.eatSpeed = KANINCHENESSEN
        self.hungerResistenz = KANINCHENHUNGERRES
        self.standardW = FITNESS_KANINCHEN
        self.hungerproframe = HUNGERKANINCHEN / FPSGAME
        self.lastAngleChange = self.game.frames
        self.groesse = KANINCHENGROESSE
        self.optimalTemp, self.tempRange = KANINCHENTEMP, KANINCHENTEMPRANGE
        self.standardInt = KANINCHENINTELLIGENZ
        self.standardEvasion = KANINCHENEVASION
        self.standardPrecision = KANINCHENPREC

    def everyFrame(self):
        if self.game.frames > self.lastAngleChange + KANINCHENDECINTERVAL * FPSGAME:
            self.lastAngleChange = self.game.frames
            self.changeAngle(random.random() * 90 - 45)
        if self.game.getPflanzenEssen(getTile(self.getPos())) > 0.01:
            self.speedMultEssen = 0
            self.pflanzenfressen()
        else:
            self.speedMultEssen = 1
        Lebewesen.everyFrame(self)

    def randomteilen(self):
        if self.popGroesse >= TEILPOPGROESSEKANINCHEN and 1 == random.randint(1, 10 * FPSGAME):
            groesse = random.randint(1, self.popGroesse - 1)
            starta = random.randint(0, 359)
            self.game.addCreature(Kaninchen, (self.posx, self.posy), self.player,
                                  starta, [self.hunger, self.alter, self.mutationen[:], groesse])
            self.popGroesse -= groesse


class Ziege(Lebewesen):
    desc = "Ziege"

    def __init__(self, game, startpos, startangle=0, info=None):
        if info == None:
            self.popGroesse = 4
            infoweiter = None
        else:
            h, a, m, self.popGroesse = info
            infoweiter = (h, a, m)
        Lebewesen.__init__(self, game, startpos, startangle, infoweiter)
        self.standardSpeed = self.speed = ZIEGEV
        self.standardspeed = ZIEGEV
        self.eatSpeed = ZIEGEESSEN
        self.hungerResistenz = ZIEGEHUNGERRES
        self.standardW = FITNESS_ZIEGE
        self.hungerproframe = HUNGERZIEGE / FPSGAME
        self.lastAngleChange = self.game.frames
        self.groesse = ZIEGEGROESSE
        self.optimalTemp, self.tempRange = ZIEGETEMP, ZIEGETEMPRANGE
        self.standardInt = ZIEGEINTELLIGENZ
        self.affinitaet = [SNOWYMOUNTAIN, LOWMOUNTAINS, HIGHMOUNTAIN]
        self.standardEvasion = ZIEGEEVASION

    def everyFrame(self):
        if self.game.frames > self.lastAngleChange + ZIEGEDECINTERVAL * FPSGAME:
            self.lastAngleChange = self.game.frames
            self.changeAngle(random.random() * 90 - 45)
        if self.game.getPflanzenEssen(getTile(self.getPos())) > 0.01:
            self.speedMultEssen = 0.5
            self.pflanzenfressen()
        else:
            self.speedMultEssen = 1
        Lebewesen.everyFrame(self)

    def randomteilen(self):
        if self.popGroesse >= TEILPOPGROESSEZIEGE and 1 == random.randint(1, 10 * FPSGAME):
            groesse = random.randint(1, self.popGroesse - 1)
            starta = random.randint(0, 359)
            self.game.addCreature(Ziege, (self.posx, self.posy), self.player,
                                  starta, [self.hunger, self.alter, self.mutationen[:], groesse])
            self.popGroesse -= groesse

    def speedMultInTerrain(self):
        if self.terrain in (HIGHMOUNTAIN, SNOWYMOUNTAIN, LOWMOUNTAINS):
            return 1
        return Lebewesen.speedMultInTerrain(self)
