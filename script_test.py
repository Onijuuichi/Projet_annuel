# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 15:40:12 2022

@author: sshan
"""

# Projet annuel M1

from datetime import datetime
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
import json

class Interruption:

    ##----------------Constructeur---------------------##

    def __init__(self, data):
        self.data = data;

    ##------------Créer la liste des doses prescrites aux patients ---------##

    def extraction_dose_prescrite(data, regle):
        liste_match_prescrite = []
        for ligne in data:
            match = regle.search(ligne['NombreFractionsPrescrites'])
            if match:
                liste_match_prescrite.append(match.group())
        return (liste_match_prescrite)

    # -----------------Créer la liste des doses recu des patients---------------------#

    def extraction_dose_recu(data, regle):
        liste_match_recu = []
        for ligne in data:
            match = regle.search(ligne['NombreFractionsDelivrees'])
            if match:
                liste_match_recu.append(match.group())
        return (liste_match_recu)

    # -----------------Verifie les noms de traitement (si PTV55 ou PTV27 return(False), sinon return(True)) ---------------------#

    def verifie_nom(data):
        liste_verifie_nom = []
        for ligne in data:
            if "PTV55" in ligne['Nom']:
                valide = False
            elif "PTV 55" in ligne['Nom']:
                valide = False
            elif "PTV27" in ligne['Nom']:
                valide = False
            elif "PTV 27" in ligne['Nom']:
                valide = False
            else:
                valide = True
            liste_verifie_nom.append(valide)
        return (liste_verifie_nom)

    # -----------------Créer la liste des dates de début de traitement (DatePremiereFraction) ---------------------#

    def extraction_date_debut(data, regle):
        liste_match_date_debut = []
        for ligne in data:
            match = regle.search(ligne['DatePremiereFraction'])
            if match:
                liste_match_date_debut.append(match.group())
        return (liste_match_date_debut)

    # -----------------Créer la liste des dates de fin de traitement (DateDerniereFraction) ---------------------#

    def extraction_date_fin(data, regle):
        liste_match_date_fin = []
        for ligne in data:
            match = regle.search(ligne['DateDerniereFraction'])
            if match:
                liste_match_date_fin.append(match.group())
        return (liste_match_date_fin)

    # --------------Verifie si le temps de traitement est supérieur à 4 semaines (si oui return(True), sinon return(False)-------------------#

    def verifie_temps(data, regle):
        liste_verifie_temps = []
        liste_match_date_fin = Interruption.extraction_date_fin(data, regle)
        liste_match_date_debut = Interruption.extraction_date_debut(data, regle)
        for i in range(len(liste_match_date_fin)):
            time_1 = datetime.strptime(liste_match_date_debut[i], "%d/%m/%Y")
            time_2 = datetime.strptime(liste_match_date_fin[i], "%d/%m/%Y")
            time_interval = time_2 - time_1
            time_ref = datetime.strptime("29", "%d")
            time_ref2 = datetime.strptime("01", "%d")
            time_interval_ref = time_ref - time_ref2
            if time_interval >= time_interval_ref:
                valide = True
            else:
                valide = False
            liste_verifie_temps.append(valide)
        return (liste_verifie_temps)

    # --------------Calcul nombre d'interruption (dose prescrite!=dose reçu)-------------------#

    def calcul_nb_interruption(data, regle1, regle2):
        interruption = 0
        liste_verifie_temps = Interruption.verifie_temps(data, regle2)
        liste_verifie_nom = Interruption.verifie_nom(data)
        liste_match_prescrite = Interruption.extraction_dose_prescrite(data, regle1)
        liste_match_recu = Interruption.extraction_dose_recu(data, regle1)
        for i in range(len(liste_match_prescrite)):
            if (liste_verifie_temps[i] and liste_verifie_nom[i]):
                if (liste_match_prescrite[i] != liste_match_recu[i]):
                    interruption = interruption + 1
        return (interruption)

    # ----------------Créer une liste des annees de dernière prescription------------#

    def extraction_annee(data, regle):
        liste_match_annee = []
        for ligne in data:
            match = regle.search(ligne['DateDerniereFraction'])
            if match:
                liste_match_annee.append(match.group())
        return (liste_match_annee)

    # --------------Calcul nombre d'interruption selon l'annéee-------------------#

    def calcul_nb_interruption_par_an(data, regle1, regle2, regle3, annee):
        interruption = 0
        liste_verifie_temps = Interruption.verifie_temps(data, regle3)
        liste_verifie_nom = Interruption.verifie_nom(data)
        liste_match_prescrite = Interruption.extraction_dose_prescrite(data, regle1)
        liste_match_recu = Interruption.extraction_dose_recu(data, regle1)
        liste_match_annee = Interruption.extraction_annee(data, regle2)
        for i in range(len(liste_match_prescrite)):
            if (liste_verifie_temps[i] and liste_verifie_nom[i]):
                if (liste_match_prescrite[i] != liste_match_recu[i] and int(liste_match_annee[i]) == annee):
                    interruption = interruption + 1
        return (interruption)

    # --------------Calcul final et affichage des résultats par an-------------------#

    def calcul(data, regle1, regle2, regle3):
        interruption_liste = []
        print("Nombre d'interruption :")
        tot_interruption = Interruption.calcul_nb_interruption(data, regle1, regle3)
        if (tot_interruption > 0):
            for i in range(1955, 2050):
                interruption = Interruption.calcul_nb_interruption_par_an(data, regle1, regle2, regle3, i)
                if (interruption > 0):
                    interruption_liste.append(interruption)
                    pourcent = (interruption / tot_interruption * 100)
                    pourcent = round(pourcent, 1)
                    print("En", i, ":", interruption, "(", pourcent, "% )")
            # df = pd.DataFrame(interruption_liste, columns = ['interruption'], index=['20' + str(i) for i in range(14,22)])
            color = sns.color_palette('pastel')
            fig = plt.figure(1, figsize=(10, 10))
            #plt.pie(interruption_liste, labels=['20' + str(i) for i in range(14, 22)], colors=color, autopct="%.1f%%")
            plt.plot(['20' + str(i) for i in range(14, 22)], interruption_liste, label="Centre Oscar Lambret")
            plt.xlabel(' Années')
            plt.ylabel(' Nombre d\'interrution')
            plt.title('Nombre d\'interruption de traitement par année')
            plt.legend("Centre Oscar Lambret")
            plt.legend(interruption_liste)
            plt.title('Nombre d\'interruption de traitement par année')
            # plt.savefig('/Users/sshan/OneDrive/Documents/COURS M1/PROJET ANNUEL/Projet_annuel/Camembert_interruption.png')
            plt.savefig('Camembert_interruption.png')
            plt.show()

        else:
            print("Aucune interruption.")


##---------Test-----------##

test = open('test.json', "r")
data = json.loads(test.read())

# fichier_out = pd.read_csv("/Users/sshan/OneDrive/Documents/COURS M1/PROJET ANNUEL/Projet_annuel/out.txt", sep='\t', index_col=0, low_memory=(False))
fichier_out = pd.read_csv("out.txt", sep='\t', index_col=0, low_memory=(False))

##-------Nos regex-------##
regle_doses = re.compile(r"^(\d*)",
                         re.IGNORECASE)  # regex permettant de récupérer uniquement les premiers chiffres dans les valeurs des doses
regle_annee = re.compile(r"\d{4}")  # regex permettant de récupérer uniquement l'année
regle_date = re.compile(r"\d{2}/\d{2}/\d{4}")  # regex permettant de récupérer entièrement la date

# print ("liste du nb de dose prescrite : " , Interruption.extraction_dose_prescrite(fichier_out, regle_doses))
# print("-------------------------------------------------------")
# print ("liste du nb de dose delivrees : ",  Interruption.extraction_dose_recu(fichier_out, regle_doses))
# print("nombre d'interruption : ", Interruption.calcul_nb_interruption(fichier_out, regle_doses, regle_date))
# print("Années : ", Interruption.extraction_annee(fichier_out, regle_annee))
# print("2020 : ", Interruption.calcul_nb_interruption_par_an(fichier_out, regle_doses, regle_annee, regle_date, 2020))
Interruption.calcul(data, regle_doses, regle_annee, regle_date)
# print(Interruption.verifie_nom(fichier_out))
# print(Interruption.verifie_temps(fichier_out, regle_date))

