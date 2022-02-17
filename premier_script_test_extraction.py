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
        
##------------Calcul nombre d'interruption (dose prescrite!=dose reçu) ---------##
        
    def extraction_dose_prescrite(fichier_out, regle):
        liste_match_prescrite=[]
        for ligne in fichier_out['NombreFractionsPrescrites']:
            match=regle.search(ligne)
            if match:
                liste_match_prescrite.append(match.group())
        return(liste_match_prescrite);          
      
#------------------------------------------------------------------------------#
    
    def extraction_dose_recu(fichier_out, regle):
        liste_match_recu=[]
        for ligne in fichier_out['NombreFractionsDelivrees']:
            match=regle.search(ligne)
            if match:
                liste_match_recu.append(match.group())
        return(liste_match_recu); 
 
#-------------------------------------------------------------------------------#       
 
    def calcul_nb_interruption(fichier_out, regle):
        cpt=0
        liste_match_prescrite=Interruption.extraction_dose_prescrite(fichier_out, regle)
        liste_match_recu=Interruption.extraction_dose_recu(fichier_out, regle)
        for i in liste_match_prescrite:
            for j in liste_match_recu:
                if(liste_match_prescrite[i]!=(liste_match_recu[j])):
                    cpt=cpt+1      
        return(cpt) 

#------------------------------------------------------------------------------# 
     
##---------Test-----------##

fichier_out = pd.read_csv("/Users/sshan/OneDrive/Documents/COURS M1/PROJET ANNUEL/Projet_annuel/out.txt", sep='\t', index_col=0)
regle_doses=re.compile(r"^(\d*)", re.IGNORECASE)
print ("liste du nb de dose prescrite : " , Interruption.extraction_dose_prescrite(fichier_out, regle_doses))
print("-------------------------------------------------------")
print ("liste du nb de dose delivrees : ",  Interruption.extraction_dose_recu(fichier_out, regle_doses))
print("nombre d'interruption : ", Interruption.calcul_nb_interruption(fichier_out, regle_doses))