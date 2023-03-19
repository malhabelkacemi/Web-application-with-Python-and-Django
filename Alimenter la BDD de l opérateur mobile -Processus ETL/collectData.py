from datetime import datetime
import csv
from collections import OrderedDict
from itertools import islice
from random import randint

from faker import Faker
from _datetime import datetime
import json
from csv import DictWriter
from main import _Generer_Prenom, _Generer_Nom, _GenerateDateBetween, DateCreationOperateur, _dateEntre, \
    absentiesme_Employe, _Generer_Adresse, _GenererTypeAntenne, _Frequence_Antenne, _ville, _Gnererer_Answered_Resolved, \
    _Convert_Seconds, _Generer_Reclamation, _GenererNbrAbonnes, _GenerePublication, _ListeForfaitParticulier, \
    _differenceDate, _GenererListeServicesParticulier, _Categorie_Abonne, fctSortDict, SortDatesServices, \
    _CompareTwoDates, _GenererPhoneNumberParticulier, _GenerernumcontratP, _noteglobalepublication, Raison_Resiliation, \
    _GenererPrefixOper, _GenererListeServicesEntreprise, _GenerernumcontratE, _Generer_Nom_Entreprise

fake = Faker('fr_FR')

listAbsentiesme = []


def _Generer_Employes(idf):
    Date_now = datetime.today().strftime('%Y-%m-%d')

    l = randint(1, 1000)
    if (l <= 199):
        dateNaissance = _GenerateDateBetween('-26y', '-31y')

    if ((l >= 200) & (l <= 500)):
        dateNaissance = _GenerateDateBetween('-32y', '-40y')

    if ((l >= 501) & (l <= 800)):
        dateNaissance = _GenerateDateBetween('-41y', '-52y')

    if ((l >= 801) & (l <= 1000)):
        dateNaissance = _GenerateDateBetween('-53y', '-66y')

    demission = fake.random_choices(elements=OrderedDict([(1, 0.15), (0, 0.85)]), length=1)[
        0]  # retourner 1 si l'employé va démissionner sinon 0

    if (demission == 1):

        Date_Debut_Travail = _dateEntre(DateCreationOperateur, Date_now)
        Date_Demission = _dateEntre(Date_Debut_Travail, Date_now)
        Date_Avis = _dateEntre(Date_Debut_Travail, Date_Demission)
        listAbsences = absentiesme_Employe(Date_Debut_Travail, Date_Demission)

    else:
        Date_Debut_Travail = _dateEntre(DateCreationOperateur, Date_now)
        Date_Demission = None
        Date_Avis = _dateEntre(Date_Debut_Travail, Date_now)
        listAbsences = absentiesme_Employe(Date_Debut_Travail, Date_now)

    Satisf_Rating = \
    fake.random_choices(elements=OrderedDict([(1, 0.08), (2, 0.21), (3, 0.32), (4, 0.30), (5, 0.68)]), length=1)[0]

    try:
        if (listAbsences is not None):
            if (len(listAbsences) > 1):

                for j in listAbsences:
                    j.update({"Id_Employee": idf})  # pour garder l'id des clients dans le fichier externe service
                    listAbsentiesme.append(j)


    except Exception as e:
        print("Exception :", str(e))

    Employe = {
        "id": idf,
        "Prenom": _Generer_Prenom(),
        "Nom": _Generer_Nom(),
        "Date_Naissance": dateNaissance,
        "Date_Debut_Travail": Date_Debut_Travail,
        "Date_Depart": Date_Demission,
        "Salaire": randint(50000, 150000),
        "Date_Avis": Date_Avis,
        "Avis_Rating": Satisf_Rating,
        "Nbr_Taches_Accomplies_a_Temps": randint(2, 200),
        "Nbr_Taches_Non_Accomplies": randint(2, 30),

    }
    return Employe


