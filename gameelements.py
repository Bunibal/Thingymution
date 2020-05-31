from cards import *
from gameclass import *


BUTTONS = ["Singleplayer", "Multiplayer", "Options", "Exit Game"]
LVLS = ["Tutorial", "Sandbox", "Level 1", "Level 2", "Menu"]

POINTS = {"Maus": 4, "Schnecke": 1, "Krabbe": 1,
          "Doktorfisch": 1, "Falke": 9, "Käfer": 1, "Fuchs": 10,
          "Kaninchen": 4, "Ziege": 20, "Singvogel": 3}
TIERE = {"Maus": Maus, "Schnecke": Schnecke, "Krabbe": Krabbe,
         "Doktorfisch": Doktorfisch, "Falke": Falke, "Singvogel": Singvogel,
         "Käfer": Kaefer, "Fuchs": Fuchs, "Kaninchen": Kaninchen,
         "Ziege": Ziege}
EVENTS = {"Meteor": Game.meteorShower, "Coolwave": Game.coolWave,
          "Heatwave": Game.heatWave, "Granade": Game.granade}
ZUGBUTTONS = ["Mutationen", "Umwelt", "Flieger", "Landtiere", "Wassertiere"]
KARTEN_VORHANDEN = {MUTATIONEN: [Getfast, Fitnessboost, EvasionBoost, PrecisionBoost, IntBoost],
                    UMWELT: [Meteorshower, Heatwave, Coolwave, Granade],
                    LANDTIERE: [Spawnslug, Spawnmouse, Spawnbug, Spawnfox, Spawnrabbit, Spawngoat],
                    WASSERTIERE: [Spawndoctorfish, Spawncrab], FLIEGER: [Spawnfalcon, Spawnbird]}
