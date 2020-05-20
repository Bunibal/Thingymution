from gameclass import *
from network import Network

# Zum laufen: py Pythonstuff\ThingyMutation\server.py
# Konstanten
FPSMENU = 60
GROESSE = BREITE, HOEHE = 1536, 825
BARBREITE = int(BREITE - BREITE / 6)
WEISS = (255, 255, 255)
SCHWARZ = (0, 0, 0)
TRANSPARENCY = (13, 66, 23)
FARBENSPIELER = [(0, 0, 255), (255, 0, 0),
                 (0, 255, 0), (0, 255, 255), (255, 255, 0), (255, 0, 255)]

pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)
screen = pygame.display.set_mode(GROESSE)
pygame.display.set_caption("Thingymution")

SONG_END = pygame.USEREVENT + 1

HANDKARTEN = 6
STONEGEWICHTUNG = 4
STEINEANZAHL = 5
ZOOM = 0.9
ANZAHLKARTENSPIELEN = 3
# menu
GROESSEBUTTONS = 300
# Game
GROESSEBUTTONSGAME = 200
GROESSEBUTTONSNEUERZUG = 200
GROESSECARD = (200, 300)

BUTTONS = ["Singleplayer", "Multiplayer", "Options", "Exit Game"]
LVLS = ["Tutorial", "Sandbox", "Level 1", "Level 2"]
# Karten
MUTATIONEN = 0
UMWELT = 1
LANDTIERE = 3
WASSERTIERE = 4
FLIEGER = 2
# Kommunikation mit Server
SPAWNTIER = 0
GIVEMUTATION = 1
DOEVENT = 2
MOUSETILE = 3
KILLSERVER = 322
# Bildgroessen
BILDGROESSESCHNECKE = (16, 8)
BILDGROESSEMAUS = (16, 16)
BILDGROESSEKRABBE = (16, 8)
BILDGROESSEFALKE = (16, 16)
BILDGROESSEKAEFER = (16, 8)
BILDGROESSEDOKTORFISCH = (16, 8)
BILDGROESSEFUCHS = (16, 16)
BILDGROESSEKANINCHEN = (14, 14)
BILDGROESSEZIEGE = (20, 20)
BILDGROESSESINGVOGEL = (16, 16)
# music and backgrounds

menubackground = pygame.image.load("menubackground.png").convert()
menubackground = pygame.transform.scale(menubackground, GROESSE)

music = ["1 Great pyramids.mp3", "2 Face to face.mp3", "3 Life in forest.mp3", "1.mp3",
         "2.mp3", "4.mp3", "6.mp3", "8.mp3", "11.mp3", "13.mp3", "15.mp3", "18.mp3"]

