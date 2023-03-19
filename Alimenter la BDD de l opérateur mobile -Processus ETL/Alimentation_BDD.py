import csv
from collections import OrderedDict
from json import load
from random import randint

from main import myclient, _GenererPrefixOper, fake
from main import _DataCenter




def Alimenter_Employe():
    ListEmployees=[]
    with open("External_Files/File_Employees.csv", "r") as File_Employee:
        """fichier = csv.reader(File_Employee)
        header=next(fichier)"""

        f= csv.DictReader(File_Employee)

        Empl = {
            "idEmploye": 1,
            "Employe_Prenom": "Julie",
            "Employe_Nom": "Jean",
            "Date_Naissance": "1990-06-19",
            "Date_Debut_Travail": "2015-04-10",
            "Date_Demission": "2018-02-28",
            "Salaire": 89474,
            "Avis_Employe": {
                "Date_Avis": "2016-04-11",
                "Avis_Rating": 3
            },
            "Nbr_Taches_Accomplies_a_Temps": 42,
            "Nbr_Taches_Non_Accomplies": 9,
            "Absences": [
                {
                    "Date_Absence": "2017-10-19",
                    "Raison": "Maladie professionelle."
                },
                {
                    "Date_Absence": "2015-04-12",
                    "Raison": "Maladie professionelle."
                },
                ]
        }

        ListEmployees.append(Empl)


        for row in f:
            with open("External_Files/File_Absences.csv", "r") as File_Absences:
                f2 = csv.DictReader(File_Absences)
                List=[]
                a = 0
                for row2 in f2:
                    if(int(row2['Id_Employee'])==int(row['id'])):
                        a=1
                        abs= {
                            "Date_Absence":row2['Date_Absence'],
                            "Raison":row2['Raison']
                        }
                        List.append(abs)
                    if(a==1 and row2['Id_Employee']!=row['id']) :
                        break
                if(a==0):
                    List=None
                if(row['Date_Depart'] == "" or  row['Date_Depart'] == "null" ):
                   p=None
                else:
                   p= row['Date_Depart']


                Employe = {
                        "idEmploye":int(row['id']),
                        "Employe_Prenom": row['Prenom'],
                        "Employe_Nom": row['Nom'] ,
                        "Date_Naissance":row['Date_Naissance'] ,
                        "Date_Debut_Travail": row['Date_Debut_Travail'],
                        "Date_Demission": p,
                        "Salaire": int(row['Salaire']),
                        "Avis_Employe": {
                            "Date_Avis": row['Date_Avis'],
                            "Avis_Rating": int(row['Avis_Rating']),
                        },
                        "Nbr_Taches_Accomplies_a_Temps": int(row['Nbr_Taches_Accomplies_a_Temps']),
                        "Nbr_Taches_Non_Accomplies": int(row['Nbr_Taches_Non_Accomplies']),
                        "Absences": List,
                  }
                ListEmployees.append(Employe)
    File_Employee.close()
    return ListEmployees


def Alimenter_Antenne():
    List=[]
    with open("External_Files/File_Antenne.csv", "r") as File_Antenne:
        f= csv.DictReader(File_Antenne)

        for row in f:

            Antenne = {
                "Type_Antenne": row['Type'],
                "Date_Installation": row['Date_Installation'],
                "Frequence": int(row['Frequence']),
                "Region":
                    {
                        "Nom_Wilaya": row['Wilaya'],
                        "Nom_Ville": row['Ville'],
                    }
            }
            List.append(Antenne)
    File_Antenne.close()
    """for j in List:
            print(j)"""

    return List



def Alimenter_Concurrents():
    with open("External_Files/File_Competitors.json", "r") as File_c:
        data=load(File_c)
    File_c.close()
    return data

