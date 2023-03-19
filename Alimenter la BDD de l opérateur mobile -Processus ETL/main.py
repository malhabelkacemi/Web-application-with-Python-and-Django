import csv
import random
import sys
import time
from _csv import writer
from collections import OrderedDict
from random import randint
from statistics import mean
from tkinter import filedialog
from faker import Faker
from pymongo import MongoClient
from _datetime import datetime
import radar
import pandas
from datetime import date
import json
import time
from csv import DictWriter


fake = Faker('fr_FR')

myclient=MongoClient('localhost',27017)
#print(myclient.list_database_names())



ListeWilaya = [
    "Adrar","Chlef", "Laghouat", "Bouaghi", "Batna", "Bejaïa", "Biskra","Bechar", "Blida", "Bouira","Tamanrasset","Tebessa","Tlemcen", "Tiaret",
    "TiziOuzou", "Alger", "Djelfa", "Jijel","Setif", "Saïda", "Skikda","SidiBelAbbès","Annaba", "Guelma ","Constantine", "Medea", "Mostaganem",
    "Msila", "Mascara", "Ouargla","Oran", "ElBayadh", "Illizi","Bordj Bou Arreridj","Boumerdes","ElTarf", "Tindouf" ,"Tissemsilt", "ElOued",
    "Khenchela", "SoukAhras ", "Tipaza ", "Mila","Aïn Defla", "Naàma", "AïnTemouchent","Ghardaïa","Relizane",
    ]

def _GenerateDateBetween(d1,d2):
    date= fake.date_time_between(start_date=d1, end_date=d2)  #(start_date='-60y', end_date='now')
    date=str(date)
    date= date.split(" ")
    return (date[0])




def parse(my_date): #convertir une date apartir de type string à Date
    #print("mydate:" ,my_date)
    c=my_date.split('-')
    y=int(c[0])
    m=int(c[1])
    d=int(c[2])

    g= date(y, m, d)

    return  g

def days_diff(date_1, date_2): #trouver la difference en jours entre deux dates de type String

    da1= date_1.split("-")
    day1=int(da1[2])



    da2 = date_2.split("-")
    day2 = int(da2[2])


    if (int(da2[1])==2):
        if(int(da2[2])>=28):
          da2[2]=28
          date_2 = str(da2[0]) + "-" + str(da2[1]) + "-" + str(day2)


    if (int(da1[1])==2):
        print()
        if (day1 >= 28):
            day1=28
            date_1 = str(da1[0]) + "-" + str(da1[1]) + "-" + str(day1)


    if (day2==0):
        day2=1
        date_2=str(da2[0]) + "-" + str(da2[1]) + "-" + str(day2)

    if (day1==0):
        day1=1
        date_1 = str(da1[0]) + "-" + str(da1[1]) + "-" + str(day1)


    l=_CompareTwoDates(date_1,date_2)
    if(l==1):
       a=abs((parse(date_1) - parse(date_2)).days)
    else:
        a = abs((parse(date_2) - parse(date_1)).days)
    #print("nbr de jours entre les 2 dates" ,a)
    return a


DateCreationOperateur=_GenerateDateBetween('-8y','-8y') #2014


def _Generer_Prenom():
  return  fake.first_name()


def _Generer_Nom():
    return fake.last_name()

def _Generer_Adresse():
    r=randint(1,len(ListeWilaya)-1)
    return ListeWilaya[r].replace("ï", "i").replace("É", "E").replace("é", "e").replace("ê", "e").replace("è", "e").replace("à", "a").replace("ç",  "c")

def _Generer_Nom_Entreprise():
    return fake.company()

def _GenerernumcontratP():
    num=fake.random_int(min=00000, max=999999)
    num=str(num)
    num='P'+num
    return num

def _GenerernumcontratE():
    num=fake.random_int(min=00000, max=999999)
    num=str(num)
    num='E'+num
    return num