# Hier laden wir ma alle Bilder rein
mapPicture0 = pygame.image.load("maplvl1.png").convert()
kleinereMap = pygame.image.load("maplvl2.png").convert()
MAPPICTURES = [mapPicture0, kleinereMap]
schneckeImage = pygame.image.load("slug.png").convert_alpha()
mausImage = pygame.image.load("mouse.png").convert_alpha()
krabbeImage = pygame.image.load("crab.png")
krabbeImage.set_colorkey(TRANSPARENCY)
krabbeImage = krabbeImage.convert_alpha()
falkeImage = pygame.image.load("falcon.png").convert_alpha()
falkeFliegendImage = pygame.image.load("falconflying.png").convert_alpha()
kaeferImage = pygame.image.load("bug.png")
kaeferImage.set_colorkey(TRANSPARENCY)
kaeferImage = kaeferImage.convert_alpha()
doktorfischimage = pygame.image.load("doctorfish.png").convert_alpha()
eelimage = pygame.image.load("eel.png").convert_alpha()
fuchsImage = pygame.image.load("fox.png").convert_alpha()
kaninchenImage = pygame.image.load("rabbit.png").convert_alpha()
ziegeImage = pygame.image.load("goat.png").convert_alpha()
singvogelImage = pygame.image.load("singvogel.png").convert_alpha()
singvogelFliegendImage = pygame.image.load("singvogelflying.png").convert_alpha()
buttons1 = pygame.transform.scale(pygame.image.load("buttons1.png").convert(),
                                  (GROESSEBUTTONSGAME, GROESSEBUTTONSGAME // 5))
bar = pygame.transform.scale(pygame.image.load("bar.png").convert(), (BREITE // 6, HOEHE))

# hier GUI
buttonzug = pygame.transform.scale(pygame.image.load("zugbutton.png").convert(),
                                   (GROESSEBUTTONSNEUERZUG, GROESSEBUTTONSNEUERZUG))
greystone = pygame.transform.scale(pygame.image.load("Magic_button_grey.png").convert(), (50, 50))

# Karten zuerst die Tiere
carddefault = pygame.transform.scale(pygame.image.load("carddefault.png").convert(), GROESSECARD)
cardfalcon = pygame.transform.scale(pygame.image.load("cardfalcon.png").convert(), GROESSECARD)
cardslug = pygame.transform.scale(pygame.image.load("cardslug.png").convert(), GROESSECARD)
cardmouse = pygame.transform.scale(pygame.image.load("cardmouse.png").convert(), GROESSECARD)
cardbug = pygame.transform.scale(pygame.image.load("cardbug.png").convert(), GROESSECARD)
carddoctorfish = pygame.transform.scale(pygame.image.load("carddoctorfish.png").convert(), GROESSECARD)
cardcrab = pygame.transform.scale(pygame.image.load("cardcrab.png").convert(), GROESSECARD)
cardeel = pygame.transform.scale(pygame.image.load("cardeel.png").convert(), GROESSECARD)
# jetzt kommen die MUTATIONEN
cardgetfast = pygame.transform.scale(pygame.image.load("cardgetfast.png").convert(), GROESSECARD)
cardfitnessboost = pygame.transform.scale(pygame.image.load("cardfitnessboost.png").convert(), GROESSECARD)
cardpowerboost = pygame.transform.scale(pygame.image.load("cardpowerboost.png").convert(), GROESSECARD)
cardintboost = pygame.transform.scale(pygame.image.load("cardgetintelligent.png").convert(), GROESSECARD)
cardgetflying = pygame.transform.scale(pygame.image.load("cardgetflying.png").convert(), GROESSECARD)
# jetzt die Umweltkarten
cardmeteorshower = pygame.transform.scale(pygame.image.load("cardmeteor.png").convert(), GROESSECARD)
if not SZABTEST:
    pass
else:
    # krabbeImage = pygame.image.load("mouse.png").convert()
    pass

#### images to description
IMAGES = {"Maus": (mausImage, None, BILDGROESSEMAUS),
          "Schnecke": (schneckeImage, None, BILDGROESSESCHNECKE),
          "Krabbe": (krabbeImage, None, BILDGROESSEKRABBE),
          "Doktorfisch": (doktorfischimage, None, BILDGROESSEDOKTORFISCH),
          "Falke": (falkeImage, None, BILDGROESSEFALKE),
          "FalkeFLG": (falkeFliegendImage, None, BILDGROESSEFALKE),
          "Singvogel": (singvogelImage, None, BILDGROESSESINGVOGEL),
          "SingvogelFLG": (singvogelFliegendImage, None, BILDGROESSESINGVOGEL),
          "Käfer": (kaeferImage, None, BILDGROESSEKAEFER),
          "Fuchs": (fuchsImage, None, BILDGROESSEFUCHS),
          "Kaninchen": (kaninchenImage, None, BILDGROESSEKANINCHEN),
          "Ziege": (ziegeImage, None, BILDGROESSEZIEGE)}
# Schriftarten
FONT1 = pygame.font.SysFont("chiller", 50)
FONT2 = pygame.font.SysFont("Times", 30)


def zuschneiden_image(image, rectInfo, scale=1):
    rect = pygame.rect.Rect(rectInfo)
    newImage = pygame.transform.chop(image, (rect.right, rect.bottom, 10000, 10000))  # spaghetti
    newImage = pygame.transform.chop(newImage, (0, 0, rect.left, rect.top))
    size = newImage.get_rect().size
    newImage = pygame.transform.scale(newImage, mult(size, scale, True))
    return newImage


# Karten############################################################################################################################

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


class ButtonNormal:
    def __init__(self, pos, label):
        self.font = FONT1
        self.pos, self.label = pos, label
        self.rect = pygame.rect.Rect(self.pos, (GROESSEBUTTONS, GROESSEBUTTONS // 5))
        self.text = self.font.render(self.label, 1, SCHWARZ)

    def blitButton(self, screen):
        pygame.draw.rect(screen, (100, 100, 0), self.rect)
        screen.blit(self.text, (self.pos[0] + 20, self.pos[1] + 20))

    def checkCollision(self, pos):
        return self.rect.collidepoint(pos)


class ButtonGame(ButtonNormal):
    def __init__(self, pos, label):
        ButtonNormal.__init__(self, pos, label)
        self.rect = pygame.rect.Rect(self.pos, (GROESSEBUTTONSGAME, GROESSEBUTTONSGAME // 5))

    def blitButton(self, screen):
        screen.blit(buttons1, self.rect)
        screen.blit(self.text, (self.pos[0] + 20, self.pos[1] + 20))


class TextFeld:
    def __init__(self, pos, initText, font, laenge=400):
        self.pos = pos
        self.font = font
        self.text = initText
        self.rendered = font.render(self.text, 1, WEISS)
        self.laenge = 400

    def blitTextFeld(self, screen):
        pygame.draw.rect(screen, SCHWARZ,
                         (self.pos, (self.laenge, 60)))
        screen.blit(self.rendered, self.pos)

    def keystroke(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        else:
            self.text = self.text + event.unicode
        self.rendered = self.font.render(self.text, 1, WEISS)

    def backspace(self):
        self.text


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


# Klasse die alles ausfuehrt###############################################################
class Execute:
    def __init__(self, images):
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
        file = open("lastip.txt", "r")
        lastIp = file.read()
        file.close()
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
        mausx, mauxy = self.mauspos = (0, 0)
        mapverschieben = False
        self.oikeymemory = [False, False]
        self.button_list = TIERE
        self.buttonsgame = []
        self.txtgame = []
        self.tiere = []
        i = 40
        self.font2 = pygame.font.SysFont("Times", 30)
        self.zoomfaktor = 1
        self.mapzoomed = zuschneiden_image(self.mapPicture,
                                           self.getMapPos((0, 0)) + mult((BARBREITE, HOEHE), 1, True))
        for label in self.button_list:
            button = pygame.sprite.Sprite()
            button.rect = pygame.rect.Rect(BARBREITE + 30, i,
                                           GROESSEBUTTONSGAME, GROESSEBUTTONSGAME // 5)
            button.image = buttons1
            i += 50
            self.buttonsgame.append(button)
            text = self.font2.render(label, 1, SCHWARZ)
            self.txtgame.append(text)
            self.framescounterzug = 0
            self.msg = [False]
        # self.interpretServerMsg(incMsg)

        while self.inGame:
            self.uhr.tick(FPSGAME)
            if not self.singleplayer:
                incMsg = self.theNetwork.send(self.msg)
                self.msg = [False]
                self.interpretServerMsg(incMsg)
            else:
                self.gameInfo = self.game.livingThings
            self.animieren()

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

                    ##if event.key == pygame.K_z:
                    ##    self.neuerZug()

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
                            if self.buttonsgame[i].rect.collidepoint(self.mauspos):
                                if click:
                                    self.tiere.append(it)
                            i += 1
                    if event.button == pygame.BUTTON_RIGHT:
                        for creature in self.tiere:
                            self.spawn(creature, self.getMapPos(self.mauspos), 10)
                        self.tiere = []

                    ##if event.button == pygame.BUTTON_RIGHT:
                    ##print(self.getTerrain(self.mauspos))

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
        i = 0
        self.font2 = pygame.font.SysFont("Times", 30)
        self.bigfont = pygame.font.SysFont("Times", 70)
        for label in self.button_listzug:
            button = pygame.sprite.Sprite()
            button.rect = pygame.rect.Rect(BREITE - BREITE // 10 + (-100 - 300 * i), HOEHE // 2 - 150,
                                           GROESSEBUTTONSNEUERZUG, GROESSEBUTTONSNEUERZUG)
            button.image = buttonzug
            self.buttonszug.append(button)
            text = self.font2.render(label, 1, WEISS)
            self.txtzug.append(text)
            i += 1
        endTurnButton = pygame.rect.Rect(BARBREITE + 30, HOEHE - 100, GROESSEBUTTONSGAME, GROESSEBUTTONSGAME // 5)
        endTurnLabel = self.font2.render("Zug beenden", 1, SCHWARZ)
        nextCardButton = pygame.rect.Rect(BARBREITE + 30, HOEHE - 150, GROESSEBUTTONSGAME, GROESSEBUTTONSGAME // 5)
        nextCardLabel = self.font2.render("nächste Karte", 1, SCHWARZ)

        self.mapzoomed = zuschneiden_image(self.mapPicture,
                                           self.getMapPos((0, 0)) + mult((BREITE, HOEHE), 1 / self.zoomfaktor),
                                           self.zoomfaktor)
        mapverschieben = False
        zugstart = True
        cardpick = False
        kartenspielen = False
        self.zugpause = True
        # WHILESCHLEIFEBOIZZZZZZZZ
        while self.zugpause:
            self.uhr.tick(FPSGAME)
            if not self.singleplayer:
                incMsg = self.theNetwork.send(self.msg)
                self.msg = [True]
                self.interpretServerMsg(incMsg)
            else:
                self.game.step()
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
                text = self.bigfont.render("%i X " % self.steineOnTable, 1, SCHWARZ)
                self.screen.blit(text, (BREITE // 2 - 100, HOEHE * 3 // 4 - 60))

            if cardpick:
                for karte in karten:
                    self.screen.blit(karte.image, karte.rect)
                    text = self.font2.render(karte.desc, 1, (0, 0, 0))
                    self.screen.blit(text, karte.rect.bottomleft)

            if kartenspielen:
                self.screen.blit(buttons1, nextCardButton)
                self.screen.blit(nextCardLabel,
                                 (nextCardButton.left + 20, nextCardButton.top))
            if self.oikeymemory[0] and self.zoomfaktor >= 0.5:
                self.zoom(ZOOM, False)
            if self.oikeymemory[1] and self.zoomfaktor <= 4:
                self.zoom(1 / ZOOM, False)
            ##for obj in self.livingThings:
            ##      obj.bildanpassen(self.zoomfaktor)
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
                                            cardpick = True
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
                        if cardpick:
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
                                    cardpick = False
                                    kartenspielen = True
                                    self.kartenGespielt += 1
                                    aktiveKarte = karte
                                    if karte.type == "Umwelt":
                                        self.eventKarteSpielen(karte)
                                        if karte.targeting == "NONE":
                                            kartenspielen = False
                                            if self.kartenGespielt >= ANZAHLKARTENSPIELEN:
                                                self.zugpause = False
                                            else:
                                                cardpick = True
                                        elif karte.targeting == "TILE":
                                            self.targets = []

                        if kartenspielen:
                            if nextCardButton.collidepoint(self.mauspos):
                                kartenspielen = False
                                if self.kartenGespielt >= ANZAHLKARTENSPIELEN:
                                    self.zugpause = False
                                else:
                                    cardpick = True

                    if event.button == pygame.BUTTON_RIGHT:
                        if kartenspielen:
                            if aktiveKarte.type == "Landtier" or aktiveKarte.type == "Wassertier" or aktiveKarte.type == "Flieger":
                                creature = self.tiere.pop(0)
                                self.spawn(creature, self.getMapPos(self.mauspos))
                                if len(self.tiere) == 0:
                                    kartenspielen = False
                                    if self.kartenGespielt >= ANZAHLKARTENSPIELEN:
                                        self.zugpause = False
                                    else:
                                        cardpick = True
                            elif aktiveKarte.type == "Mutation":
                                if (self.objectOnMouse != None and
                                        self.getId(self.objectOnMouse) not in self.mutierteTiere):
                                    mut = self.mutations_list.pop(0)
                                    id = self.getId(self.objectOnMouse)
                                    self.addMutation(id, mut)
                                    self.mutierteTiere.append(id)
                                    if len(self.mutations_list) == 0:
                                        kartenspielen = False
                                        if self.kartenGespielt >= ANZAHLKARTENSPIELEN:
                                            self.zugpause = False
                                        else:
                                            cardpick = True
                            elif aktiveKarte.type == "Umwelt":
                                if aktiveKarte.targeting == "TILE":
                                    self.targets.append(self.getMouseTile())
                                    if len(self.targets) >= aktiveKarte.targetNbr:
                                        aktiveKarte.spielen(self, self.targets)
                                        kartenspielen = False
                                        if self.kartenGespielt >= ANZAHLKARTENSPIELEN:
                                            self.zugpause = False
                                        else:
                                            cardpick = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == pygame.BUTTON_LEFT:
                        mapverschieben = False

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_o:
                        self.oikeymemory[0] = False
                    if event.key == pygame.K_i:
                        self.oikeymemory[1] = False
            pygame.display.flip()

    def eventKarteSpielen(self, karte):
        pass

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
        self.screen.blit(bar, (BARBREITE, 0))
        if self.zeigeStats:
            self.screen.blit(bar, (0, 0))
        for button in self.buttonsgame:
            self.screen.blit(button.image, button.rect)
        i = 40
        for label in self.txtgame:
            self.screen.blit(label, (int(BARBREITE + 50), i))
            i += 50
        if self.singleplayer:
            self.statusSinglePlayer()
        else:
            self.statusMultiPlayer()
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
        for tier in self.objectInfoInTile:
            text = self.font2.render("%s, %i, %.1f, %.3f, %s" % (self.getDesc(tier), self.getAnzahl(tier),
                                                                 self.getHunger(tier), self.getFitness(tier),
                                                                 ", ".join(self.getMutations(tier))), 1, (20, 0, 0))
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
        ##text = self.font2.render("Spieler %i: %i"%(p,self.points[p])
        ##                    ,1,FARBENSPIELER[p])
        ##self.screen.blit(text, [BREITE - BREITE//6 + 50, HOEHE//2+a])
        a += 30
        tileRN = getTile(self.getMapPos(self.mauspos))
        if 0 <= tileRN[0] < self.tilenbrx and 0 <= tileRN[1] < self.tilenbry:
            try:
                text = self.font2.render("Essen: %.1f" % self.game.getPflanzenEssen(tileRN), 1, (0, 0, 0))
            except:
                print(self.plantFoodInTile, "ist keine Zahl")
                fehler
            self.screen.blit(text, [100, 40])
        i = 50
        for tier in self.gameInfo:
            if tier.tile == tileRN:
                text = self.font2.render("%s, %i, %.1f, %.3f, %s" % (self.getDesc(tier), self.getAnzahl(tier),
                                                                     self.getHunger(tier), self.getFitness(tier),
                                                                     ", ".join(self.getMutations(tier))), 1, (20, 0, 0))
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
                                             1, FARBENSPIELER[player])
                    self.screen.blit(text, [30, a])
                    a += 30

    def getMapPos(self, pos):
        return mult(abst(self.posmap, pos), 1 / self.zoomfaktor)

    def getScreenPos(self, posOnMap):
        return addieren(mult(posOnMap, self.zoomfaktor, True), self.posmap)

    def getMouseTile(self):
        return getTile(self.getMapPos(self.mauspos))

    # Interpretiere die server messages
    def interpretServerMsg(self, incMsg):
        if incMsg is not None:
            try:
                forcePausing = incMsg[0]
                self.points = incMsg[1][0]
                self.playerCount = incMsg[1][1]
                self.gameInfo = incMsg[2]
                self.plantFoodInTile = incMsg[3][0]
                self.objectInfoInTile = incMsg[3][1:]
            except:
                print(incMsg, "does not have the right format.")

            if forcePausing and not self.zugpause:
                self.neuerZug()
        else:
            print("Empfangene Information fehlerhaft")

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
        self.msg.append((SPAWNTIER, tierDesc, pos, anzahl))

    def addMutation(self, tierId, mutation):
        self.msg.append((GIVEMUTATION, tierId, mutation))

    def doevent(self, event, targets=None):
        self.msg.append((DOEVENT, event, targets))

    def killserver(self):
        self.msg.append((KILLSERVER,))


KARTEN_VORHANDEN = {MUTATIONEN: [Getfast, Fitnessboost, EvasionBoost, PrecisionBoost, IntBoost],
                    UMWELT: [Meteorshower, Heatwave, Coolwave, Granade],
                    LANDTIERE: [Spawnslug, Spawnmouse, Spawnbug, Spawnfox, Spawnrabbit, Spawngoat],
                    WASSERTIERE: [Spawndoctorfish, Spawncrab], FLIEGER: [Spawnfalcon, Spawnbird]}

Execute(IMAGES)
