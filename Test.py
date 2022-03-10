from script_test import Interruption
"""
Projet annuel M1 GPhy 2021/2022

Script de tests unitaires

@author: arthur
"""

#Import de la classe Interruption contenue dans "script_test.py"
from script_test import Interruption

##----------------MODULES IMPORTES-----------------##

import sys
import unittest
import pandas as pd
import re
import json

#Permet de récupérer code du script "script_test.py"
sys.path.append("..")

##----------------NOUVELLE CLASSE------------------##

class TestInterruption(unittest.TestCase):
    
    #----Fonction qui définit les éléments utiles pour réaliser les tests----#
    def setUp(self):
        test = open('test_out.json', "r")
        self.data = json.loads(test.read())
        self.regle_doses = re.compile(r"^(\d*)", re.IGNORECASE)
        self.regle_date = re.compile(r"\d{4}")

    #----Fonction de test de "calcul_nb_interruptions"----#
    def test_calcul_nb_interruptions(self):
        self.nb = Interruption.calcul_nb_interruptions(self.data, self.regle_doses)
        self.assertEquals(self.nb, 3)

    def test_extraction_dose_prescrite(self):
        liste_test = ['12', '10', '10', '33', '30', '10', '10', '30', '10', '28', '10', '10', '33', '10', '10', '11','15', '3', '7', '5', '15', '11']
        self.liste = Interruption.extraction_dose_prescrite(self.data, self.regle_doses)
    #----Fonction de test de "extraction_doses_prescrites"----#
        self.assertListEqual(liste_test,self.liste)

    #----Fonction de test de "extraction_doses_recues"----#
    def test_extraction_doses_recues(self):
        liste_test = ['12','10','10','32','30','10','9','30','10','28','8','10','33','10','10','11','15','3','7','5','15','11']
        self.liste = Interruption.extraction_doses_recues(self.data, self.regle_doses)
        self.assertListEqual(liste_test,self.liste)


##----------------FIN DE LA CLASSE TestInterruption------------------##

#Lancement du test : fournit une interface de ligne de commande au script de test ?
if __name__ == '__main__':
    unittest.main()