def _GenererListeEmpl():
    idEmpl = 2
    List_Empl = []
    r = randint(200, 260)  # nbr d'employés
    for i in range(r):
        E = _Generer_Employes(idEmpl)
        List_Empl.append(E)
        idEmpl += 1

    return List_Empl


def _FichierCSV_Externe_Employees():
    data = _GenererListeEmpl()

    headersCSV = ['id', 'Prenom', 'Nom', 'Date_Naissance', 'Date_Debut_Travail', 'Date_Depart', 'Salaire', 'Date_Avis',
                  'Avis_Rating', 'Nbr_Taches_Accomplies_a_Temps', 'Nbr_Taches_Non_Accomplies']

    with open('External_Files/File_Employees.csv', 'w', newline='') as f_object:
        dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
        csv_writer = csv.writer(f_object, delimiter=',')
        csv_writer.writerow(headersCSV)
        for i in data:
            dictwriter_object.writerow(i)
    f_object.close()


def _AjouterDoublonsEmployes():
    n = 0
    with open("External_Files/File_Employees.csv", "r") as File_Employees:
        f2 = csv.DictReader(File_Employees)
        for row in f2:
            n = int(row['id'])
    # print(n)
    List_Empl = []

    with open("External_Files/File_Employees.csv", "r") as File_Employees:
        f2 = csv.DictReader(File_Employees)
        for row in islice(f2, 10):
            # print(row)
            row['id'] = int(n + 1)
            List_Empl.append(row)
            n += 1

    File_Employees.close()

    headersCSV = ['id', 'Prenom', 'Nom', 'Date_Naissance', 'Date_Debut_Travail', 'Date_Depart', 'Salaire', 'Date_Avis',
                  'Avis_Rating', 'Nbr_Taches_Accomplies_a_Temps', 'Nbr_Taches_Non_Accomplies']

    with open('External_Files/File_Employees.csv', 'a', newline='') as f_object:
        dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
        csv_writer = csv.writer(f_object, delimiter=',')

        for i in List_Empl:
            dictwriter_object.writerow(i)
    f_object.close()


def _FichierCSV_Externe_Absences():
    headersCSV = ['Id_Employee', 'Date_Absence', 'Raison']
    with open('External_Files/File_Absences.csv', 'w', newline='') as f_object:
        dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
        csv_writer = csv.writer(f_object, delimiter=',')
        csv_writer.writerow(headersCSV)
        for i in listAbsentiesme:
            dictwriter_object.writerow(i)
    f_object.close()


def _Antenne(DateCreationOperateur):
    dateToday = datetime.today() \
        .strftime('%Y-%m-%d')  # de type str
    Date_Inst_Antenne = _dateEntre(DateCreationOperateur, dateToday)
    Wilaya = _Generer_Adresse()
    # print("Date_Inst_Antenne", Date_Inst_Antenne)

    Antenne = {
        "Type": _GenererTypeAntenne(),  # 4G , 3G ,2G
        "Date_Installation": Date_Inst_Antenne,
        "Frequence": int(_Frequence_Antenne()),
        "Wilaya": Wilaya,
        "Ville": _ville(Wilaya),
    }
    return Antenne



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



def _ListeAntennes(DateCreationOperateur):
    Antennes = []
    Nbr_Antennes = randint(20796, 27971)
    for i in range(0, Nbr_Antennes):
        Antenne = _Antenne(DateCreationOperateur)
        Antennes.append(Antenne)

    return Antennes


def _FichierCSV_Externe_Antenne():
    data = _ListeAntennes(DateCreationOperateur)

    headersCSV = ['Type', 'Date_Installation', 'Frequence', 'Wilaya', 'Ville']

    with open('External_Files/File_Antenne.csv', 'w', newline='') as f_object:
        dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
        csv_writer = csv.writer(f_object, delimiter=',')
        csv_writer.writerow(headersCSV)
        for i in data:
            dictwriter_object.writerow(i)
    f_object.close()