#Reclamations
def _Generer_Reclamation():
    Rec=fake.random_choices(elements=OrderedDict(((1, 0.19), (2, 0.23), (3, 0.07), (4, 0.12),(5, 0.08),(6, 0.05),(7, 0.10),(8, 0.16))), length=1)
   # print(Rec)
    Reclamations = {
        1: "Coupures de l acces internet (mauvaise qualite du reseau internet) §.",
        2: "La reception d appels indesirables!!!!!!.",
        3: "Ne pas pouvoir passer/recevoir des appels / sms.",
        4: "Mauvaise qualite du reseau telephone. ",
        5: "Probleme de contrat.",
        6: "Probleme d augmentations tarifaires.",
        7: "Probleme entre la souscription du forfait ~~ et l activation du service.",
        8: "Mauvaise couverture sur ^ l axe de transport et a l interieur des batiments .",
    }
    return Reclamations[Rec[0]]


#Numero de tel
def _GenererPrefixOper():
    #Code_p = fake.random_choices(elements=OrderedDict([("07", 0.40), ("06", 0.33), ("05", 0.40)]), length=1)
    return "07"

prefixOper=_GenererPrefixOper()
def _GenererPhoneNumberParticulier(prefixOper):
    x=""
    for i in range(0, 8):
      x=x+str(randint(0,9))

    phone_number_Particulier = x
    return F'{prefixOper}{phone_number_Particulier}'



#convertir les secondes en format H:M:S
def _Convert_Seconds(seconds):
    return time.strftime("%H:%M:%S", time.gmtime(seconds))


#convertir à partir de format H:M:S  en secondes
def _hms_to_Seconds(t):
    h,m,s = [int(i) for i in t.split(":")]
    return 3600*h + 60*m +s


#Answered_Resolved cas
#print("Answered_Resolved cas ")#y_y  OU:  N_N for : (Ignored calls)  OU:  Y_N
def _Gnererer_Answered_Resolved():
    element = fake.random_choices(elements=OrderedDict((("yy", 0.66), ("nn", 0.18), ("yn", 0.16))), length=1)
    #print(element)
    if element[0] == "yy" :
        #print("yy")
        return 11 #en binaire
    elif element[0]== "nn":
        #print("nn")
        return 00
    else:
        #print("yn")
        return 10


#Generer SpeedAnswer
def _SpeedAnswer():
     y=randint(11,125)
     y=_Convert_Seconds(y)
     return y


#Generer Talk_Duration
def _Talk_Duration():
     y=randint(32,420)
     y=_Convert_Seconds(y)
     return y


#Concurrent
def _GenererNbrAbonnes():
    return randint(300000, 480000)

def _Generer_Taux_Couverture_Concurrent():
    wilayas= randint(1, 48)
    taux=(wilayas/48)*100
    return round(taux,2)


def _DateFinForfait(dateAchatForf, Mois, Jour): #generer une date fin forfait apartir de la date d achat forfait
                                                # Pour les param Mois et Jour c'est pour la duree de forfait (par exemple 3 mois, 15jours ...)

    dateAchatForf = str(dateAchatForf)
    dateAchatForf = dateAchatForf.split("-")
    year1 = int(dateAchatForf[0])
    month1 = int(dateAchatForf[1])
    day1 = int(dateAchatForf[2])

    JourFinForf = day1 + Jour
    MoisFinForf = month1 + Mois
    if (MoisFinForf == 0):
        MoisFinForf = 12
    AnneeFinForf = year1

    if(MoisFinForf==12):
         if (JourFinForf <30):
            JourFinForf = JourFinForf
         elif (JourFinForf >= 30):
            JourFinForf = JourFinForf % 30
            MoisFinForf = (month1 + Mois) % 12
            MoisFinForf += 1  # incrementer le mois
            AnneeFinForf += 1

    elif (MoisFinForf < 12):
        if (JourFinForf < 30):
            JourFinForf = JourFinForf
        elif (JourFinForf >= 30):
            JourFinForf = JourFinForf % 30
            MoisFinForf = (month1 + Mois) % 12
            if (MoisFinForf == 0):
                MoisFinForf = 12
            MoisFinForf += 1  # incrementer le mois

    else:  # (MoisFinForf > 12):
        MoisFinForf = (month1 + Mois) % 12
        if (MoisFinForf == 0):
            MoisFinForf = 12
        AnneeFinForf += 1  # incrementer l annee

    DateFinForfait = str(AnneeFinForf) + "-" + str(MoisFinForf) + "-" + str(JourFinForf)

    return DateFinForfait


