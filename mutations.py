# Mutationenstats
GETFASTBONUS = 0.2
FITNESSBOOSTBONUS = 0.2
EVASIONBOOSTBONUS = 1
PRECISIONBOOSTBONUS = 1
INTBOOSTBONUS = 1
INTBOOSTMULT = 1  # Das heisst mal 2

STATSZUMUTIEREN = ["SPEED", "FITNESS", "EVASION", "PRECISION", "INTFLAT", "INTMULT"]

# Mutationen
getFast = {"Name": "getFast", "Stats": {"SPEED": GETFASTBONUS}}
getFitness = {"Name": "getFitness", "Stats": {"FITNESS": FITNESSBOOSTBONUS}}
getEvasion = {"Name": "getEvasion", "Stats": {"EVASION": EVASIONBOOSTBONUS}}
getPrecision = {"Name": "getFitness", "Stats": {"PRECISION": PRECISIONBOOSTBONUS}}
getInt = {"Name": "getFitness", "Stats": {"INTFLAT": INTBOOSTBONUS, "INTMULT": INTBOOSTMULT}}