def _ListeReclamation(Date_Debut_Contrat, dfin):
    nbr_reclam = fake.random_choices(
        elements=OrderedDict([(0, 0.30), (1, 0.15), (2, 0.17), (3, 0.16), (4, 0.13), (5, 0.42), (6, 0.05)]), length=1)[
        0]

    # print(nbr_reclam)
    if (nbr_reclam == 0):  # si y'a aucune reclamation
        return None
    else:
        Reclamation = []
        for i in range(1, nbr_reclam):
            a = _Gnererer_Answered_Resolved()
            if a == 0:  # answered = no AND resolved =no
                Answered = 0,
                Resolved = 0,
                speed = None
                Duration_Talk = None
                Satisf_Rating = None

            elif a == 10:  # answered = yes AND resolved =no
                Answered = 1,
                Resolved = 0,
                speed = randint(11, 125)  # seconds
                Duration_Talk = _Convert_Seconds(randint(32, 420))  # entre 32 sec et 420sec(7 min)
                if (speed <= 55):
                    Satisf_Rating = \
                    fake.random_choices(elements=OrderedDict([(1, 0.25), (2, 0.37), (3, 0.30), (4, 0.08)]), length=1)[0]
                else:
                    Satisf_Rating = \
                    fake.random_choices(elements=OrderedDict([(1, 0.25), (2, 0.45), (3, 0.22), (4, 0.08)]), length=1)[0]

            else:  # answered = yes AND resolved =yes
                Answered = 1,
                Resolved = 1,
                speed = randint(11, 125)  # seconds
                Duration_Talk = _Convert_Seconds(randint(32, 420))  # entre 32 sec et 420 sec(7 min)
                if (speed <= 55):
                    Satisf_Rating = \
                    fake.random_choices(elements=OrderedDict([(3, 0.18), (4, 0.44), (5, 0.58)]), length=1)[0]
                else:
                    Satisf_Rating = \
                    fake.random_choices(elements=OrderedDict([(2, 0.05), (3, 0.13), (4, 0.52), (5, 0.30)]), length=1)[0]

            if (Answered[0] == 0):
                ans = "No"
            else:
                ans = "Yes"

            if (Resolved[0] == 0):
                res = "No"
            else:
                res = "Yes"

            Recl = {
                "Date_Call": _dateEntre(Date_Debut_Contrat, dfin),
                "Descripition-Reclamation": _Generer_Reclamation(),
                "Answered": ans,
                "Resolved": res,
                "Speed_of_Answer": speed,
                "Avg_Call_Duration": Duration_Talk,
                "Satisfaction_rating": Satisf_Rating,
            }
            Reclamation.append(Recl)

    return Reclamation


data = []  # list service en commun entre entrep et particuliers