#forfaits particulier

def _ListeForfaitParticulier(Date_Debut_Contrat,dfin):


    c= fake.random_choices(elements=OrderedDict([("Aucun_forfait", 0.10),("m", 0.40), ("j", 0.28)]), length=1)[0]
    if(c=="Aucun_forfait"):
     print("Aucun forfait")
     return None
    else:
        Forfaits = []
        annees=_differenceDate(dfin, Date_Debut_Contrat)

        print(annees)
        if(annees==0):
            y = randint(2, 5)
        else:
            y=randint(5,25)*annees #nbr forfaits à generer pr un particulier par annee

        for i in range(1, y):
            Choix = fake.random_choices(elements=OrderedDict([("m", 0.60), ("j", 0.40)]), length=1)[0] #choisir forfait par mois ou jours
            if(Choix=="m"): #si forfait par mois
                Date_Achat_Forfait = _dateEntre(Date_Debut_Contrat, dfin)
                s=randint(1,6)#un forfait de 1 mois , 2 mois ... jusqu'a 6 mois (max)
                Date_Fin_Forfait = _DateFinForfait(Date_Achat_Forfait, s, 0)
                if(_CompareTwoDates(Date_Fin_Forfait,dfin)==1):
                    break
                else:
                    if (s==1):  # 1mois
                        Nforfait = "Forfait_" + str(s) + "Mois"
                        duree = s
                        prix = 1000
                        sms = "Illimite vers meme operateur"
                        appel = "Illimite vers meme operateur et 1500DA vers les autres reseaux"
                        Volume_Internet = 15  # 15 GO
                    if (s==2):
                        Nforfait = "Forfait_" + str(s) + "Mois"
                        duree = s  # 2mois
                        prix = 1600
                        sms = "Illimite vers meme operateur"
                        appel = "Illimite vers meme operateur et 2000DA vers les autres reseaux"
                        Volume_Internet = 20
                    if (s==3):
                        Nforfait = "Forfait_" + str(s) + "Mois"
                        duree = s  # 3mois
                        prix = 2000
                        sms = "Illimite vers meme operateur"
                        appel = "Illimite vers meme operateur et 2500DA vers les autres reseaux"
                        Volume_Internet = 25
                    if (s==4):
                        Nforfait = "Forfait_" + str(s) + "Mois"
                        duree = s  # 4mois
                        prix = 2500
                        sms = "Illimite vers meme operateur"
                        appel = "Illimite vers meme operateur et 3000DA vers les autres reseaux"
                        Volume_Internet = 20
                    if (s==5):
                        Nforfait = "Forfait_" + str(s) + "Mois"
                        duree = s  # 5mois
                        prix = 3000
                        sms = "Illimite vers meme operateur"
                        appel = "Illimite vers meme operateur et 3500DA vers les autres reseaux"
                        Volume_Internet = 30
                    if (s==6):
                        Nforfait = "Forfait_" + str(s) + "Mois"
                        duree = s  # 6mois
                        prix = 4000
                        sms = "Illimite vers meme operateur"
                        appel = "Illimite vers meme operateur et 4000DA vers les autres reseaux"
                        Volume_Internet = 35

            else: #forfait par jours

                Date_Achat_Forfait = _dateEntre(Date_Debut_Contrat, dfin)
                s=fake.random_choices(elements=OrderedDict([(1, 0.60), (15, 0.40),(20, 0.40)]), length=1)[0]
                Date_Fin_Forfait = _DateFinForfait(Date_Achat_Forfait, 0,s)
                if(_CompareTwoDates(Date_Fin_Forfait,dfin)==1): #supprimer
                    break
                else:
                    if(s==1): #1 jour
                        Nforfait="Forfait_"+str(s)+"Jour"
                        duree = s  # "24h"
                        prix = 150
                        sms = "Illimite vers meme operateur"
                        appel = "Illimite vers meme operateur et 300DA vers les autres reseaux"
                        Volume_Internet = 2
                    if(s==15): #15 jours
                        Nforfait = "Forfait_" + str(s)+"Jours"
                        duree = s  #15 jours
                        prix = 500
                        sms = "Illimite vers meme operateur"
                        appel = "Illimite vers meme operateur et 750DA vers les autres reseaux"
                        Volume_Internet = 3
                    if(s==20): #20 jours
                        Nforfait="Forfait_"+str(s)+"Jours"
                        duree = s  #20 jours
                        prix = 700
                        sms = "Illimite vers meme operateur"
                        appel = "Illimite vers meme operateur et 1000DA vers autres reseaux"
                        Volume_Internet = 5

            forfait = {
                "Nom_Forfait": Nforfait,
                "Date_Achat_Forfait": Date_Achat_Forfait,
                "Date_Fin_Forfait": Date_Fin_Forfait,
                "Duree_Forfait": duree,
                "Prix_Forfait": prix,
                "SMS": sms,
                "Appel": appel,
                "Volume_Internet": Volume_Internet,
            }
            Forfaits.append(forfait)
    return Forfaits




