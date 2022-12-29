# letzte Änderung:14.04.2020
# Sebastian Bittner, Stephan Buchner

import sys
from gameelements import *
from network import *
from widgets import *
from skilltreeclass import *
from cards import *

SONG_END = pygame.USEREVENT + 1


def handkarten(stonetype):
    anzahl_karten = random.choices(list(range(len(stonetype))),
                                   [STONEGEWICHTUNG * zahl_steine + 1 for zahl_steine in stonetype], k=HANDKARTEN)
    return choosecardintype(anzahl_karten)


def choosecardintype(anzahl_karten):
    handcards = []
    for typ in anzahl_karten:
        card = random.choice(KARTEN_VORHANDEN[typ])
        if card != None:
            handcards.append(card())
    return handcards


# Klasse die alles ausfuehrt###############################################################

class Execute:
    def __init__(self, screen, images):
        self.origImages = images
        self.workingImages = {}
        self.uhr = pygame.time.Clock()
        self.screen = screen
        self.inmenu = True
        self.ingame = False
        self.inlvlmenu = False
        self.options = False
        self.posmap = (0, 0)
        self.zugpause = False
        self.zeigeSpieler = True
        self.zeigeStats = False
        for img in images:
            val = images[img]
            self.workingImages[img] = pygame.transform.scale(val[0], val[2])
        self.specialInfoAnimals = []  # Tiere für die man spezielle Info anfragt
        self.messages = []

        # Muss als letztes stehen
        self.menu()

    def menu(self):
        pygame.mixer.music.load(random.choice(music))
        pygame.mixer.music.play()
        SONG_END = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(SONG_END)
        self.button_list = BUTTONS
        self.buttonslvl_list = LVLS
        self.lvlbutton_list = []
        self.buttons = []
        self.txt = []
        i = 100
        self.font2 = pygame.font.SysFont("chiller", 50)
        for label in self.button_list:
            button = pygame.Rect(int(BREITE // 20), int(HOEHE // 8 + i), GROESSEBUTTONS, GROESSEBUTTONS // 5)
            i += 100
            self.buttons.append(button)
            text = self.font2.render(label, 1, SCHWARZ)
            self.txt.append(text)
        while True:
            self.uhr.tick(FPSMENU)
            self.menuanimieren()
            for event in pygame.event.get():
                mx, my = pygame.mouse.get_pos()
                click = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        click = True
                    if self.buttons[0].collidepoint((mx, my)):
                        if click:
                            self.singleplayermenu()
                    if self.buttons[1].collidepoint((mx, my)):
                        if click:
                            self.ipmenu()
                    if self.buttons[2].collidepoint((mx, my)):
                        if click:
                            self.options()
                    if self.buttons[3].collidepoint((mx, my)):
                        if click:
                            pygame.quit()
                            sys.exit()
                self.standardHandling(event)

    def singleplayermenu(self):
        i = 0
        for label in self.buttonslvl_list:
            i += 100
            button = ButtonNormal((BREITE // 2 - (GROESSEBUTTONS // 2), 300 + i), label)
            self.lvlbutton_list.append(button)
        while True:
            self.uhr.tick(FPSMENU)
            self.singleplayermenuanimieren()
            for event in pygame.event.get():
                mx, my = pygame.mouse.get_pos()
                click = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        click = True
                        for button in self.lvlbutton_list:
                            if button.checkCollision((mx, my)):
                                map = self.lvlbutton_list.index(button)
                                self.startSinglePlayerGame(map)
                self.standardHandling(event)

    def ipmenu(self):
        buttonEnter = ButtonNormal((int(BREITE // 2 - 150), int(HOEHE // 2)), "Verbinden")
        buttonReturn = ButtonNormal((int(BREITE // 2 - 150), int(HOEHE // 2 + 100)), "Zurück")
        try:
            file = open("lastip.txt", "r")
            lastIp = file.read()
            file.close()
        except:
            lastIp = ""
        self.ipFeld = TextFeld((int(BREITE // 2 - 150), int(HOEHE // 2) - 100), lastIp,
                               self.font2)
        self.ipMenuButtons = (buttonEnter, buttonReturn)
        while True:
            self.uhr.tick(FPSMENU)
            self.ipmenuanimieren()
            for event in pygame.event.get():
                mx, my = pygame.mouse.get_pos()
                click = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        click = True
                    if buttonEnter.checkCollision((mx, my)):
                        if click:
                            ip = self.ipFeld.text
                            self.enterMultiPlayerGame(ip)
                            return
                    if buttonReturn.checkCollision((mx, my)):
                        if click:
                            return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        ip = self.ipFeld.text
                        self.enterMultiPlayerGame(ip)
                        return
                    else:
                        self.ipFeld.keystroke(event)
                self.standardHandling(event)

    def enterMultiPlayerGame(self, ip):
        f = open("lastip.txt", "w")
        f.write(ip)
        f.close()
        self.theNetwork = Network(ip)
        self.playerNumber, self.mapNr = self.theNetwork.getStartInfo()
        self.mapPicture = MAPPICTURES[self.mapNr]
        self.tilenbr = MAPFILES[self.mapNr][1]
        self.tilenbrx, self.tilenbry = self.tilenbr
        self.singleplayer = False
        self.runGame()

    def startSinglePlayerGame(self, mapNr):
        self.mapNr = mapNr
        self.mapPicture = MAPPICTURES[mapNr]
        self.mapFile, self.tilenbr = MAPFILES[mapNr]
        self.tilenbrx, self.tilenbry = self.tilenbr
        self.singleplayer = True
        self.game = Game(mapNr)
        self.runGame()

    def runGame(self):
        pygame.mixer.music.set_endevent(SONG_END)
        self.inGame = True
        self.gameover = False
        self.inskilltree = False
        self.testsktr = Skilltree(pygame.Surface(GROESSE), "slug")
        self.skilltreePoints = 4
        mausx, mauxy = self.mauspos = (0, 0)
        mapverschieben = False
        self.oikeymemory = [False, False]
        self.button_list = TIERE
        self.buttonsgame = []
        self.tiere = []
        self.font2 = pygame.font.SysFont("Times", 30)
        self.zoomfaktor = 1
        self.mapzoomed = zuschneiden_image(self.mapPicture,
                                           self.getMapPos((0, 0)) + mult((BARBREITE, HOEHE), 1, True))
        i = 40
        for label in self.button_list:
            button = ButtonGame((BARBREITE + 30, i), label)
            i += 50
            self.buttonsgame.append(button)
        self.buttonsgame.append(ButtonGame((BARBREITE + 30, i), "Skilltree"))
        self.framescounterzug = 0
        self.msg = [False]

        # self.interpretServerMsg(incMsg)
        while self.inGame:
            self.uhr.tick(FPSGAME)
            if not self.singleplayer:
                self.msg.append((INFOANIMALS, self.specialInfoAnimals))
                incMsg = self.theNetwork.send(self.msg)
                self.msg = [False]
                self.interpretServerMsg(incMsg)
            else:
                if self.game.frames % (FPSGAME * SEKUNDENZUG) == 0:
                    self.neuerZug()
                self.game.step()
                self.gameInfo = self.game.livingThings
            if not self.inskilltree:
                self.animieren()
            else:
                self.animierenSkillTree()

            if self.oikeymemory[0] and self.zoomfaktor >= 0.5:
                self.zoom(ZOOM)
            if self.oikeymemory[1] and self.zoomfaktor <= 4:
                self.zoom(1 / ZOOM)

            for event in pygame.event.get():
                self.standardHandling(event)
                mx, my = pygame.mouse.get_pos()
                click = False
                # zoomen
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_k:
                        self.killserver()
                    if event.key == pygame.K_m:
                        return
                    if event.key == pygame.K_o:
                        self.oikeymemory[0] = True

                    if event.key == pygame.K_c:
                        self.zeigeSpieler = not self.zeigeSpieler

                    if event.key == pygame.K_s:
                        self.zeigeStats = not self.zeigeStats

                    if event.key == pygame.K_i:
                        self.oikeymemory[1] = True

                elif event.type == pygame.MOUSEMOTION:
                    mausx, mausy = self.mauspos = event.pos
                    self.msg.append((MOUSETILE, getTile(self.getMapPos(self.mauspos))))
                    if mapverschieben:
                        self.posmap = abst(mouseMapCoord, self.mauspos)
                        self.mapzoomed = zuschneiden_image(self.mapPicture,
                                                           self.getMapPos((0, 0)) + mult((BARBREITE, HOEHE),
                                                                                         1 / self.zoomfaktor),
                                                           self.zoomfaktor)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        mouseMapCoord = abst(self.posmap, self.mauspos)
                        mapverschieben = True
                        click = True
                        i = 0
                        for it in TIERE:
                            if self.buttonsgame[i].checkCollision(self.mauspos):
                                if click:
                                    self.tiere.append(it)
                            i += 1
                        if self.buttonsgame[-1].checkCollision(self.mauspos):
                            if click:
                                self.inskilltree = not self.inskilltree
                    if event.button == pygame.BUTTON_RIGHT:
                        if self.inskilltree:
                            if self.skilltreePoints > 0:
                                mutpos = self.testsktr.unlock(self.mauspos)
                                if mutpos != None:
                                    self.skilltreePoints -= 1
                                    self.unlockMutation(mutpos)
                        else:
                            for creature in self.tiere:
                                self.spawn(creature, self.getMapPos(self.mauspos), 10)
                            self.tiere = []

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == pygame.BUTTON_LEFT:
                        mapverschieben = False
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_o:
                        self.oikeymemory[0] = False
                    if event.key == pygame.K_i:
                        self.oikeymemory[1] = False

    def menuanimieren(self):
        i = 100
        self.screen.blit(menubackground, (0, 0))
        for button in self.buttons:
            pygame.draw.rect(self.screen, (100, 100, 0), button)
        for label in self.txt:
            self.screen.blit(label, (int(BREITE // 20 + 30), int(HOEHE // 8 + i + 10)))
            i += 100
        pygame.display.flip()

    def ipmenuanimieren(self):
        self.screen.blit(menubackground, (0, 0))
        for button in self.ipMenuButtons:
            button.blitButton(self.screen)
        self.ipFeld.blitTextFeld(self.screen)
        pygame.display.flip()

    def singleplayermenuanimieren(self):
        self.screen.blit(menubackground, (0, 0))
        for button in self.lvlbutton_list:
            button.blitButton(self.screen)
        pygame.display.flip()

    def neuerZug(self):
        self.button_listzug = ZUGBUTTONS
        self.buttonszug = []
        self.txtzug = []
        self.stonetype = len(ZUGBUTTONS) * [0]
        self.steineOnTable = STEINEANZAHL
        self.kartenGespielt = 0
        self.objectOnMouse = None
        self.messages = []
        i = 0
        for label in self.button_listzug:
            button = pygame.sprite.Sprite()
            button.rect = pygame.rect.Rect(BREITE - BREITE // 10 + (-100 - 300 * i), HOEHE // 2 - 150,
                                           GROESSEBUTTONSNEUERZUG, GROESSEBUTTONSNEUERZUG)
            button.image = buttonzug
            self.buttonszug.append(button)
            text = FONT2.render(label, 1, WEISS)
            self.txtzug.append(text)
            i += 1
        endTurnButton = pygame.rect.Rect(BARBREITE + 30, HOEHE - 100, GROESSEBUTTONSGAME, GROESSEBUTTONSGAME // 5)
        endTurnLabel = FONT2.render("Zug beenden", 1, SCHWARZ)
        nextCardButton = pygame.rect.Rect(BARBREITE + 30, HOEHE - 150, GROESSEBUTTONSGAME, GROESSEBUTTONSGAME // 5)
        nextCardLabel = FONT2.render("nächste Karte", 1, SCHWARZ)

        self.mapzoomed = zuschneiden_image(self.mapPicture,
                                           self.getMapPos((0, 0)) + mult((BREITE, HOEHE), 1 / self.zoomfaktor),
                                           self.zoomfaktor)
        mapverschieben = False
        zugstart = True
        self.cardpick = False
        self.kartenspielen = False
        self.zugpause = True
        while self.zugpause:
            self.uhr.tick(FPSGAME)
            if not self.singleplayer:
                incMsg = self.theNetwork.send(self.msg)
                self.msg = [True]
                self.interpretServerMsg(incMsg)
            else:
                self.gameInfo = self.game.livingThings
            self.screen.fill((150, 150, 0))
            mapblitpos = [0, 0]
            for i in (0, 1):
                mapblitpos[i] = max(self.posmap[i], 0)
            self.screen.blit(self.mapzoomed, mapblitpos)
            self.gesTiere = 0
            self.objectOnMouse = None
            for obj in self.gameInfo:
                picStr = self.getDesc(obj)
                if self.isFlying(obj):
                    picStr += "FLG"
                img = self.workingImages[picStr]
                rect = img.get_rect()
                rect.center = self.getScreenPos(self.getPos(obj))
                if rect.colliderect((0, 0, BREITE, HOEHE)):
                    self.screen.blit(img, rect)
                    self.gesTiere += self.getAnzahl(obj)
                    if self.getPlayer(obj) != -1 and self.zeigeSpieler:
                        pygame.draw.circle(self.screen, FARBENSPIELER[self.getPlayer(obj)],
                                           rect.center, int(2 * self.zoomfaktor))
                if rect.collidepoint(self.mauspos):
                    self.objectOnMouse = obj

            self.screen.blit(buttons1, endTurnButton)
            self.screen.blit(endTurnLabel,
                             (endTurnButton.left + 20, endTurnButton.top))

            if zugstart:
                i = -100
                for button in self.buttonszug:
                    self.screen.blit(button.image, button.rect)
                    for j in range(self.stonetype[self.buttonszug.index(button)]):
                        self.screen.blit(greystone, (BREITE - BREITE // 10 + i + 30 * j, HOEHE // 2 - 150))
                    i -= 300
                i = -100
                for label in self.txtzug:
                    self.screen.blit(label, (BREITE - BREITE // 10 + i + 50, HOEHE // 2 - 50))
                    i -= 300
                self.screen.blit(greystone, (BREITE // 2, HOEHE * 3 // 4))
                text = FONT2BIG.render("%i X " % self.steineOnTable, 1, SCHWARZ)
                self.screen.blit(text, (BREITE // 2 - 100, HOEHE * 3 // 4 - 60))

            if self.cardpick:
                for karte in karten:
                    self.screen.blit(karte.image, karte.rect)
                    text = self.font2.render(karte.desc, 1, (0, 0, 0))
                    self.screen.blit(text, karte.rect.bottomleft)

            if self.kartenspielen:
                self.screen.blit(buttons1, nextCardButton)
                self.screen.blit(nextCardLabel,
                                 (nextCardButton.left + 20, nextCardButton.top))
                # AOE indicator
                if aktiveKarte.showAOE:
                    position = self.getScreenPos(tileCoords(self.getMouseTile()))
                    size = mult(aktiveKarte.aoe, 16 * self.zoomfaktor, True)
                    pygame.draw.rect(self.screen, (0, 0, 255),
                                     (position, size), 5)

            if self.oikeymemory[0] and self.zoomfaktor >= 0.5:
                self.zoom(ZOOM, False)
            if self.oikeymemory[1] and self.zoomfaktor <= 4:
                self.zoom(1 / ZOOM, False)
            for event in pygame.event.get():
                self.standardHandling(event)
                mx, my = pygame.mouse.get_pos()
                click = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_k:
                        self.killserver()
                    if event.key == pygame.K_o:
                        self.oikeymemory[0] = True

                    if event.key == pygame.K_c:  # Schalte Spieleranzeige an/aus
                        self.zeigeSpieler = not self.zeigeSpieler
                    if event.key == pygame.K_i:
                        self.oikeymemory[1] = True

                elif event.type == pygame.MOUSEMOTION:
                    mausx, mausy = self.mauspos = event.pos
                    if mapverschieben:
                        self.posmap = abst(mouseMapCoord, self.mauspos)
                        self.mapzoomed = zuschneiden_image(self.mapPicture,
                                                           self.getMapPos((0, 0)) + mult((BREITE, HOEHE),
                                                                                         1 / self.zoomfaktor),
                                                           self.zoomfaktor)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        mouseMapCoord = abst(self.posmap, self.mauspos)
                        mapverschieben = True
                        if endTurnButton.collidepoint(self.mauspos):
                            self.zugpause = False
                        if zugstart:
                            for it in self.buttonszug:
                                if it.rect.collidepoint(self.mauspos):
                                    if self.steineOnTable > 0:
                                        self.steineOnTable -= 1
                                        self.stonetype[self.buttonszug.index(it)] += 1
                                        if self.steineOnTable == 0:
                                            self.cardpick = True
                                            zugstart = False
                                            karten = handkarten(self.stonetype)
                                            i = 0
                                            for karte in karten:
                                                if karte != None:
                                                    if i < 3:
                                                        karte.rect = pygame.rect.Rect(
                                                            (BREITE // 8 + BREITE // 4 * i, HOEHE // 2 - 350),
                                                            GROESSECARD)
                                                    else:
                                                        karte.rect = pygame.rect.Rect(
                                                            (BREITE // 8 + BREITE // 4 * (i - 3), HOEHE // 2 + 50),
                                                            GROESSECARD)
                                                i += 1
                        if self.cardpick:
                            for karte in karten:
                                if karte.rect.collidepoint(self.mauspos):
                                    if karte.type == "Landtier" or karte.type == "Wassertier" or karte.type == "Flieger":
                                        self.tiere = []
                                        karte.spielen(self)
                                    elif karte.type == "Mutation":
                                        self.mutations_list = []
                                        self.mutierteTiere = []
                                        karte.spielen(self)
                                    karten.remove(karte)
                                    self.cardpick = False
                                    self.kartenspielen = True
                                    self.kartenGespielt += 1
                                    aktiveKarte = karte
                                    if karte.type == "Umwelt":
                                        if karte.targeting == "NONE":
                                            self.nextcard()
                                        elif karte.targeting == "TILE":
                                            self.targets = []
                                    elif karte.type == "Mutiere":
                                        self.mutated = 0

                        if self.kartenspielen:
                            if nextCardButton.collidepoint(self.mauspos):
                                self.nextcard()

                    if event.button == pygame.BUTTON_RIGHT:
                        if self.kartenspielen:
                            if aktiveKarte.type == "Landtier" or aktiveKarte.type == "Wassertier" or aktiveKarte.type == "Flieger":
                                creature = self.tiere.pop(0)
                                self.spawn(creature, self.getMapPos(self.mauspos))
                                if len(self.tiere) == 0:
                                    self.nextcard()
                            elif aktiveKarte.type == "Mutation":
                                if (self.objectOnMouse != None and
                                        self.getId(self.objectOnMouse) not in self.mutierteTiere):
                                    mut = self.mutations_list.pop(0)
                                    id = self.getId(self.objectOnMouse)
                                    self.addMutation(id, mut)
                                    self.mutierteTiere.append(id)
                                    if len(self.mutations_list) == 0:
                                        self.nextcard()
                            elif aktiveKarte.type == "Umwelt":
                                if aktiveKarte.targeting == "TILE":
                                    self.targets.append(self.getMouseTile())
                                    if len(self.targets) >= aktiveKarte.targetNbr:
                                        aktiveKarte.spielen(self, self.targets)
                                        self.nextcard()
                            elif aktiveKarte.type == "Mutiere":
                                if self.objectOnMouse != None:
                                    self.mutate(self.getId(self.objectOnMouse))
                                    self.mutated += 1
                                    if self.mutated >= aktiveKarte.targetNbr:
                                        self.nextcard()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == pygame.BUTTON_LEFT:
                        mapverschieben = False

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_o:
                        self.oikeymemory[0] = False
                    if event.key == pygame.K_i:
                        self.oikeymemory[1] = False
            pygame.display.flip()

    def animieren(self):
        self.screen.fill((150, 150, 0))
        mapblitpos = [0, 0]
        for i in (0, 1):
            mapblitpos[i] = max(self.posmap[i], 0)
        self.screen.blit(self.mapzoomed, mapblitpos)
        self.gesTiere = 0
        for obj in self.gameInfo:
            picStr = self.getDesc(obj)
            if self.isFlying(obj):
                picStr += "FLG"
            img = self.workingImages[picStr]
            rect = img.get_rect()
            rect.center = self.getScreenPos(self.getPos(obj))
            if rect.colliderect((0, 0, BARBREITE, HOEHE)):
                self.screen.blit(img, rect)
                self.gesTiere += self.getAnzahl(obj)
                if self.getPlayer(obj) != -1 and self.zeigeSpieler:
                    pygame.draw.circle(self.screen, FARBENSPIELER[self.getPlayer(obj)],
                                       rect.center, int(3 * self.zoomfaktor))
            if rect.collidepoint(self.mauspos):
                self.objectOnMouse = obj

        self.screen.blit(bar, (BARBREITE, 0))
        if self.zeigeStats:
            self.screen.blit(bar, (0, 0))
        if self.singleplayer:
            self.statusSinglePlayer()
        else:
            self.statusMultiPlayer()
        for button in self.buttonsgame:
            button.blitButton(self.screen)
        for message in self.messages:
            message.blitmessage(self.screen)
        if self.gameover:
            self.endgamescreen()
        pygame.display.flip()

    def animierenSkillTree(self):
        self.testsktr.blitSkilltree(self.screen, (0, 0))
        for button in self.buttonsgame:
            button.blitButton(self.screen)
        if self.gameover:
            self.endgamescreen()
        pygame.display.flip()

    def standardHandling(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif event.type == SONG_END:
            pygame.mixer.music.load(random.choice(music))
            pygame.mixer.music.play()

    def zoom(self, factor, bar=True):
        mouseMapCoord = mult(abst(self.posmap, self.mauspos), 1 / self.zoomfaktor)
        self.zoomfaktor *= factor
        self.posmap = mult(addieren(mult(mouseMapCoord, -self.zoomfaktor), self.mauspos), 1, True)
        breite = BARBREITE
        if not bar:
            breite = BREITE
        self.mapzoomed = zuschneiden_image(self.mapPicture,
                                           self.getMapPos((0, 0)) + mult((breite, HOEHE),
                                                                         1 / self.zoomfaktor, True), self.zoomfaktor)
        self.workingImages = {}
        for img in self.origImages:
            val = self.origImages[img]
            groesse = mult(val[2], self.zoomfaktor, True)
            self.workingImages[img] = pygame.transform.scale(val[0], groesse)

    def statusMultiPlayer(self):  # Gibt alle moegliche Zeugs aus
        a = 0
        for p in range(len(self.points)):
            text = self.font2.render("Spieler %i: %i" % (p, self.points[p])
                                     , 1, FARBENSPIELER[p])
            self.screen.blit(text, [BREITE - BREITE // 6 + 50, HOEHE // 2 + a])
            a += 30
        tileRN = getTile(self.getMapPos(self.mauspos))
        if 0 <= tileRN[0] < self.tilenbrx and 0 <= tileRN[1] < self.tilenbry:
            try:
                text = self.font2.render("Essen: %.1f" % self.plantFoodInTile, 1, (0, 0, 0))
            except:
                print(self.plantFoodInTile, "ist keine Zahl, tile:", tileRN)
            self.screen.blit(text, [100, 40])
        i = 50
        #Tierinfo
        for tier in self.objectInfoInTile:
            text = self.font2.render("%s, %i, %.1f, %.3f, %s" % (self.getDesc(tier), self.getAnzahl(tier),
                                                                 self.getHunger(tier), self.getFitness(tier),
                                                                 self.getMutations(tier)), 1, (20, 0, 0))
            self.screen.blit(text, [100 + 300 * int(self.zeigeStats), 40 + i])
            i += 50
        if self.zeigeStats:
            self.anzeige = {"Herden:": (len(self.gameInfo)),
                            "Tiere:": self.gesTiere}
            a = 50
            for stats in self.anzeige:
                text = self.font2.render(stats + "%i" % self.anzeige[stats], 1, (0, 0, 0))
                self.screen.blit(text, [30, a])
                a += 30

            playerAnimals = createListofLists(self.playerCount, len(TIERE))
            moeglicheTiere = list(TIERE.keys())
            playerPts = self.playerCount * [0]
            for tier in self.gameInfo:
                desc = self.getDesc(tier)
                plr = self.getPlayer(tier)
                pop = self.getAnzahl(tier)
                if self.getPlayer(tier) in range(self.playerCount):
                    playerAnimals[plr][moeglicheTiere.index(desc)] += pop
                    playerPts[plr] += (POINTS[desc] * pop)
            for player in range(self.playerCount):
                text = self.font2.render("Spieler %i: %i" % (player, playerPts[player]),
                                         1, FARBENSPIELER[player])
                self.screen.blit(text, [30, a])
                a += 30
                for tierNR in range(len(moeglicheTiere)):
                    anz = playerAnimals[player][tierNR]
                    if anz > 0:
                        zahl = playerAnimals[player][tierNR]
                        text = self.font2.render(moeglicheTiere[tierNR] + ": %i" % zahl,
                                                 1, FARBENSPIELER[player])
                        self.screen.blit(text, [30, a])
                        a += 30

    def statusSinglePlayer(self):
        a = 0
        a += 30
        tileRN = getTile(self.getMapPos(self.mauspos))
        if 0 <= tileRN[0] < self.tilenbrx and 0 <= tileRN[1] < self.tilenbry:
            try:
                text = self.font2.render("Essen: %.1f / %.1f / %.1f" \
                                         %(self.game.getPflanzenEssen(tileRN, 0),
                                          self.game.getPflanzenEssen(tileRN, 1),
                                           self.game.getPflanzenEssen(tileRN, 2)),
                                            True, (0, 0, 0))
            except:
                print(self.plantFoodInTile, "ist keine Zahl")
                fehler
            self.screen.blit(text, [100, 40])
        i = 50
        for tier in self.gameInfo:
            if tier.tile == tileRN:
                muts = [mut["Name"] for mut in self.getMutations(tier)]
                text = self.font2.render("%s, %i, %.1f, %.3f, %s" % (self.getDesc(tier), self.getAnzahl(tier),
                                                                     self.getHunger(tier), self.getFitness(tier),
                                                                     muts), 1, (20, 0, 0))
                self.screen.blit(text, [100 + 300 * int(self.zeigeStats), 40 + i])
                i += 50
        if self.zeigeStats:
            self.anzeige = {"Herden:": (len(self.gameInfo)),
                            "Tiere:": self.gesTiere}
            a = 50
            for stats in self.anzeige:
                text = self.font2.render(stats + "%i" % self.anzeige[stats], 1, (0, 0, 0))
                self.screen.blit(text, [30, a])
                a += 30

            playerAnimals = len(TIERE) * [0]
            moeglicheTiere = list(TIERE.keys())
            playerPts = 0
            for tier in self.gameInfo:
                desc = self.getDesc(tier)
                plr = self.getPlayer(tier)
                pop = self.getAnzahl(tier)
                playerAnimals[moeglicheTiere.index(desc)] += pop
                playerPts += (POINTS[desc] * pop)
            text = self.font2.render("Wert der Tiere: %i" % (playerPts),
                                     1, SCHWARZ)
            self.screen.blit(text, [30, a])
            a += 30
            for tierNR in range(len(moeglicheTiere)):
                anz = playerAnimals[tierNR]
                if anz > 0:
                    zahl = playerAnimals[tierNR]
                    text = self.font2.render(moeglicheTiere[tierNR] + ": %i" % zahl,
                                             1, (0, 0, 255))
                    self.screen.blit(text, [30, a])
                    a += 30

    def nextcard(self):
        self.kartenspielen = False
        if self.kartenGespielt >= ANZAHLKARTENSPIELEN:
            self.zugpause = False
        else:
            self.cardpick = True

    def endgamescreen(self):
        text = FONT2.render("Game over", 1, SCHWARZ)
        screen.blit(text, (400, 200))
        for player in range(self.playerCount):
            text = self.font2.render("Spieler %i: %i" % (player, self.points[player]), 1,
                                     FARBENSPIELER[player])
            screen.blit(text, (400, 300 + 100 * player))

    def getMapPos(self, pos):
        return mult(abst(self.posmap, pos), 1 / self.zoomfaktor)

    def getScreenPos(self, posOnMap):
        return addieren(mult(posOnMap, self.zoomfaktor, True), self.posmap)

    def getMouseTile(self):
        return getTile(self.getMapPos(self.mauspos))

    # Interpretiere die server messages
    def interpretServerMsg(self, incMsg):
        action, self.points, self.playerCount, self.gameInfo, \
                self.plantFoodInTile,self.objectInfoInTile, self.notifications = incMsg
        for n in self.notifications:
            print(n)
        if action == TURN and not self.zugpause:
            self.neuerZug()
        elif action == GAMEOVER:
            self.gameover = True

    def getDesc(self, tier):
        if self.singleplayer:
            return tier.desc
        return tier[0]

    def getPos(self, tier):
        if self.singleplayer:
            return tier.getPos()
        return tier[1]

    def getHunger(self, tier):
        if self.singleplayer:
            return tier.hunger
        return tier[6]

    def getAnzahl(self, tier):
        if self.singleplayer:
            return tier.popGroesse
        return tier[2]

    def getId(self, tier):
        if self.singleplayer:
            return tier.id
        return tier[3]

    def getPlayer(self, tier):
        if self.singleplayer:
            return tier.player
        return tier[4]

    def isFlying(self, tier):
        if self.singleplayer:
            return tier.imFlug
        return tier[5]

    def getFitness(self, tier):
        if self.singleplayer:
            return tier.getFitness()
        return tier[7]

    def getMutations(self, tier):
        if self.singleplayer:
           return tier.mutationen
        return tier[8]

    # Befehle an Server
    def spawn(self, tierDesc, pos, anzahl=1):
        if self.singleplayer:
            for i in range(anzahl):
                self.game.addCreature(TIERE[tierDesc], pos)
        else:
            self.msg.append((SPAWNTIER, tierDesc, pos, anzahl))

    def addMutation(self, tierId, mutation):
        if self.singleplayer:
            self.game.giveMutation(tierId, mutation)
        else:
            self.msg.append((GIVEMUTATION, tierId, mutation))

    def doevent(self, event, targets=None):
        if self.singleplayer:
            EVENTS[event](self.game, targets)
        self.msg.append((DOEVENT, event, targets))

    def mutate(self, animalId):
        if self.singleplayer:
            return
        self.msg.append((ADVANCE, animalId))

    def unlockMutation(self, posInTree):
        self.msg.append((UNLOCK, posInTree))

    def killserver(self):
        self.msg.append((KILLSERVER,))



if __name__ == "__main__":
    imges = prepareAnimalImages()
    prepareOtherImages()
    Execute(screen, imges)
