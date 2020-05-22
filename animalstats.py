# statsslug

        SCHNECKEV = 2.5
        SCHNECKEESSEN =  0.05 #Essen pro Tier und Sekunde
        SCHNECKEHUNGERRES = 2
        HUNGERSCHNECKE = 0.009
        FITNESS_SCHNECKE = 1.018 # ~ Chance eines Tiers sich zu teilen pro Sekunde
        SCHNECKEDECINTERVAL = 2
        TEILPOPGROESSESCHNECKE = 50
        SCHNECKEGROESSE = 1
        ANGRIFFSLISTESCHNECKE = []
        SCHNECKETEMP, SCHNECKETEMPRANGE = 25,20
        SCHNECKEEVASION = -4
        SCHNECKEPREC = -5
        # statsmouse

        MAUSV = 8
        MAUSESSEN = 0.5 #Essen pro Tier und Sekunde
        MAUSHUNGERRES = 1.2
        HUNGERMAUS = 0.09
        FITNESS_MAUS = 1.012 # ~ Chance einer Schnecke sich zu teilen pro Sekunde
        MAUSDECINTERVAL = 3
        TEILPOPGROESSEMAUS = 30
        MAUSGROESSE = 3
        ANGRIFFSLISTEMAUS = ["Schnecke", "Käfer"]
        MAUSTEMP, MAUSTEMPRANGE = 20,20
        MAUSINTELLIGENZ = 2
        MAUSSTAERKE = 1
        MAUSEVASION = 0
        MAUSPREC = 0
        #statskrabbe

        KRABBEV = 2
        KRABBEESSEN = 0.15 #Essen pro Tier und Sekunde
        KRABBEHUNGERRES = 3
        HUNGERKRABBE = 0.0045
        FITNESS_KRABBE = 1.016 # ~ Chance einer Schnecke sich zu teilen pro Sekunde
        KRABBEDECINTERVAL = 10
        TEILPOPGROESSEKRABBE = 40
        KRABBEGROESSE = 1.5
        ANGRIFFSLISTEKRABBE = ["Schnecke"]
        KRABBETEMP, KRABBETEMPRANGE = 10, 20
        KRABBEINTELLIGENZ = 1
        KRABBEEVASION = -2
        KRABBEPREC = -2
        #Falkestats

        FALKEVGEHEND = 5
        FALKEVFLIEGEND = 30
        FALKEESSEN = 1 #Essen pro Tier und Sekunde
        FALKEHUNGERRES = 0.7
        HUNGERFALKEGEHEND = 0.05
        HUNGERFALKEFLIEGEND = 0.09
        FITNESS_FALKE = 1.01 # ~ Chance einer Schnecke sich zu teilen pro Sekunde
        FALKEDECINTERVAL = 3
        TEILPOPGROESSEFALKE = 15
        FALKEGROESSE = 4
        ANGRIFFSLISTEFALKE = ["Maus", "Käfer", "Singvogel"]
        FALKETEMP, FALKETEMPRANGE = 15,20
        FALKEINTELLIGENZ = 2
        FALKESTAERKE = 5
        FALKEEVASION = 2
        FALKEPREC = 3
        #SINGVOGELstats

        SINGVOGELVGEHEND = 5
        SINGVOGELVFLIEGEND = 25
        SINGVOGELESSEN = 1.5 #Essen pro Tier und Sekunde
        SINGVOGELHUNGERRES = 1.2
        HUNGERSINGVOGELGEHEND = 0.04
        HUNGERSINGVOGELFLIEGEND = 0.06
        FITNESS_SINGVOGEL = 1.013 # ~ Chance einer Schnecke sich zu teilen pro Sekunde
        SINGVOGELDECINTERVAL = 4
        TEILPOPGROESSESINGVOGEL = 20
        SINGVOGELGROESSE = 5
        ANGRIFFSLISTESINGVOGEL = ["Schnecke", "Käfer"]
        SINGVOGELTEMP, SINGVOGELTEMPRANGE = 25,15
        SINGVOGELINTELLIGENZ = 2
        SINGVOGELSTAERKE = 2
        SINGVOGELEVASION = 1
        SINGVOGELPREC = 2
        #statskaefer

        KAEFERV = 4
        KAEFERESSEN = 0.05 #Essen pro Schnecke und Sekunde
        KAEFERHUNGERRES = 1.0
        HUNGERKAEFER = 0.018
        FITNESS_KAEFER = 1.023 # ~ Chance einer Schnecke sich zu teilen pro Sekunde
        KAEFERDECINTERVAL = 3
        TEILPOPGROESSEKAEFER = 60
        KAEFERGROESSE = 0.6
        ANGRIFFSLISTEKAEFER = []
        KAEFERTEMP, KAEFERTEMPRANGE = 20,30
        KAEFEREVASION = -3
        KAEFERPREC = -2

        #statsdoktorfisch

        DOKTORFISCHV = 5
        DOKTORFISCHESSEN = 0.1 #Essen pro Schnecke und Sekunde
        DOKTORFISCHHUNGERRES = 1.5
        HUNGERDOKTORFISCH = 0.006
        FITNESS_DOKTORFISCH = 1.018 # ~ Chance einer Schnecke sich zu teilen pro Sekunde
        DOKTORFISCHDECINTERVAL = 5
        TEILPOPGROESSEDOKTORFISCH = 60
        DOKTORFISCHGROESSE = 1
        ANGRIFFSLISTEDOKTORFISCH = []
        DOKTORFISCHTEMP, DOKTORFISCHTEMPRANGE = 7,20
        DOKTORFISCHINTELLIGENZ = 1
        DOKTORFISCHEVASION = -1
        DOKTORFISCHPREC = -3
        # statsFUCHS
        FUCHSV = 15
        FUCHSVHUNT = 40
        FUCHSESSEN = 2 #Essen pro Tier und Sekunde
        FUCHSHUNGERRES = 1.4
        HUNGERFUCHS = 0.1
        FITNESS_FUCHS = 1.007 # ~ Chance eines Tiers sich zu teilen pro Sekunde
        FUCHSDECINTERVAL = 3
        TEILPOPGROESSEFUCHS = 15
        FUCHSGROESSE = 10
        ANGRIFFSLISTEFUCHS = ["Maus", "Kaninchen"]
        FUCHSTEMP, FUCHSTEMPRANGE = 15,23
        FUCHSINTELLIGENZ = 2
        FUCHSEVASION = 1
        FUCHSPREC = 2

        # statskaninchen
        KANINCHENV = 15
        KANINCHENESSEN = 0.3 #Essen pro Schnecke und Sekunde
        KANINCHENHUNGERRES = 1.0
        HUNGERKANINCHEN = 0.08
        FITNESS_KANINCHEN = 1.011 # Chance sich zu teilen pro Sekunde
        KANINCHENDECINTERVAL = 3
        TEILPOPGROESSEKANINCHEN = 25
        KANINCHENGROESSE = 5
        ANGRIFFSLISTEKANINCHEN = []
        KANINCHENTEMP, KANINCHENTEMPRANGE = 20,20
        KANINCHENINTELLIGENZ = 2
        KANINCHENEVASION = 1
        KANINCHENPREC = -2

        # statsziege
        ZIEGEV = 20
        ZIEGEESSEN = 0.3 #Essen pro Tier und Sekunde
        ZIEGEHUNGERRES = 2
        HUNGERZIEGE = 0.15
        FITNESS_ZIEGE = 1.006 # ~ Chance eines Tiers sich zu teilen pro Sekunde
        ZIEGEDECINTERVAL = 3
        TEILPOPGROESSEZIEGE = 10
        ZIEGEGROESSE = 5
        ANGRIFFSLISTEZIEGE = []
        ZIEGETEMP, ZIEGETEMPRANGE = 0,10
        ZIEGEINTELLIGENZ = 3
        ZIEGEEVASION = 1