#forfait entreprise

def _ListeForfaitEntreprise(Date_Debut_Contrat, dfin):
    c = fake.random_choices(elements=OrderedDict([("Aucun_forfait", 0.10), ("m", 0.75), ("j", 0.15)]), length=1)[0]
    if (c == "Aucun_forfait"):
        print("Aucun forfait")
        return None
    else:
        Forfaits=[]
        annees=_differenceDate(dfin, Date_Debut_Contrat)

        print(annees)
        if(annees==0):
            y = randint(2, 5)
        else:
            y=randint(5,25)*annees #nbr forfaits à generer pr une entreprise par annee

        for i in range(1, y):
            Choix = fake.random_choices(elements=OrderedDict([("m", 0.80), ("j", 0.20)]), length=1)[0]  # choisir forfait par mois ou jours
            if (Choix == "m"):  # si forfait par mois
                Date_Achat_Forfait = _dateEntre(Date_Debut_Contrat, dfin)
                s = randint(1, 8)  # un forfait de 1 mois , 2 mois ... 12 mois (max)
                Date_Fin_Forfait = _DateFinForfait(Date_Achat_Forfait, s, 0)
                if (_CompareTwoDates(Date_Fin_Forfait, dfin) == 1):  # supprimer

                    break
                else:
                    if(s==1):# 1mois
                        Nforfait="Forfait_"+str(s)+"Mois"
                        duree = s
                        prix = 1000
                        sms = "Illimite vers meme operateur"
                        appel = "Illimite vers meme operateur et 1500DA vers les autres reseaux"
                        Volume_Internet = 15 #15 GO
                    if(s==2):
                        Nforfait="Forfait_"+str(s)+"Mois"
                        duree = s # 2mois
                        prix = 1600
                        sms = "Illimite vers meme operateur"
                        appel = "Illimite vers meme operateur et 2000DA vers les autres reseaux"
                        Volume_Internet = 20
                    if(s==3):
                        Nforfait="Forfait_"+str(s)+"Mois"
                        duree = s  # 3mois
                        prix = 2000
                        sms = "Illimite vers meme operateur"
                        appel = "Illimite vers meme operateur et 2500DA vers les autres reseaux"
                        Volume_Internet = 25
                    if (s == 4):
                        Nforfait="Forfait_"+str(s)+"Mois"
                        duree = s # 4mois
                        prix = 2500
                        sms = "Illimite vers meme operateur"
                        appel = "Illimite vers meme operateur et 3000DA vers les autres reseaux"
                        Volume_Internet = 20
                    if (s == 5):
                        Nforfait="Forfait_"+str(s)+"Mois"
                        duree = s # 5mois
                        prix = 3000
                        sms = "Illimite vers meme operateur"
                        appel = "Illimite vers meme operateur et 3500DA vers les autres reseaux"
                        Volume_Internet = 30
                    if (s == 6):
                        Nforfait="Forfait_"+str(s)+"Mois"
                        duree = s # 6mois
                        prix = 4000
                        sms = "Illimite vers meme operateur"
                        appel = "Illimite vers meme operateur et 4000DA vers les autres reseaux"
                        Volume_Internet = 35
                    if (s == 7):  # forfait 8 mois
                        Nforfait = "Forfait_8 Mois"
                        duree = s  # 8mois
                        prix = 4500
                        sms = "Illimite vers meme operateur"
                        appel = "Illimite vers meme operateur et 4000DA vers les autres reseaux"
                        Volume_Internet = 30
                    if (s == 8):  # pour le forfait de 12 mois
                        Nforfait = "Forfait_12 Mois"
                        duree = s  # 12mois
                        prix = 6000
                        sms = "Illimite vers meme operateur"
                        appel = "Illimite vers meme operateur et 5000DA vers les autres reseaux"
                        Volume_Internet = 30

            else:  # forfait par jours

                Date_Achat_Forfait = _dateEntre(Date_Debut_Contrat, dfin)
                s = fake.random_choices(elements=OrderedDict([(1, 0.60), (15, 0.40), (20, 0.40)]), length=1)[0]
                Date_Fin_Forfait = _DateFinForfait(Date_Achat_Forfait, 0, s)
                if (_CompareTwoDates(Date_Fin_Forfait, dfin) == 1):  # supprimer
                    break
                else:
                    if(s==1): #1 jour
                        Nforfait="Forfait_"+str(s)+"Jour"
                        duree = s  # "24h"
                        prix = 150
                        sms = "Illimite vers meme operateur"
                        appel = "Illimite vers meme operateur et 300DA vers les autres reseaux"
                        Volume_Internet = 2
                    if(s==15): #15 jours
                        Nforfait = "Forfait_" + str(s)+"Jours"
                        duree = s  #15 jours
                        prix = 500
                        sms = "Illimite vers meme operateur"
                        appel = "Illimite vers meme operateur et 750DA vers les autres reseaux"
                        Volume_Internet = 3
                    if(s==20): #20 jours
                        Nforfait="Forfait_"+str(s)+"Jours"
                        duree = s  #20 jours
                        prix = 700
                        sms = "Illimite vers meme operateur"
                        appel = "Illimite vers meme operateur et 1000DA vers autres reseaux"
                        Volume_Internet =5

            forfait = {
                "Nom_Forfait": Nforfait,
                "Date_Achat_Forfait": Date_Achat_Forfait,
                "Date_Fin_Forfait": Date_Fin_Forfait,
                "Duree_Forfait": duree,
                "Prix_Forfait": prix,
                "SMS": sms,
                "Appel": appel,
                "Volume_Internet": Volume_Internet,
            }
            Forfaits.append(forfait)
    return Forfaits







