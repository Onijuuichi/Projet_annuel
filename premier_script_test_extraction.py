# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 15:40:12 2022

@author: sshan
"""

#Projet annuel M1

import numpy as np
import pandas as pd
import re

class Interruption:
    
##----------------Constructeur---------------------##

    def __init__(self, fichier_out):
        self.fichier_out=fichier_out;
        
##------------Créer la liste des doses prescrites aux patients ---------##
        
    def extraction_dose_prescrite(fichier_out, regle):
        liste_match_prescrite=[]
        for ligne in fichier_out['NombreFractionsPrescrites']:
            match=regle.search(ligne)
            if match:
                liste_match_prescrite.append(match.group())
        return(liste_match_prescrite)        
      
#-----------------Créer la liste des doses recu des patients---------------------#
    
    def extraction_dose_recu(fichier_out, regle):
        liste_match_recu=[]
        for ligne in fichier_out['NombreFractionsDelivrees']:
            match=regle.search(ligne)
            if match:
                liste_match_recu.append(match.group())
        return(liste_match_recu) 
 
#--------------Calcul nombre d'interruption (dose prescrite!=dose reçu)-------------------#       
 
    def calcul_nb_interruption(fichier_out, regle):
        interruption=0
        liste_match_prescrite=Interruption.extraction_dose_prescrite(fichier_out, regle)
        liste_match_recu=Interruption.extraction_dose_recu(fichier_out, regle)
        for i in range(len(liste_match_prescrite)):
                if (liste_match_prescrite[i]!=liste_match_recu[i]):
                    interruption=interruption+1
        return(interruption) 

#----------------Créer une liste des dates de dernière prescription------------# 
     
    def extraction_date(fichier_out, regle):
        liste_match_date=[]
        for ligne in fichier_out['DateDerniereFraction']:
            match=regle.search(ligne)
            if match:
                liste_match_date.append(match.group())
        return(liste_match_date) 
        
##---------Test-----------##

fichier_out = pd.read_csv("/Users/sshan/OneDrive/Documents/COURS M1/PROJET ANNUEL/Projet_annuel/out.txt", sep='\t', index_col=0)

##-------Nos regex-------##
regle_doses=re.compile(r"^(\d*)", re.IGNORECASE)
regle_date=re.compile(r"\d{4}")

#print ("liste du nb de dose prescrite : " , Interruption.extraction_dose_prescrite(fichier_out, regle_doses))
#print("-------------------------------------------------------")
#print ("liste du nb de dose delivrees : ",  Interruption.extraction_dose_recu(fichier_out, regle_doses))
#print("nombre d'interruption : ", Interruption.calcul_nb_interruption(fichier_out, regle_doses))
print("Années : ", Interruption.extraction_date(fichier_out, regle_date))