def _Generer_Particulier(pref, idf):
    Date_now = datetime.today().strftime('%Y-%m-%d')
    Date_Debut_Contrat = _dateEntre(DateCreationOperateur, Date_now)

    Date_Resiliation = _dateEntre(Date_Debut_Contrat, Date_now)

    resilier = fake.random_choices(elements=OrderedDict([(1, 0.20), (0, 0.80)]), length=1)[
        0]  # choisir si le particulier va resilier =1 ou pas =0

    if (
            resilier == 1):  # si plus tard l entreprise decide de resilie => ON LUI associe le type de raison de cette resiliation (raison d'inactivite ou par demande)
        resil = 1
        dfin = Date_Resiliation
        RaisonResiliation = Raison_Resiliation()
        catg = "Inactif"
        # print("resil : ", resil)
        d = _dateEntre(Date_Debut_Contrat, dfin)
        pub = _GenerePublication(d)  # pour passer pub en argument pour calculer la note

    else:  # dans le cas ou y a pas de resiliation => ni une date ni une raison de resiliation
        resil = 0
        # print("resil : ", resil)
        dfin = Date_now
        Date_Resiliation = None
        RaisonResiliation = None
        catg = "Moyen"
        d = _dateEntre(Date_Debut_Contrat, dfin)
        pub = _GenerePublication(d)  # pour passer pub en argument pour calculer la note

    Date_Avis = _dateEntre(Date_Debut_Contrat, dfin)
    testf = _ListeForfaitParticulier(Date_Debut_Contrat, dfin)
    serv = _GenererListeServicesParticulier(Date_Debut_Contrat, dfin)

    anciennete = _differenceDate(dfin, Date_Debut_Contrat)

    try:
        if (serv is not None):
            if (len(serv) > 1):

                for j in serv:
                    j.update({"Id_client": idf})  # pour garder l'id des clients dans le fichier externe service
                    data.append(j)


    except Exception as e:
        print("Exception :", str(e))

    # cas ou y a des forfaits mais aucun service
    if ((testf is not None) and (len(testf) >= 2) and (serv is None)):

        Nbr_offres_Achetes = len(testf)
        # print("forfait nbr: ", Nbr_offres_Achetes)
        testf = sorted(testf, key=fctSortDict, reverse=False)

        Date_Dernier_Fin_Forfait = testf[-1]['Date_Fin_Forfait']
        # print("Date_Dernier_Fin_Forfait :", Date_Dernier_Fin_Forfait)
        catg = _Categorie_Abonne(resil, Date_Dernier_Fin_Forfait, anciennete)


    # cas ou y a des services mais aucun forfait
    elif ((serv is not None) and (len(serv) >= 2) and (testf is None)):

        # Nbr_services = len(serv)
        # print("nbr service : ", Nbr_services)
        serv = sorted(serv, key=SortDatesServices, reverse=False)

        Date_Dernier_Service = serv[-1]['Date_Service']
        # print("Date_Dernier_Service", Date_Dernier_Service)
        catg = _Categorie_Abonne(resil, Date_Dernier_Service, anciennete)
        # print("catg : ", catg)

    # cas ou y a des forfaits et des services
    elif ((testf is not None) and (
            len(testf) >= 2)):  # le tri se fait uniquement si l'abonne a achete au moins deux forfaits

        # Nbr_offres_Achetes = len(testf)
        # print("nbr forf : ",Nbr_offres_Achetes)
        testf = sorted(testf, key=fctSortDict, reverse=False)

        Date_Dernier_Fin_Forfait = testf[-1]['Date_Fin_Forfait']
        # print("Date_Fin_Forfait", Date_Dernier_Fin_Forfait)
        if ((serv is not None) and (len(serv) >= 2)):

            # Nbr_services = len(serv)
            # print("nbr service : ", Nbr_services)
            serv = sorted(serv, key=SortDatesServices, reverse=False)
            Date_Dernier_Service = serv[-1]['Date_Service']
            # print("Date_Dernier_Service", Date_Dernier_Service)

            if ((Date_Dernier_Service is not None) and (Date_Dernier_Service is not None)):

                if (_CompareTwoDates(Date_Dernier_Fin_Forfait,
                                     Date_Dernier_Service) == -1):  # si Date_Dernier_Fin_Forfait<Date_Dernier_Service
                    catg = _Categorie_Abonne(resil, Date_Dernier_Service, anciennete)
                    # print("catg : ", catg)

                else:
                    catg = _Categorie_Abonne(resil, Date_Dernier_Fin_Forfait, anciennete)
                    # print("catg : ", catg)

    elif ((testf is None) and (serv is None)):  # aucun forfait et aucun service
        DerniereDate = "2018-02-18"
        catg = _Categorie_Abonne(resil, DerniereDate, anciennete)

    l = randint(1, 1000)
    # print(l)
    if (l <= 50):
        date = _GenerateDateBetween('-18y', '-19y')
        ca = randint(1000, 40000)

    if ((l >= 51) & (l <= 190)):
        date = _GenerateDateBetween('-20y', '-24y')  # pour les particuliers agés entre 20 ans et 24 ans
        ca = randint(36000, 46000)

    if ((l >= 191) & (l <= 320)):
        date = _GenerateDateBetween('-25y', '-29y')
        ca = randint(40000, 58000)

    if ((l >= 321) & (l <= 430)):
        date = _GenerateDateBetween('-30y', '-34y')
        ca = randint(50000, 62000)

    if ((l >= 431) & (l <= 520)):
        date = _GenerateDateBetween('-35y', '-39y')
        ca = randint(58000, 66000)

    if ((l >= 521) & (l <= 600)):
        date = _GenerateDateBetween('-40y', '-44y')
        ca = randint(64000, 73000)

    if ((l >= 601) & (l <= 695)):
        date = _GenerateDateBetween('-45y', '-49y')
        ca = randint(67000, 75000)

    if ((l >= 696) & (l <= 785)):
        date = _GenerateDateBetween('-50y', '-54y')
        ca = randint(50000, 68000)

    if ((l >= 786) & (l <= 855)):
        date = _GenerateDateBetween('-55y', '-59y')
        ca = randint(44000, 54000)

    if ((l >= 856) & (l <= 905)):
        date = _GenerateDateBetween('-60y', '-64y')
        ca = randint(40000, 50000)

    if ((l >= 906) & (l <= 950)):
        date = _GenerateDateBetween('-65y', '-69y')
        ca = randint(9500, 13000)

    if ((l >= 951) & (l <= 1000)):
        date = _GenerateDateBetween('-70y', '-77y')
        ca = randint(8500, 12000)

    SumForfait = 0
    if (testf is not None):
        for i in testf:
            SumForfait = SumForfait + int(i["Prix_Forfait"])

    ca = ca + SumForfait

    c = randint(0, 2)
    if (c == 0):
        ca = str(ca) + " Dinars"
    elif (c == 1):
        ca = str(ca) + " dinars"
    else:
        ca = str(ca) + " Dinars_Algeriens"

    if (l < 200):
        Situation_familiale = fake.random_choices(
            elements=OrderedDict([("celibataire", 0.70), ("marie sans enfant", 0.20), ("marié avec enfant(s)", 0.10)]),
            length=1)[0]

    else:
        Situation_familiale = fake.random_choices(elements=OrderedDict(
            [("celibataire", 0.15), ("marie sans enfant", 0.35), ("marié avec enfant(s)", 0.40), ("divorcé", 0.10)]),
                                                  length=1)[0]

    Particulier = {
        "id": idf,
        "Numero_Tel": _GenererPhoneNumberParticulier(pref),
        "Categorie_Client": catg,
        "Prenom": _Generer_Prenom(),
        "Nom": _Generer_Nom(),
        "Adresse": _Generer_Adresse(),
        "Date": date,
        "CA": ca,
        "Situation_familiale": Situation_familiale,
        "professionClient": fake.job(),
        "lieu_Travail": _Generer_Adresse(),
        "Contrat": {
            "Num_contrat": _GenerernumcontratP(),
            "Date_Debut_Contrat": Date_Debut_Contrat,

        },
        "Forfaits": testf,
        "Reclamation": _ListeReclamation(Date_Debut_Contrat, dfin),
        "Avis_Abonne": {
            "Date_Avis": Date_Avis,
            "Avis_Rating": _noteglobalepublication(pub),
        },
        "Resiliation": {
            "Date_Resiliation": Date_Resiliation,
            "Raison_Resiliation": RaisonResiliation,
        },
        "Reseau_Social_Operateur":
            {
                "Nom_Reseau": "Facebook",
                "Publication": pub,
            },
    }

    return Particulier