#Generer services pour particulier (internet,appel,sms)
def _GenererHeure():
    date= fake.date_time_between('-2y', 'now')
    date=str(date)
    date= date.split(" ")
    return (date[1])

def _differenceDate(d1, d2):
    date = str(d1).split("-")
    y = int(date[0])
    #print(y)

    date2 = str(d2).split("-")
    y2 = int(date2[0])
    #print(y2)

    if (_CompareTwoDates(d1, d2) == -1):
        r = y2 - y
    if (_CompareTwoDates(d1, d2) == 1):
        r = y - y2
    else: #0
        r=0
    return r





#Generer des antennes

def _GenererTypeAntenne():
    return fake.random_choices(elements=OrderedDict((("4G", 0.39), ("3G", 0.32),("2G", 0.29))), length=1)[0]

"""
def _Nbr_Antennes_4G(): #LTE
    return randint(21796,27971)

def _Nbr_Antennes_3G(): #UMTS
    return randint(21913,27977)

def _Nbr_Antennes_2G(): #GSM
    return randint(377,20546)
"""




def _Frequence_Antenne():
    listeFreq= [700 , 800, 1800 , 2100, 2600 ] #en MHz
    r=randint(0,4)
    return listeFreq[r]

"""plus la freq utilisee est basse , plus le signal porte loin et mieux il traverse les murs des habitations
 les operateurs privilegient l'utilisation des bandes de 700MHz et 800MHz, afin de couvrir plus facilement les zones rurales """

def _ville(wilaya):
    r=randint(1,8)
    ville="Ville_"+str(r)+"_"+wilaya[0:4]
    return ville

