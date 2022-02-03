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
   fichier = open(fichier_out, "r")
   liste_match=[]
   for ligne in fichier:
       match=regle.search(ligne)
       if match:
           liste_match.append(match.group())
   fichier.close()
   return(liste_match);          
    
        

##---------Test------##


regle=re.compile(r"^(\d*)", re.IGNORECASE)
print (extraction_dose_prescrite("out.txt", regle))