# Entreprise
def _Generer_Entreprise(pref, idf):
    # print("Entreprise")
    Date_now = datetime.today().strftime('%Y-%m-%d')
    Date_Debut_Contrat = _dateEntre(DateCreationOperateur, Date_now)

    Date_Resiliation = _dateEntre(Date_Debut_Contrat, Date_now)

    resilier = fake.random_choices(elements=OrderedDict([(1, 0.40), (0, 0.60)]), length=1)[
        0]  # choisir: si resilier =1 ou pas =0

    if (
            resilier == 1):  # si plus tard l entreprise decide de resilie => ON LUI associe le type de raison de cette resiliation (raison d'inactivite ou par demande)
        resil = 1
        dfin = Date_Resiliation
        RaisonResiliation = Raison_Resiliation()
        d = _dateEntre(Date_Debut_Contrat, dfin)
        pub = _GenerePublication(d)  # pour passer pub en argument pour calculer la note
        catg = "Inactif"
    else:  # dans le cas ou y a pas de resiliation => ni une date ni une raison de resiliation
        resil = 0
        dfin = Date_now
        Date_Resiliation = None
        RaisonResiliation = None
        catg = "Moyen"
        d = _dateEntre(Date_Debut_Contrat, dfin)
        pub = _GenerePublication(d)  # pour passer pub en argument pour calculer la note

    Date_Avis = _dateEntre(Date_Debut_Contrat, dfin)
    testf = _ListeForfaitParticulier(Date_Debut_Contrat, dfin)
    serv = _GenererListeServicesEntreprise(Date_Debut_Contrat, dfin)

    anciennete = _differenceDate(dfin, Date_Debut_Contrat)

    try:
        if (serv is not None):
            if (len(serv) > 1):

                for j in serv:
                    j.update({"Id_client": idf})  # pour garder l'id des clients dans le fichier externe service
                    data.append(j)


    except Exception as e:
        print("Exception :", str(e))

    # cas ou y a des forfaits mais aucun service
    if ((testf is not None) and (len(testf) >= 2) and (serv is None)):

        Nbr_offres_Achetes = len(testf)
        # print("forfait nbr: ", Nbr_offres_Achetes)
        testf = sorted(testf, key=fctSortDict, reverse=False)

        Date_Dernier_Fin_Forfait = testf[-1]['Date_Fin_Forfait']
        # print("Date_Dernier_Fin_Forfait :", Date_Dernier_Fin_Forfait)
        catg = _Categorie_Abonne(resil, Date_Dernier_Fin_Forfait, anciennete)
        # print("catg : ", catg)

    # cas ou y a des services mais aucun forfait
    elif ((serv is not None) and (len(serv) >= 2) and (testf is None)):

        # Nbr_services = len(serv)
        # print("nbr service : ", Nbr_services)
        serv = sorted(serv, key=SortDatesServices, reverse=False)

        Date_Dernier_Service = serv[-1]['Date_Service']
        # print("Date_Dernier_Service", Date_Dernier_Service)
        catg = _Categorie_Abonne(resil, Date_Dernier_Service, anciennete)
        # print("catg : ", catg)

    # cas ou y a des forfaits et des services
    elif ((testf is not None) and (len(testf) >= 2) and (serv is not None) and (
            len(serv) >= 2)):  # le tri se fait uniquement si l'abonne a achete au moins deux forfaits

        # Nbr_offres_Achetes = len(testf)
        # print("nbr forf : ",Nbr_offres_Achetes)
        testf = sorted(testf, key=fctSortDict, reverse=False)

        Date_Dernier_Fin_Forfait = testf[-1]['Date_Fin_Forfait']
        # print("Date_Fin_Forfait", Date_Dernier_Fin_Forfait)

        # Nbr_services = len(serv)
        # print("nbr service : ", Nbr_services)
        serv = sorted(serv, key=SortDatesServices, reverse=False)
        Date_Dernier_Service = serv[-1]['Date_Service']
        # print("Date_Dernier_Service", Date_Dernier_Service)

        if ((Date_Dernier_Service is not None) and (Date_Dernier_Service is not None)):

            if (_CompareTwoDates(Date_Dernier_Fin_Forfait,
                                 Date_Dernier_Service) == -1):  # si Date_Dernier_Fin_Forfait<Date_Dernier_Service
                catg = _Categorie_Abonne(resil, Date_Dernier_Service, anciennete)
                # print("catg : ", catg)

            else:
                catg = _Categorie_Abonne(resil, Date_Dernier_Fin_Forfait, anciennete)
                # print("catg : ", catg)

    elif ((testf is None) and (serv is None)):  # aucun forfait et aucun service
        DerniereDate = "2018-02-18"
        catg = _Categorie_Abonne(resil, DerniereDate, anciennete)

    l = randint(1, 200)
    # print(l)
    if (l <= 1):
        date = _GenerateDateBetween('-18y', '-19y')
        ca = randint(40000, 50000)

    if ((l >= 2) & (l <= 3)):
        date = _GenerateDateBetween('-20y', '-24y')
        ca = randint(10000, 100000)

    if ((l >= 4) & (l <= 7)):
        date = _GenerateDateBetween('-25y', '-29y')
        ca = randint(100000, 112000)

    if ((l >= 8) & (l <= 16)):
        date = _GenerateDateBetween('-30y', '-34y')
        ca = randint(99800, 128000)

    if ((l >= 17) & (l <= 30)):
        date = _GenerateDateBetween('-35y', '-39y')
        ca = randint(100000, 132000)

    if ((l >= 31) & (l <= 50)):
        date = _GenerateDateBetween('-40y', '-44y')
        ca = randint(120000, 172000)

    if ((l >= 51) & (l <= 82)):
        date = _GenerateDateBetween('-45y', '-49y')
        ca = randint(140000, 180000)

    if ((l >= 83) & (l <= 119)):
        date = _GenerateDateBetween('-50y', '-54y')
        ca = randint(100000, 152000)

    if ((l >= 120) & (l <= 153)):
        date = _GenerateDateBetween('-55y', '-59y')
        ca = randint(110000, 160000)

    if ((l >= 154) & (l <= 178)):
        date = _GenerateDateBetween('-60y', '-64y')
        ca = randint(130000, 170000)

    if ((l >= 179) & (l <= 192)):
        date = _GenerateDateBetween('-65y', '-69y')
        ca = randint(96000, 140000)

    if ((l >= 193) & (l <= 200)):
        date = _GenerateDateBetween('-70y', '-77y')
        ca = randint(99000, 120000)

    SumForfait = 0
    if (testf is not None):
        for i in testf:
            SumForfait = SumForfait + int(i["Prix_Forfait"])

    ca = ca + SumForfait

    c = randint(0, 2)
    if (c == 0):
        ca = str(ca) + " Dinars"
    elif (c == 1):
        ca = str(ca) + " dinars"
    else:
        ca = str(ca) + " Dinars_Algeriens"

    Entreprise = {
        "idEntr": idf,
        "Numero_Tel": _GenererPhoneNumberParticulier(pref),
        "Categorie_Client": catg,
        "Client_Prenom": None,
        "Client_Nom": _Generer_Nom_Entreprise(),
        "Adresse": _Generer_Adresse(),
        "Date": date,
        "CA": ca,
        "Contrat": {
            "Num_contrat": _GenerernumcontratE(),
            "Date_Debut_Contrat": Date_Debut_Contrat,

        },
        "Forfaits": testf,
        "Reclamation": _ListeReclamation(Date_Debut_Contrat, dfin),

        "Avis_Abonne": {
            "Date_Avis": Date_Avis,
            "Avis_Rating": _noteglobalepublication(pub),
        },
        "Resiliation": {
            "Date_Resiliation": Date_Resiliation,
            "Raison_Resiliation": RaisonResiliation,
        },
        "Reseau_Social_Operateur":
            {
                "Nom_Reseau": "Facebook",
                "Publication": pub,
            },
    }
    return Entreprise