def Raison_Resiliation():
   Raison  = fake.random_choices(elements=OrderedDict([("Demande", 0.45), ("Inactivite", 55)]), length=1)[0]
   return Raison


def _CompareTwoDates(d1,d2):  #retourne 0 si date d1== date d2 ,  1: si d1>d2 ,   -1 si d1<d2
    d1=str(d1)
    #print("d1:" , d1)

    d2=str(d2)
    #print("d2:", d2)
    comp=0

    da1= d1.split("-")
    year1=int(da1[0])
    month1=int(da1[1])
    day1=int(da1[2])

    da2 = d2.split("-")
    year2 = int(da2[0])
    month2 = int(da2[1])
    day2 = int(da2[2])

    if(year1<year2):
       comp=-1
    elif(year1>year2):
       comp=1
    else:
        if(year1==year2):
            if(month1<month2):
                comp=-1
            elif(month1>month2):
                comp=1
            else:
             if(month1==month2):
                if(day1<day2):
                    comp=-1
                elif(day1>day2):
                    comp=1
                else:
                    comp=0   #si d1 == d2
    #print(comp)
    return comp


def _Generedateinf(d1,y): #generer une date inferieure à d1
    da1= d1.split("-")
    year1=int(da1[0])
    month1=int(da1[1])
    day1=int(da1[2])

    year2 = year1 - y
    month2=randint(1,12)
    day2=randint(1,29)
    return str(year2)+"-"+str(month2)+"-"+str(day2)




def _dateEntre(d1,d2):     #date entre d1 et d2  (d1 et d2 sont des string sous forme "yyyy-mm-jj"
    if(_CompareTwoDates(d1,d2)==-1):
        start=d1
        end=d2
    else:
        start=d2
        end=d1

    a = radar.random_datetime(start, end)
    a = str(a).split(" ")
    return a[0]


#generer publications
def _GenerePublication(date):
    Publications=[]
    y = randint(2, 5)
    for i in range(1, y):
        appreciation = fake.random_choices(elements=OrderedDict(((1, 0.33), (2, 0.45), (3, 0.22), (4, 0.12), (5, 0.08))), length=1)
        choices = {

            1: "tres_mauvaise",
            2: "mauvaise",
            3: "Moyenne",
            4: "Tres_Bonne",
            5: "Excellente",
        }
        comments=randint(0, 12)
        likes=randint(0, 100)
        if (likes==0):
            partages=0
        else:
            partages=randint(1, 100)


        publication = {
            "Caractere" : choices[appreciation[0]],
            "Date_Publ": date,
            "Nbr_Comments" : comments,
			"Nbr_likes" : likes,
			"Nbr_Partages" : partages,
             }
        Publications.append(publication)

    return Publications



#calcule de la note avis a partir des publications
def _noteglobalepublication(publ):
    y = len(publ)
    note = 0
    dict = {'tres_mauvaise': 1, 'mauvaise': 2, 'Moyenne': 3, 'Tres_Bonne': 4, 'Excellente': 5}
    for i in range(y):
        note = note + int(dict[publ[i]["Caractere"]])

    note = int(note / y)
    return note