def Alimenter_abonnes():
    List=[]
    with open("External_Files/File_Particuliers.json", "r") as File_part:
        data1=load(File_part)

    with open("External_Files/File_companies.json", "r") as File_entrep:
        data2=load(File_entrep)

        part = {
            "idPart": 1,
            "Numero_Tel": "0758302281",
            "Type_Client": "Particulier",
            "Categorie_Client": "tres_Actif",
            "Client_Prenom": "Marcel",
            "Client_Nom": "Alves",
            "Adresse": "Naama",
            "Date": "2002-07-04",
            "CA": 17850,
            "Contrat": {
                "Num_contrat": "P471997",
                "Date_Debut_Contrat": "2020-01-24"
            },
            "Service": [
                {
                    "Date_Service": "2022-05-15",
                    "Heure_Service": "01:41:13",
                    "Type_Service": "Appel",
                    "Nom_Service": "APPELS_GRATUITS_ENTRE_COLLABORATEURS",
                    "Description_Service": "Un service qui permet de profiter des appels gratuits en national  7j/7 de 8h vers 18h ou 24h/24 entre un groupe de collaborateurs de la meme entreprise ou de la meme flotte "
                }
            ],

            "Forfaits": [
                {
                    "Nom_Forfait": "Forfait_4Mois",
                    "Date_Achat_Forfait": "2018-04-09",
                    "Date_Fin_Forfait": "2018-8-9",
                    "Duree_Forfait": 4,
                    "Prix_Forfait": 2500,
                    "SMS": "Illimite vers meme operateur",
                    "Appel": "Illimite vers meme operateur et 3000DA vers les autres reseaux",
                    "Volume_Internet": "20"
                }],
            "Reclamation": [
                {
                    "Date_Call": "2021-09-19",
                    "Descripition-Reclamation": "Coupures de l acces internet (mauvaise qualite du reseau internet).",
                    "Answered": 0,
                    "Resolved": 0,
                    "Speed_of_Answer": 51,
                    "Avg_Call_Duration": "00:06:21",
                    "Satisfaction_rating": 3
                }],
            "Avis_Abonne": {
                "Date_Avis": "2017-06-27",
                "Avis_Rating": 3,
            },
            "Resiliation": {
                "Date_Resiliation": "2021-10-08",
                "Raison_Resiliation": "Demande",
            },

            "Reseau_Social_Operateur": {
                "Nom_Reseau": "Facebook",
                "Publication": [
                    {
                        "Caractere": "Excellente",
                        "Date_Publ": "2020-06-30",
                        "Nbr_Comments": 1,
                        "Nbr_likes": 76,
                        "Nbr_Partages": 21
                    }
                ]
            }
        }
        List.append(part)
        for i in data1:
            with open("External_Files/File_services.csv", "r") as File_services:
                f = csv.DictReader(File_services)
                serv= []
                a = 0
                for row in f:
                    if (int(i['id'])!=int(row['Id_client'])):
                        pass
                    else:
                        a = 1
                        Service = {
                            "Date_Service": row['Date_Service'],
                            "Heure_Service": row['Heure_Service'],
                            "Type_Service": row['Type_Service'],
                            "Nom_Service": row['Nom_Service'],
                            "Description_Service": row['Description_Service'],
                        }
                        serv.append(Service)

                if (a == 0):
                    serv = None


                Particulier = {
                    "idPart": i['id'],
                    "Numero_Tel": i['Numero_Tel'],
                    "Type_Client": "Particulier",
                    "Categorie_Client": i['Categorie_Client'],
                    "Client_Prenom": i['Prenom'],
                    "Client_Nom": i['Nom'],
                    "Adresse": i['Adresse'],
                    "Date": i['Date'],
                    "CA": int(i['CA']),
                    "Contrat": {
                        "Num_contrat": i['Contrat']['Num_contrat'],
                        "Date_Debut_Contrat": i['Contrat']['Date_Debut_Contrat'],

                    },
                    "Service": serv,
                    "Forfaits": i['Forfaits'],
                    "Reclamation": i['Reclamation'],

                    "Avis_Abonne": {
                        "Date_Avis": i['Avis_Abonne']['Date_Avis'],
                        "Avis_Rating": i['Avis_Abonne']['Avis_Rating'],
                    },
                    "Resiliation": {
                        "Date_Resiliation": i['Resiliation']['Date_Resiliation'],
                        "Raison_Resiliation": i['Resiliation']['Raison_Resiliation'],
                    },
                    "Reseau_Social_Operateur":
                        {
                            "Nom_Reseau": i['Reseau_Social_Operateur']['Nom_Reseau'],
                            "Publication": i['Reseau_Social_Operateur']['Publication'],
                        },
                }
                List.append(Particulier)






        for i in data2:

            with open("External_Files/File_services.csv", "r") as File_services:
                f = csv.DictReader(File_services)
                serv= []
                a = 0
                for row in f:
                    if (int(i['idEntr'])!=int(row['Id_client'])):
                        pass
                    else:
                        a = 1
                        Service = {
                            "Date_Service": row['Date_Service'],
                            "Heure_Service": row['Heure_Service'],
                            "Type_Service": row['Type_Service'],
                            "Nom_Service": row['Nom_Service'],
                            "Description_Service": row['Description_Service'],
                        }
                        serv.append(Service)

                if (a == 0):
                    serv = None


                Entreprise = {
                    "idEntr": i['idEntr'],
                    "Numero_Tel": i['Numero_Tel'],
                    "Type_Client": "Entreprise",
                    "Categorie_Client": i['Categorie_Client'],
                    "Client_Prenom": None,
                    "Client_Nom": i['Client_Nom'],
                    "Adresse": i['Adresse'],
                    "Date": i['Date'],
                    "CA": int(i['CA']),
                    "Contrat": {
                        "Num_contrat": i['Contrat']['Num_contrat'],
                        "Date_Debut_Contrat": i['Contrat']['Date_Debut_Contrat'],

                    },
                    "Service": serv,
                    "Forfaits": i['Forfaits'],
                    "Reclamation": i['Reclamation'],

                    "Avis_Abonne": {
                        "Date_Avis": i['Avis_Abonne']['Date_Avis'],
                        "Avis_Rating": i['Avis_Abonne']['Avis_Rating'],
                    },
                    "Resiliation": {
                        "Date_Resiliation": i['Resiliation']['Date_Resiliation'],
                        "Raison_Resiliation": i['Resiliation']['Raison_Resiliation'],
                    },
                    "Reseau_Social_Operateur":
                        {
                            "Nom_Reseau": i['Reseau_Social_Operateur']['Nom_Reseau'],
                            "Publication": i['Reseau_Social_Operateur']['Publication'],
                        },
                }
                List.append(Entreprise)

        """for j in List:
         print(j)"""



    File_services.close()
    File_part.close()
    File_entrep.close()
    return List





#connexion à la BDD
def _Connection(NomCollection):
    Collection_Operateur = myclient.myNewDb.get_collection(NomCollection)
    return Collection_Operateur

Collection_Operateur=_Connection("OPERATEUR")

#Collection_Operateur.update_many( update_one
"""Collection_Operateur.update_many(
    {"$.Abonnes":{"idEntr":0}},
    {'$set': {"new111":"attribute_value"}})"""


def _Alimenter_Operateur():
    #prefixOper = _GenererPrefixOper()
    

    Operateur_Mobile = {

                "Operateur_Name": "SIL Mobile",
                "Prefix_Operateur": "07",
                "Abonnes":Alimenter_abonnes(),
                "Employés":Alimenter_Employe(),
                "Antenne": Alimenter_Antenne(),
                "Concurrent": Alimenter_Concurrents(),
                "Data_center": _DataCenter("2014-01-01"),
               }
    Collection_Operateur.insert_one(Operateur_Mobile)

