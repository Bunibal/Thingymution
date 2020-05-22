import os
from globalconstants import *

GROESSE = BREITE, HOEHE = 1536, 825
TRANSPARENCY = (13, 66, 23)

pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)
screen = pygame.display.set_mode(GROESSE)
pygame.display.set_caption("Thingymution")

# Schriftarten
FONT1 = pygame.font.SysFont("chiller", 50)
FONT2 = pygame.font.SysFont("Times", 30)

# Bildgroessen
origPath = os.getcwd()
os.chdir(origPath + "/resources")
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

os.chdir(origPath)