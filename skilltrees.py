from graphicalconstants import *
from mutations import *
skilltreeslug = [[{"Mutation": getFitness}, {"Mutation": getEvasion}],
                 [{"Mutation": getFast, "Parent": 1}, {"Mutation": getInt, "Parent": 1}]]
POSTIER4 = HOEHE // 6
POSTIER0 = POSTIER4 * 5
POSTIER1 = POSTIER4 * 4
POSTIER2 = POSTIER4 * 3
POSTIER3 = POSTIER4 * 2
POSTIER = [POSTIER0, POSTIER1, POSTIER2, POSTIER3, POSTIER4]

