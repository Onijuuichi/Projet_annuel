# -*- coding: utf-8 -*-
"""
Projet annuel M1 GPhy 2021/2022

Premier script

@author: sshan
"""

##----------------MODULES IMPORTES-----------------##

import numpy as np
import pandas as pd
import re

##----------------NOUVELLE CLASSE Interruption------------------##

class Interruption:
    
    ##----CONSTRUCTEUR----##
    def __init__(self, fichier_out):
        self.fichier_out = fichier_out;
        
    #----Fonction qui crée la liste des doses prescrites aux patients----#
    def extraction_doses_prescrites(fichier_out, regle):
        liste_match_prescrite = []
        for ligne in fichier_out['NombreFractionsPrescrites']:
            match = regle.search(ligne)
            if match:
                liste_match_prescrite.append(match.group())
        return(liste_match_prescrite)        
      
    #----Fonction qui crée la liste des doses reçues par les patients----#
    def extraction_doses_recues(fichier_out, regle):
        liste_match_recu = []
        for ligne in fichier_out['NombreFractionsDelivrees']:
            match = regle.search(ligne)
            if match:
                liste_match_recu.append(match.group())
        return(liste_match_recu) 
 
    #----Fonction qui calcule le nombre d'interruptions de traitement (dose prescrite != dose reçue)----##       
    def calcul_nb_interruptions(fichier_out, regle):
        interruption = 0
        liste_match_prescrite = Interruption.extraction_doses_prescrites(fichier_out, regle)
        liste_match_recu = Interruption.extraction_doses_recues(fichier_out, regle)
        for i in range(len(liste_match_prescrite)):
            if (liste_match_prescrite[i] != liste_match_recu[i]):
                interruption = interruption + 1
        return(interruption) 

    #----Fonction qui crée une liste des dates de dernière prescription----# 
    #inutile en fait     
    # def extraction_annee(fichier_out, regle):
    #     liste_match_annee = []
    #     for ligne in fichier_out['DateDerniereFraction']:
    #         match = regle.search(ligne)
    #         if match:
    #             liste_match_annee.append(match.group())
    #     return(liste_match_annee) 
    
    #----Fonction qui calcule le nombre d'interruptions de traitement pour chaque année----#       
    def calcul_nb_interruptions_par_an(fichier_out, regle1, regle2, annee):
        interruption = 0
        liste_match_prescrite = Interruption.extraction_doses_prescrites(fichier_out, regle1)
        liste_match_recu = Interruption.extraction_doses_recues(fichier_out, regle1)
        liste_match_annee = Interruption.extraction_annee(fichier_out, regle2)
        for i in range(len(liste_match_prescrite)):
            if (liste_match_prescrite[i] != liste_match_recu[i] and int(liste_match_annee[i]) == annee):
                interruption = interruption + 1
        return(interruption) 
        
    #----Fonction : calcul final et affichage des résultats par an----# 
    def calcul(fichier_out, regle1, regle2):
        print("Nombre d'interruptions de traitement :")
        tot_interruption = Interruption.calcul_nb_interruptions(fichier_out, regle1)
        if(tot_interruption>0):
            for i in range(1955, 2050):
                interruption = Interruption.calcul_nb_interruptions_par_an(fichier_out, regle1, regle2, i)
                if (interruption>0):
                    pourcent = interruption / tot_interruption * 100
                    pourcent = round(pourcent, 1)
                    print("En", i, ":", interruption, "(", pourcent, "% )")
        else:
            print("Aucune interruption de traitement.")
            
##----------------FIN DE LA CLASSE Interruption------------------##
        
##----------------TESTS-----------------##

#fichier_out = pd.read_csv("/Users/sshan/OneDrive/Documents/COURS M1/PROJET ANNUEL/Projet_annuel/out.txt", sep='\t', index_col=0)
fichier_out = pd.read_csv("/Users/perar/Documents/GitHub/Projet_annuel/out.txt", sep='\t', index_col = 0, low_memory = False)

#----Nos regex----#
regle_doses = re.compile(r"^(\d*)", re.IGNORECASE)
regle_annee = re.compile(r"\d{4}")
regle_date = re.compile(r"\d{2}/\d{2}/\d{4}")

#print ("liste du nb de dose prescrite : " , Interruption.extraction_doses_prescrites(fichier_out, regle_doses))
#print("-------------------------------------------------------")
#print ("liste du nb de dose delivrees : ",  Interruption.extraction_doses_recues(fichier_out, regle_doses))
#print("nombre d'interruption : ", Interruption.calcul_nb_interruptions(fichier_out, regle_doses))
#print("Années : ", Interruption.extraction_annee(fichier_out, regle_annee))
#print("2020 : ", Interruption.calcul_nb_interruptions_par_an(fichier_out, regle_doses, regle_annee, 2020))
Interruption.calcul(fichier_out, regle_doses, regle_annee)
