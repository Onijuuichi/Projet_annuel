from premier_script_test_extraction import Interruption

import sys
import unittest
import pandas as pd
import re

sys.path.append("..")


class TestInterruption(unittest.TestCase):
    def setUp(self):
        self.fichier_out = pd.read_csv("/Users/Arthur/Desktop/PA/Projet_annuel/test_out.txt", sep='\t', index_col=0)
        self.regle_doses = re.compile(r"^(\d*)", re.IGNORECASE)

    def test_calcul_nb_interruption(self):
        self.nb = Interruption.calcul_nb_interruption(self.fichier_out, self.regle_doses)
        self.assertEquals(self.nb, 3)

    def test_extraction_dose_prescrite(self):
        liste_test = ['12', '10', '10', '33', '30', '10', '10', '30', '10', '28', '10', '10', '33', '10', '10', '11',
                      '15', '3', '7', '5', '15', '11'];
        self.liste = Interruption.extraction_dose_prescrite(self.fichier_out, self.regle_doses)
        self.assertListEqual(liste_test,self.liste)

    def test_extraction_dose_recu(self):
        liste_test = ['12','10','10','32','30','10','9','30','10','28','8','10','33','10','10','11','15','3','7','5','15','11']
        self.liste = Interruption.extraction_dose_recu(self.fichier_out, self.regle_doses)
        self.assertListEqual(liste_test,self.liste)

if __name__ == '__main__':
    unittest.main()