def _Categorie_Abonne(resil,DerniereDate,Anciennete):
  #print("Derniere Date entre la derniere  date  de fin_forfait et la derniere date de service utilisé " ,DerniereDate)
  #print("Anciennete" ,Anciennete)
  Date_now = datetime.today().strftime('%Y-%m-%d')
  Difference_En_Jours = days_diff(DerniereDate,Date_now)
  if(resil==1): #si resilie => Inactif
        categ="Inactif"
  else :

        if(Anciennete>=6): #si 6ans ou plus d'anciennete
            if(Difference_En_Jours<=50):
               categ = "Fidele"
            elif(Difference_En_Jours>=51 and Difference_En_Jours<60):
                categ = "tres_Actif"
            elif (Difference_En_Jours >= 61 and Difference_En_Jours < 69):
                categ = "Actif"
            elif (Difference_En_Jours >= 70 and Difference_En_Jours < 100):
                categ = "Moyen"
            else:
                categ = "Inactif"

        elif(Anciennete==5 or Anciennete==4 ):
            if (Difference_En_Jours<=50):
                categ = "Fidele"
            elif (Difference_En_Jours>=51 and Difference_En_Jours<70):
                categ = "tres_Actif"
            elif (Difference_En_Jours >= 71 and Difference_En_Jours < 79):
                categ = "Actif"
            elif(Difference_En_Jours >= 80 and Difference_En_Jours < 100):
                categ = "Moyen"
            else:
               categ = "Inactif"

        elif(Anciennete==3 or Anciennete==2):
            if (Difference_En_Jours<=40):
                categ = "Fidele"
            elif (Difference_En_Jours>=41 and Difference_En_Jours<60):
                categ = "tres_Actif"
            elif (Difference_En_Jours >= 61 and Difference_En_Jours < 70):
                categ = "Actif"
            elif(Difference_En_Jours >= 71 and Difference_En_Jours < 100):
                categ = "Moyen"
            else:
                categ = "Inactif"

        elif (Anciennete<=1 ):
            if(Difference_En_Jours<=30):
                categ = "tres_Actif"
            elif (Difference_En_Jours >= 31 and Difference_En_Jours < 50):
                categ = "Actif"
            elif (Difference_En_Jours >= 51 and Difference_En_Jours < 80):
                categ = "Moyen"
            else:
                categ = "Inactif"

  print(resil)
  print(categ)
  return categ




def _GeneretypeServ():
    return fake.random_choices(elements=OrderedDict((("Aucun_Service", 0.10),("Internet", 0.45), ("Appel", 0.30), ("SMS", 0.15))), length=1)[0]

def _GenererServiceParticulier(Date_Debut_Contrat, dfin):

      TypeService=fake.random_choices(elements=OrderedDict((("Internet", 0.25), ("Appel", 0.45), ("SMS", 0.30))), length=1)[0]
      Date_Service =_dateEntre(Date_Debut_Contrat, dfin)
      Heure_Serv = _GenererHeure()

      if(TypeService=="Internet"):
         Nom_Service="DISPATCH_INTERNET"
         Description_Service="Acheter et ou transferer des volumes internet entre les lignes de votre entreprise (" \
                             "meme flotte) "


      elif(TypeService=="Appel"):
         Nom_Service="APPELS_GRATUITS_ENTRE_COLLABORATEURS"
         Description_Service="Un service qui permet de profiter des appels gratuits en national  7j/7 de 8h vers 18h ou " \
                             "24h/24 entre un groupe de collaborateurs de la meme entreprise ou de la meme flotte "

      else: #SMS
          Nom_Service = "3awdli"
          Description_Service ="Le service 3awedli  permet aux clients de l operateur ayant un credit insuffisant pour " \
                               "effectuer un appel de solliciter leurs proches en leur envoyant des SMS gratuits. Le " \
                               "client sollicite sera notifie par SMS lui indiquant le numero du demandeur !"

      Service =	{
				"Date_Service": Date_Service,
                "Heure_Service": Heure_Serv,
                "Type_Service":TypeService,
                "Nom_Service":Nom_Service,
				"Description_Service":Description_Service,
				}
      return Service




#Generer services pour Entreprise (internet,appel,sms)
def _GenererServiceEntreprise(Date_Debut_Contrat, dfin):
    TypeService =fake.random_choices(elements=OrderedDict((("Internet", 0.15), ("Appel", 0.75), ("SMS", 0.10))), length=1)[0]
    Date_Service = _dateEntre(Date_Debut_Contrat, dfin)
    Heure_Serv= _GenererHeure()

    if (TypeService == "Internet"):
        Nom_Service = "DISPATCH_INTERNET"
        Description_Service = "Acheter et ou transferer des volumes internet entre les lignes de votre entreprise (" \
                              "meme flotte) "


    elif (TypeService == "Appel"):
        Nom_Service = "APPELS_GRATUITS_ENTRE_COLLABORATEURS"
        Description_Service = "Un service qui permet de profiter des appels gratuits en national  7j/7 de 8h à 18h ou " \
                              "24h/24 entre un groupe de collaborateurs de la meme entreprise ou de la meme flotte "

    else:  # SMS
        Nom_Service = "3awdli"
        Description_Service = "Le service 3awedli permet aux clients de l operateur ayant un credit insuffisant pour " \
                              "effectuer un appel de solliciter leurs proches en leur envoyant des SMS gratuits. Le " \
                              "client sollicite sera notifie par SMS lui indiquant le numero du demandeur "

    Service = {
        "Date_Service": Date_Service,
        "Heure_Service": Heure_Serv,
        "Type_Service": TypeService,
        "Nom_Service": Nom_Service,
        "Description_Service": Description_Service,
       }
    return Service

