from graphicalconstants import *
import tkinter as tk
import pygame
import os
import pytmx



def loadandscale(file, scale):
    return pygame.transform.scale(pygame.image.load(file).convert(), scale)


root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

GROESSE = BREITE, HOEHE = screen_width, screen_height
TRANSPARENCY = (13, 66, 23)

pygame.init()
origPath = os.getcwd()
os.chdir(origPath + "/resources")
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)
screen = pygame.display.set_mode(GROESSE)
pygame.display.set_caption("Thingymution")

# mapfiles
mapFile0 = pytmx.TiledMap("maplvl1.tmx")
mapFileKleiner = pytmx.TiledMap("maplvl2.tmx")
MAPFILES = [(mapFile0, (200, 200)), (mapFileKleiner, (60, 60))]

# music and backgrounds

menubackground = pygame.image.load("menubackground.png").convert()
menubackground = pygame.transform.scale(menubackground, GROESSE)

music = ["1 Great pyramids.mp3", "2 Face to face.mp3", "3 Life in forest.mp3", "1.mp3",
         "2.mp3", "4.mp3", "6.mp3", "8.mp3", "11.mp3", "13.mp3", "15.mp3", "18.mp3"]

# Hier laden wir ma alle Bilder rein
MAPPICTURES = [pygame.image.load("maplvl1.png").convert(), pygame.image.load("maplvl2.png").convert()]

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
umweltimage = loadandscale("umweltmessage.png", GROESSEMESSAGES)
warningmessage = loadandscale("warningmessage.png", GROESSEMESSAGES)
# images to description
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

MESSAGEIMAGES = {"Umwelt": umweltimage, "warning": warningmessage}

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


