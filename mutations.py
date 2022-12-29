# Mutationenstats
GETFASTBONUS = 0.2
FITNESSBOOSTBONUS = 0.2
EVASIONBOOSTBONUS = 1
PRECISIONBOOSTBONUS = 1
INTBOOSTBONUS = 1
INTBOOSTMULT = 1  # Das heisst mal 2

# Mutationen
getFast = {"Name": "getFast", "Stats": {"Speed": GETFASTBONUS}}
getFitness = {"Name": "getFitness", "Stats": {"Fitness": FITNESSBOOSTBONUS}}
getEvasion = {"Name": "getEvasion", "Stats": {"Evasion": EVASIONBOOSTBONUS}}
getPrecision = {"Name": "getPrecision", "Stats": {"Precision": PRECISIONBOOSTBONUS}}
getInt = {"Name": "getIntelligence", "Stats": {"IntFLAT": INTBOOSTBONUS, "Int": INTBOOSTMULT}}
