# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 15:40:12 2022

@author: sshan
"""

#Projet annuel M1

import numpy as np
import pandas as pd
import re

##------------Calcul nombre d'interruption (dose prescrite!=dose reçu) ---------##

def extraction_dose_prescrite(fichier_out, regle):
    dose_prescrite=fichier_out["NombreFractionsPrescrites"].totxt                    
    liste_match=pd.DataFrame()
    for i in dose_prescrite.columns[:]:
        match=regle.search(i)
        if match:
           liste_match.append(match.group())
    return (liste_match)
        

##---------Test------##
fichier_out= pd.read_csv('C:/Users/sshan/OneDrive/Documents/COURS M1/PROJET ANNUEL/Projet_annuel/out.csv', sep=',', header=0)
fichier_out.index=fichier_out.id
regle=re.compile(r"\d*(;\d*)+", re.IGNORECASE)
print (extraction_dose_prescrite(fichier_out, regle))