ListeAbonnes_Part = []
ListeAbonnes_Entrep = []


def _Generer_abonnes():
    prefixOper = "07"
    nbr_abonnes = randint(460,500)
    for i in range(2, nbr_abonnes):
        Client = fake.random_choices(elements=OrderedDict([('P', 0.85), ('E', 0.15)], length=1))[0]
        if (Client == 'P'):

            p = _Generer_Particulier(prefixOper, i)
            ListeAbonnes_Part.append(p)

        else:
            e = _Generer_Entreprise(prefixOper, i)
            ListeAbonnes_Entrep.append(e)


def _FichierJson_Externe_Particuliers():
    with open('External_Files/File_Particuliers.json', 'w') as json_file:
        json.dump(ListeAbonnes_Part, json_file)
    json_file.close()


def _FichierJson_Externe_Entreprises():
    """for i in ListeAbonnes_Entrep:
        print(i)"""
    with open('External_Files/File_companies.json', 'w') as json_file:
        json.dump(ListeAbonnes_Entrep, json_file)
    json_file.close()


def _FichierCSV_Externe_Services():
    headersCSV = ['Id_client', 'Date_Service', 'Heure_Service', 'Type_Service', 'Nom_Service', 'Description_Service']
    with open('External_Files/File_services.csv', 'w', newline='') as f_object:
        dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
        csv_writer = csv.writer(f_object, delimiter=',')
        csv_writer.writerow(headersCSV)
        for i in data:
            dictwriter_object.writerow(i)
    f_object.close()


