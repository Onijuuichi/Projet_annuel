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
     
    def extraction_annee(fichier_out, regle):
        liste_match_annee=[]
        for ligne in fichier_out['DateDerniereFraction']:
            match=regle.search(ligne)
            if match:
                liste_match_annee.append(match.group())
        return(liste_match_annee) 
    
#--------------Calcul nombre d'interruption selon l'annéee-------------------#       
 
    def calcul_nb_interruption_par_an(fichier_out, regle1, regle2, annee):
        interruption=0
        liste_match_prescrite=Interruption.extraction_dose_prescrite(fichier_out, regle1)
        liste_match_recu=Interruption.extraction_dose_recu(fichier_out, regle1)
        liste_match_annee=Interruption.extraction_annee(fichier_out, regle2)
        for i in range(len(liste_match_prescrite)):
            if (liste_match_prescrite[i]!=liste_match_recu[i] and int(liste_match_annee[i])==annee):
                interruption=interruption+1
        return(interruption) 
        
#--------------Calcul final et affichage des résultats par an-------------------# 
    
    def calcul(fichier_out, regle1, regle2):
        print("Nombre d'interruption :")
        tot_interruption=Interruption.calcul_nb_interruption(fichier_out, regle1)
        if(tot_interruption>0):
            for i in range(1955, 2050):
                interruption=Interruption.calcul_nb_interruption_par_an(fichier_out, regle1, regle2, i)
                if (interruption>0):
                    pourcent=interruption/tot_interruption*100
                    pourcent=round(pourcent, 1)
                    print("En", i, ":", interruption, "(", pourcent, "% )")
        else:
            print("Aucune interruption.")
            
                    
                    
                    
       
        
   
        
##---------Test-----------##

#fichier_out = pd.read_csv("/Users/sshan/OneDrive/Documents/COURS M1/PROJET ANNUEL/Projet_annuel/out.txt", sep='\t', index_col=0)
fichier_out = pd.read_csv("/Users/damienarrive/Documents/GitHub/Projet_annuel/out.txt", sep='\t', index_col=0)

##-------Nos regex-------##
regle_doses=re.compile(r"^(\d*)", re.IGNORECASE)
regle_annee=re.compile(r"\d{4}")
regle_date=re.compile(r"\d{2}/\d{2}/\d{4}")

#print ("liste du nb de dose prescrite : " , Interruption.extraction_dose_prescrite(fichier_out, regle_doses))
#print("-------------------------------------------------------")
#print ("liste du nb de dose delivrees : ",  Interruption.extraction_dose_recu(fichier_out, regle_doses))
#print("nombre d'interruption : ", Interruption.calcul_nb_interruption(fichier_out, regle_doses))
#print("Années : ", Interruption.extraction_annee(fichier_out, regle_annee))
#print("2020 : ", Interruption.calcul_nb_interruption_par_an(fichier_out, regle_doses, regle_annee, 2020))
Interruption.calcul(fichier_out, regle_doses, regle_annee)
