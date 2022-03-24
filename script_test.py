# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 15:40:12 2022

@author: sshan
"""

#Projet annuel M1

from datetime import datetime
from datetime import timedelta  
#import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns

class Interruption:
    
##----------------Constructeur---------------------##

    def __init__(self, fichier_out):
        self.fichier_out=fichier_out;
        
##------------Créer la liste des doses prescrites aux patients ---------##
        
    def extraction_dose_prescrite(fichier_out, regleDose):
        liste_match_prescrite=[]
        for ligne in fichier_out['NombreFractionsPrescrites']:
            match=regleDose.search(ligne)
            if match:
                liste_match_prescrite.append(match.group())
        return(liste_match_prescrite)        
      
#-----------------Créer la liste des doses recu des patients---------------------#
    
    def extraction_dose_recu(fichier_out, regleDose):
        liste_match_recu=[]
        for ligne in fichier_out['NombreFractionsDelivrees']:
            match=regleDose.search(ligne)
            if match:
                liste_match_recu.append(match.group())
        return(liste_match_recu) 
    

#-----------------Verifie les noms de traitement (si PTV55 ou PTV27 return(False), sinon return(True)) ---------------------#
    
    def verifie_nom(fichier_out):
        liste_verifie_nom=[]
        for ligne in fichier_out['Nom']:
            if "PTV55" in ligne:
                valide=False
            elif "PTV 55" in ligne:
                valide=False
            elif "PTV27" in ligne:
                valide=False
            elif "PTV 27" in ligne:
                valide=False
            else:
                valide=True
            liste_verifie_nom.append(valide)
        return(liste_verifie_nom) 
    
    
#--------------Verifie si le temps de traitement est supérieur à 4 semaines (si oui return(True), sinon return(False)-------------------#       
 
    def verifie_temps(fichier_out, regleDate):
        liste_verifie_temps=[]
        liste_match_date_fin=Interruption.extraction_date_fin(fichier_out, regleDate)
        liste_match_date_debut=Interruption.extraction_date_debut(fichier_out, regleDate)
        for i in range(len(liste_match_date_fin)):
            time_1 = datetime.strptime(liste_match_date_debut[i],"%d/%m/%Y")
            time_2 = datetime.strptime(liste_match_date_fin[i],"%d/%m/%Y")
            time_interval = time_2 - time_1
            time_ref = datetime.strptime("29", "%d")
            time_ref2 = datetime.strptime("01", "%d")
            time_interval_ref = time_ref - time_ref2
            if time_interval >= time_interval_ref:
                valide = True
            else:
                valide = False
            liste_verifie_temps.append(valide)
        return(liste_verifie_temps) 
    
 
    
#-----------------Créer la liste des dates de début de traitement (DatePremiereFraction) ---------------------#
    
    def extraction_date_debut(fichier_out, regleDate):
        liste_match_date_debut=[]
        for ligne in fichier_out['DatePremiereFraction']:
            match=regleDate.search(ligne)
            if match:
                liste_match_date_debut.append(match.group())
        return(liste_match_date_debut) 
    
    
#-----------------Créer la liste des dates de début de traitement avec la règle des 4 semaines et des PTV (DatePremiereFraction) ---------------------#
    
    def extraction_date_debut2(fichier_out, regleDate):
        liste_match_date_debutV=[]
        liste_match_date_debutF=Interruption.extraction_date_debut(fichier_out, regleDate)
        liste_verifie_temps=Interruption.verifie_temps(fichier_out, regleDate)
        liste_verifie_nom=Interruption.verifie_nom(fichier_out)
        for i in range(len(liste_match_date_debutF)):
            if (liste_verifie_temps[i] and liste_verifie_nom[i]):
                liste_match_date_debutV.append(liste_match_date_debutF[i])
        return(liste_match_date_debutV) 
    
    
#-----------------Créer la liste des dates de fin de traitement théorique (DateDerniereFraction) ---------------------#
    
    def extraction_date_fin(fichier_out, regleDate):
        liste_match_date_fin=[]
        for ligne in fichier_out['DateDerniereFraction']:
            match=regleDate.search(ligne)
            if match:
                liste_match_date_fin.append(match.group())
        return(liste_match_date_fin) 
    
    
#-----------------Créer la liste des dates de fin de traitement théorique avec la règle des 4 semaines et des PTV (DateDerniereFraction) ---------------------#
    
    def extraction_date_fin2(fichier_out, regleDate):
        liste_match_date_finV=[]
        liste_match_date_finF=Interruption.extraction_date_fin(fichier_out, regleDate)
        liste_verifie_temps=Interruption.verifie_temps(fichier_out, regleDate)
        liste_verifie_nom=Interruption.verifie_nom(fichier_out)
        for i in range(len(liste_match_date_finF)):
            if (liste_verifie_temps[i] and liste_verifie_nom[i]):
                liste_match_date_finV.append(liste_match_date_finF[i])
        return(liste_match_date_finV) 
    
    
#-----------------Créer la liste des dates de fin de traitement theorique () ---------------------#
    
    def calcul_date_fin(fichier_out, regleDate, regleDose):
        liste_match_date_fin=[]
        liste_match_prescrite=Interruption.extraction_dose_prescrite(fichier_out, regleDose)
        liste_match_date_debut=Interruption.extraction_date_debut2(fichier_out, regleDate) ##
        for i in range(len(liste_match_date_debut)):
            dose=int(liste_match_prescrite[i])
            if(dose>=7):
                nb_de_dimanche=dose/7
                x=nb_de_dimanche%1  #on isole la décimale
                nb_de_dimanche=nb_de_dimanche-x  #on soustrait la décimale
            else:
                nb_de_dimanche=0
            jour_traitement=dose+nb_de_dimanche
            date_debut=datetime.strptime(liste_match_date_debut[i],"%d/%m/%Y")
            date_fin=date_debut+timedelta(days=jour_traitement)
            date_fin=str(date_fin)
            liste_match_date_fin.append(date_fin)
        return(liste_match_date_fin) 
    
    
#------------------Transtypage des jours (datatime => integer)-------------------#

    def jour_int(date):
        date=str(date)
        if 'days' in date:
            date=date.removesuffix(' days, 0:00:00')
        else:
            date="0"
        date=int(date)
        return(date)
    
    
#-----------------Créer la liste des intervalles des dates de fin entre réelles et théoriques---------------------#
    
    def calcul_intervalle_fin(fichier_out, regleDate, regleDose):
        liste_match_intervalle_date_fin=[]
        liste_match_date_fin_theo=Interruption.calcul_date_fin(fichier_out, regleDate, regleDose)
        liste_match_date_fin_reel=Interruption.extraction_date_fin2(fichier_out, regleDate)  ##
        for i in range(len(liste_match_date_fin_theo)):
            date_fin_reel=datetime.strptime(liste_match_date_fin_reel[i],"%d/%m/%Y")
            date_fin_theorique=datetime.strptime(liste_match_date_fin_theo[i],"%Y-%m-%d %H:%M:%S")
            
            intervalle=date_fin_theorique-date_fin_reel
            #intervalle=date_fin_theorique-date_fin_reel
            
            intervalle=Interruption.jour_int(intervalle)
            liste_match_intervalle_date_fin.append(intervalle)
        return(liste_match_intervalle_date_fin)
    
    
    
#-----------------Le pourcentage de difference entre fin de traitement théorique et réel---------------------#

    def calcul_pourcentage(fichier_out, regleDate, regleDose):
        totP=0
        liste_intervalle=Interruption.calcul_intervalle_fin(fichier_out, regleDate, regleDose)
        liste_date_fin_theo=Interruption.calcul_date_fin(fichier_out, regleDate, regleDose)
        liste_date_fin_reel=Interruption.extraction_date_fin2(fichier_out, regleDate)  ## 
        liste_date_debut=Interruption.extraction_date_debut2(fichier_out, regleDate)  ##
        for i in range(len(liste_intervalle)):
            date_fin_reel=datetime.strptime(liste_date_fin_reel[i],"%d/%m/%Y")
            date_fin_theo=datetime.strptime(liste_date_fin_theo[i],"%Y-%m-%d %H:%M:%S")
            date_debut=datetime.strptime(liste_date_debut[i],"%d/%m/%Y")
            nb_jour_traitement=date_fin_reel-date_debut
            #nb_jour_traitement=date_fin_theo-date_debut
            nb_jour_traitement=Interruption.jour_int(nb_jour_traitement)
            if nb_jour_traitement!=0 and nb_jour_traitement!=0:
                pourcent=liste_intervalle[i]/nb_jour_traitement*100                
                pourcent=round(pourcent, 2)
            else:
                pourcent=0
            totP=totP+pourcent
            
            nb_jour_T=date_fin_theo-date_debut
            nb_jour_T=Interruption.jour_int(nb_jour_T)
            nb_jour_R=date_fin_reel-date_debut
            nb_jour_R=Interruption.jour_int(nb_jour_R)
            print(i, "=> nb jour theorique : ", nb_jour_T, " - nb jour reel : ", nb_jour_R, " => diff : ", liste_intervalle[i], " => ", pourcent, "%")
            
        moyenne=totP/len(liste_intervalle)
        moyenne=round(moyenne, 2)
        return(moyenne)
            

#--------------Calcul nombre d'interruption (dose prescrite!=dose reçu)-------------------#       
 
    def calcul_nb_interruption(fichier_out, regleDate, regleDose):
        interruption=0
        liste_verifie_temps=Interruption.verifie_temps(fichier_out, regleDate)
        liste_verifie_nom=Interruption.verifie_nom(fichier_out)
        liste_match_prescrite=Interruption.extraction_dose_prescrite(fichier_out, regleDose)
        liste_match_recu=Interruption.extraction_dose_recu(fichier_out, regleDose)
        for i in range(len(liste_match_prescrite)):
            if (liste_verifie_temps[i] and liste_verifie_nom[i]):
                if (liste_match_prescrite[i]!=liste_match_recu[i]):
                    interruption=interruption+1
        return(interruption) 
    

#----------------Créer une liste des annees de dernière prescription------------# 
     
    def extraction_annee(fichier_out, regleDate, regleAnnee):
        liste_match_annee=[]
        liste_verifie_temps=Interruption.verifie_temps(fichier_out, regleDate)
        liste_verifie_nom=Interruption.verifie_nom(fichier_out)
        for ligne in fichier_out['DateDerniereFraction']:
            if (liste_verifie_temps[ligne] and liste_verifie_nom[ligne]):
                match=regleAnnee.search(ligne)
                if match:
                    liste_match_annee.append(match.group())
        return(liste_match_annee) 

    
#--------------Calcul nombre d'interruption selon l'annéee-------------------#       
 
    def calcul_nb_interruption_par_an(fichier_out, regleDate, regleDose, regleAnnee, annee):
        interruption=0
        liste_verifie_temps=Interruption.verifie_temps(fichier_out, regleDate)
        liste_verifie_nom=Interruption.verifie_nom(fichier_out)
        liste_match_prescrite=Interruption.extraction_dose_prescrite(fichier_out, regleDose)
        liste_match_recu=Interruption.extraction_dose_recu(fichier_out, regleDose)
        liste_match_annee=Interruption.extraction_annee(fichier_out, regleAnnee)
        for i in range(len(liste_match_prescrite)):
            if (liste_verifie_temps[i] and liste_verifie_nom[i]):
                if (liste_match_prescrite[i]!=liste_match_recu[i] and int(liste_match_annee[i])==annee):
                    interruption=interruption+1
        return(interruption)
        
#--------------Calcul final et affichage des résultats par an-------------------# 
    
    def calcul(fichier_out, regleDate, regleDose, regleAnnee):
        interruption_liste=[]
        print("Nombre d'interruption :")
        tot_interruption=Interruption.calcul_nb_interruption(fichier_out, regleDate, regleDose)
        if(tot_interruption>0):
            for i in range(1955, 2050):
                interruption=Interruption.calcul_nb_interruption_par_an(fichier_out, regleDate, regleDose, regleAnnee, i)
                if (interruption>0):
                    interruption_liste.append(interruption)
                    pourcent=(interruption/tot_interruption*100)
                    pourcent=round(pourcent, 1)
                    print("En", i, ":", interruption, "(", pourcent, "% )")
            #df = pd.DataFrame(interruption_liste, columns = ['interruption'], index=['20' + str(i) for i in range(14,22)]) 
            color=sns.color_palette('pastel')
            fig = plt.figure(1, figsize=(10, 10))
            plt.plot(['20' + str(i) for i in range(14,22)], interruption_liste, label="Centre Oscar Lambret" )
            plt.xlabel(' Années')
            plt.ylabel(' Nombre d\'interrution')
            plt.title('Nombre d\'interruption de traitement par année')
            plt.legend("Centre Oscar Lambret")
            #plt.savefig('/Users/sshan/OneDrive/Documents/COURS M1/PROJET ANNUEL/Projet_annuel/Camembert_interruption.png')
            plt.savefig('/Users/damienarrive/Documents/GitHub/Projet_annuel/Camembert_interruption.png')
            plt.show()
                    
        else:
            print("Aucune interruption.")
            
      
##---------Fichier-----------##

#fichier_out = pd.read_csv("/Users/sshan/OneDrive/Documents/COURS M1/PROJET ANNUEL/Projet_annuel/out.txt", sep='\t', index_col=0, low_memory=(False))
fichier_out = pd.read_csv("/Users/damienarrive/Documents/GitHub/Projet_annuel/out.txt", sep='\t', index_col=0)

##-------Nos regex-------##

regleDose=re.compile(r"^(\d*)", re.IGNORECASE) #regex permettant de récupérer uniquement les premiers chiffres dans les valeurs des doses
regleAnnee=re.compile(r"\d{4}") #regex permettant de récupérer uniquement l'année
regleDate=re.compile(r"\d{2}/\d{2}/\d{4}") #regex permettant de récupérer entièrement la date 


##------Test-------------##

print(Interruption.calcul_pourcentage(fichier_out, regleDate, regleDose))
#Interruption.calcul_intervalle_fin(fichier_out, regleDate, regleDose)