def _Concurrent(s):
    r = randint(1, 100)
    NomConcurrent = "Operat_C" + str(r)
    ListCouv = {}
    ListCA = {}
    ListNbrAbon = {}
    ListRep = {}

    for i in range(2014, 2023):
        # generer taux de couv en chaque année
        r = randint(29, 68)
        ListCouv.update({str(i): r})

        # generer nbr abonnés en chaque année
        nbr = _GenererNbrAbonnes()
        ListNbrAbon.update({str(i): nbr})

        # generer CA en chaque année
        CA = randint(700000000, 950000000)  # entre 70 et 95 milliards
        ListCA.update({str(i): CA})

        # generer Reputation en chaque année
        if ((CA >= 700000000) and (CA < 800000000)):
            Reputation = fake.random_choices(elements=OrderedDict(((3, 0.25), (4, 0.45))), length=1)[0]

        elif ((CA >= 800000000) and (CA < 850000000)):
            Reputation = fake.random_choices(elements=OrderedDict(((3, 0.40), (4, 0.45), (5, 0.15))), length=1)[0]

        elif ((CA <= 850000000) and (CA <= 900000000)):
            Reputation = fake.random_choices(elements=OrderedDict(((3, 0.25), (4, 0.50), (5, 0.25))), length=1)[0]

        else:
            Reputation = fake.random_choices(elements=OrderedDict(((3, 0.15), (4, 0.50), (5, 0.35))), length=1)[0]

        ListRep.update({str(i): Reputation})

    Concurrent = {
        "idConc": s,
        "Nom_Concurrent": NomConcurrent,
        "Nombre_Abonnes": ListNbrAbon,
        "CA_Conc": ListCA,
        "Taux_couverture": ListCouv,
        "Reputation": ListRep,
    }

    return Concurrent


def _ListeConcurrents():
    List_Concur = []
    for i in range(0, 3):
        Concurrent = _Concurrent(i)
        List_Concur.append(Concurrent)

    return List_Concur


def _FichierJson_Externe_Concurrent():
    data = _ListeConcurrents()
    with open('External_Files/File_Competitors.json', 'w') as json_file:
        json.dump(data, json_file)
    json_file.close()