def _GenererListeServicesParticulier(Date_Debut_Contrat, dfin):
    TypeService = _GeneretypeServ()
    if (TypeService == "Aucun_Service"):#si l'abonne n'a utilisé aucun service on retourne null
        return None #liste vide
    else:  #si l'abonne a utilisé des services ....
        Services = []
        annees=_differenceDate(dfin, Date_Debut_Contrat)

        if(annees==0):
            y = randint(2, 10)
        else:
            y=randint(2,40)*annees #nbr services à generer pr un abonné par annee

        Nbr_Services=y

        for i in range(0, Nbr_Services):
            Service=_GenererServiceParticulier(Date_Debut_Contrat, dfin)
            Services.append(Service)
        return Services


def _GenererListeServicesEntreprise(Date_Debut_Contrat, dfin):
    TypeService = _GeneretypeServ()
    if (TypeService == "Aucun_Service"):#si l'abonne n'a utilisé aucun service on retourne null
        return None #liste vide
    else:  #si l'abonne a utiliser des services ....
        Services = []
        annees=_differenceDate(dfin, Date_Debut_Contrat)

        if(annees==0):
            y = randint(2, 5)
        else:
            y=randint(2,40)*annees #nbr services à generer pr un abonné par annee

        Nbr_Services=y
        for i in range(0, Nbr_Services):
            Service=_GenererServiceEntreprise(Date_Debut_Contrat, dfin)
            Services.append(Service)
        return Services




# tri par date achat forfait
def fctSortDict(value):
    return value['Date_Achat_Forfait']  # fct pour le tri


# tri par date services
def SortDatesServices(value):
    return value['Date_Service']



def absentiesme_Employe(Date_Debut_Travail,Date_Fin):
    c= fake.random_choices(elements=OrderedDict([("Aucune_Absence", 0.65),("Absences", 0.35),]), length=1)[0]
    if(c=="Aucune_Absence"):
        #print("Aucune_Absence")
        return None

    else:
        list=[]
        Raisons = {
            1: "Maladie professionelle.",
            2: "Stress professionelle.",
            3: "Accident de travail.",
            4: "Mauvaise ambiance de travail ",
            5: "Mauvaises conditions de travail.",
        }
        r=randint(1,13)
        for i in range(1, r):
           cause = fake.random_choices(elements=OrderedDict(((1, 0.20), (2, 0.15), (3, 0.25), (4, 0.20), (5, 0.20))),
                                        length=1)

           Date_Absence = _dateEntre(Date_Debut_Travail, Date_Fin)


           abs= {
                 "Date_Absence":Date_Absence,
                 "Raison": Raisons[cause[0]],
                }
           list.append(abs)
        """for i in list:
            print(i)"""
    return list

def _DataCenter(DateCreationOperateur):
    ListEnerg ={}
    for an in range(2014, 2023):
        ListEnerg.update({str(an): randint(50,90)}) # en TWh/an
    dateToday = datetime.today() \
        .strftime('%Y-%m-%d')
    Date_Installation_DataCenter = _dateEntre(DateCreationOperateur, dateToday)
    Wilaya = _Generer_Adresse()

    Centre_de_Donnees = {
        "Date_Installation": Date_Installation_DataCenter,
         "Consom_Energitique": ListEnerg,
        "Wilaya": Wilaya,
        "capacite_Stockage": randint(23,26) , #les  data-centers peuvent gérer jusqu’à 26 TB (soit 26 000 GB) de données. ,
    }
    return Centre_de_Donnees

myclient.close()