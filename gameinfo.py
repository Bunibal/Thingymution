from gameclass import *
POINTS = {"Maus": 4, "Schnecke":1, "Krabbe": 1,
        "Doktorfisch": 1, "Falke": 9, "Käfer":1, "Fuchs": 10,
        "Kaninchen": 4, "Ziege": 20, "Singvogel": 3}
TIERE = {"Maus":Maus, "Schnecke":Schnecke, "Krabbe": Krabbe,
    "Doktorfisch": Doktorfisch, "Falke": Falke, "Singvogel": Singvogel,
    "Käfer":Kaefer, "Fuchs":Fuchs, "Kaninchen": Kaninchen,
    "Ziege": Ziege,}
EVENTS = {"Meteor": Game.meteorShower, "Coolwave": Game.coolWave,
        "Heatwave":Game.heatWave, "Granade": Game.granade}
ZUGBUTTONS =["Mutationen","Umwelt","Flieger","Landtiere","Wassertiere"]