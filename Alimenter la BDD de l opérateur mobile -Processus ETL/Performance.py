from datetime import datetime
from random import randint

from bson import ObjectId
from pymongo import MongoClient


myclient = MongoClient('localhost', 27017)

# PERFORMANCE
CollectionPerformance = myclient.myNewDb.get_collection("Performance")
List_performances = list(CollectionPerformance.find())

# OPERATEUR
CollectionOperateur = myclient.myNewDb.get_collection("OPERATEUR")
Operateur = list(CollectionOperateur.find())


ListAbonnes = Operateur[0]["Abonnes"]
ListEmployes = Operateur[0]["Employés"]
ListConcurrent= Operateur[0]["Concurrent"]
ListAntennes= Operateur[0]["Antenne"]
ListAbonnesPart = []  # list des  particuliers
ListAbonnesEnt = []  # liste des entreprises




for x in ListAbonnes:
    if (x["Type_Client"] == "Entreprise"):
        ListAbonnesEnt.append(x)
    else:
        ListAbonnesPart.append(x)





Current_Year = int(datetime.today().strftime('%Y'))+1

def _Remplissage_CA_Entrep():

    ListCA_Entr={}
    for an in range(2014, Current_Year):
        CA_en_une_annee = 0
        for x in ListAbonnesEnt:
                d_contrat = int((x["Contrat"]["Date_Debut_Contrat"]).split("-")[0])
                if d_contrat == an:
                        CA_en_une_annee = CA_en_une_annee + x['CA']
        ListCA_Entr.update({str(an):CA_en_une_annee})

    """for x in ListCA_Entr:
        print(x)"""
    return ListCA_Entr


def _Remplissage_CA_Particuliers():

    ListCA_Part = {}
    for an in range(2014, Current_Year):
        CA_en_une_annee = 0
        for x in ListAbonnesPart:
            d_contrat = int((x["Contrat"]["Date_Debut_Contrat"]).split("-")[0])
            if d_contrat == an:
                CA_en_une_annee = CA_en_une_annee + x['CA']
        ListCA_Part.update({str(an): CA_en_une_annee})

    """for x in ListCA_Part:
        print(x)"""
    return ListCA_Part


def Rempl_SatisfactionEmploye():

    List_Satisf_Emp = {}
    for an in range(2014, Current_Year):
        n = 0
        nbr = 0
        for x in ListEmployes:
            d_avis = int((x["Avis_Employe"]["Date_Avis"]).split("-")[0])
            if d_avis == an:
                n += 1
                if ((x["Avis_Employe"]['Avis_Rating'] == 4) or (x["Avis_Employe"]['Avis_Rating'] == 5)):
                    nbr += 1

        if (n <= 5):
            List_Satisf_Emp.update({str(an): randint(30,35)})
        else:
            s = round(100 * (nbr / n), 2)
            List_Satisf_Emp.update({str(an): int(s)})
    return List_Satisf_Emp


def Taux_Accompl_Taches():

    List_Task = {}
    for an in range(2014, Current_Year):
        nbr_Total_taches = 0
        nbrTotalAccomli=0
        for x in ListEmployes:
            dat= int((x["Date_Debut_Travail"]).split("-")[0])
            if dat == an:
                nbrTotalAccomli=nbrTotalAccomli +x["Nbr_Taches_Accomplies_a_Temps"]
                nbr_Total_taches = nbr_Total_taches+ x["Nbr_Taches_Accomplies_a_Temps"] + x["Nbr_Taches_Non_Accomplies"]

        if(nbrTotalAccomli>800):
           nbrTotalAccomli=nbrTotalAccomli-randint(250,410)

        if(nbr_Total_taches==0):
            taux=0.22
            List_Task.update({str(an): taux})
        else:
            taux = round(100 * (nbrTotalAccomli / nbr_Total_taches), 2)
            List_Task.update({str(an): int(taux)})
    return List_Task


def Taux_Trait_Reclam_Entrep():

    List_TRec = {}
    for an in range(2014, Current_Year):
        nbr_rec = 0
        nbrTrait= 0
        for x in ListAbonnesEnt:
            r=x["Reclamation"]

            if(r is not None):

                for g in r:
                    nbr_rec=nbr_rec+1
                    dat = int((g["Date_Call"]).split("-")[0])
                    if dat == an:

                        if ((g["Resolved"] ==1)):
                            nbrTrait += 1


        if(nbrTrait==0):
            taux=42
            List_TRec.update({str(an): taux})
        else:
          taux=round(100*(nbrTrait/nbr_rec),2)
          if (taux <= 20):
              List_TRec.update({str(an): randint(42, 81)})
          else:
           List_TRec.update({str(an): int(taux)})

    return  List_TRec

def Taux_Trait_Reclam_Part():

                ################ Particulier ##################

    List_TRec_Part = {}
    for an in range(2014, Current_Year):
        nbr_rec = 0
        nbrTrait= 0

        for x in ListAbonnesPart:
            r=x["Reclamation"]

            if(r is not None):

                for g in r:
                    nbr_rec=nbr_rec+1
                    dat = int((g["Date_Call"]).split("-")[0])
                    if dat == an:

                        if ((g["Resolved"] ==1)):
                            nbrTrait += 1


        if(nbrTrait==0):
            taux=38
            List_TRec_Part.update({str(an): taux})

        else:
          taux=round(100*(nbrTrait/nbr_rec),2)
          if(taux<=20):
              List_TRec_Part.update({str(an): randint(42,81)})
          else:
           List_TRec_Part.update({str(an): int(taux)})


    return List_TRec_Part




def _ChurnEntr():

                 ######### churn entreprise ##########
    total = 0
    ListChurn_Entr={}
    for an in range(2014, Current_Year):
        nbr_Entr=0
        nbrTotal=0
        s=0

       #nbr client qui ont une date de contrat <= an
        for i in ListAbonnesEnt:
            b= int((i["Contrat"]["Date_Debut_Contrat"]).split("-")[0])
            #print(type(an))
            if(b<=an):
                nbrTotal = nbrTotal+1
            else:
                nbrTotal=1
        #print(nbrTotal)

        for x in ListAbonnesEnt:
            d_Resil= x["Resiliation"]["Date_Resiliation"]
            #print(d_Resil)
            if(d_Resil is not None):
                    d_Resil=int(d_Resil.split("-")[0])
                    #print(d_Resil)
                    if(d_Resil == an):
                        nbr_Entr = nbr_Entr+ 1
                        #print(nbr_Entr)


        total = total + (nbrTotal - nbr_Entr)

        if (total == 0):
            ListChurn_Entr.update({str(an): randint(9, 25)})
        else:
            s = 100 * round((nbr_Entr / total), 2)
            if (s >= 100):
                ListChurn_Entr.update({str(an): randint(65, 90)})
            elif (s <= 0):
                ListChurn_Entr.update({str(an): randint(9, 45)})
            else:

                ListChurn_Entr.update({str(an): int(s)})


    return  ListChurn_Entr


def Churn_Particulier():
                    ######### churn Particuliers ##########
    total=0
    ListChurn_Part={}
    for an in range(2014, Current_Year):
        nbr_part=0
        nbrTotal=0
        s=0

        for i in ListAbonnesPart:
            b= int((i["Contrat"]["Date_Debut_Contrat"]).split("-")[0])
            #print(type(an))
            if(b<=an):
                nbrTotal = nbrTotal+1
            else:
                nbrTotal=1
        #print(nbrTotal)

        for x in ListAbonnesPart:
            d_Resil= x["Resiliation"]["Date_Resiliation"]
            #print(d_Resil)
            if(d_Resil is not None):
                    d_Resil=int(d_Resil.split("-")[0])
                    #print(d_Resil)
                    if(d_Resil == an):
                        nbr_part = nbr_part+ 1
                        #print(nbr_part)

        total=total+(nbrTotal-nbr_part)

        if(total==0):
            ListChurn_Part.update({str(an): randint(9,25)})
        else:
            s = 100 *round((nbr_part / total), 2)
            if(s>=100):
               ListChurn_Part.update({str(an):randint(65,90)})
            elif(s<=0):
                ListChurn_Part.update({str(an): randint(9, 45)})
            else:
                ListChurn_Part.update({str(an): int(s)})
    return  ListChurn_Part


def _Remplissage_Satisf_Entrep():
    #a partir de  **Avis d'abonné


    ListSatisf_Entr={}
    for an in range(2014, Current_Year):
        n= 0
        nbr_Entr=0
        for x in ListAbonnesEnt:
                d_avis= int((x["Avis_Abonne"]["Date_Avis"]).split("-")[0])
                if d_avis == an:
                    n += 1
                    if ((x["Avis_Abonne"]['Avis_Rating']==4) or (x["Avis_Abonne"]['Avis_Rating']==5)):
                        nbr_Entr = nbr_Entr+ 1
                        #print((x["Avis_Abonne"]["Avis_Rating"]))


        if (n == 0):
             ListSatisf_Entr.update({str(an): randint(20, 25)})
        else:
             s = 100 * round((nbr_Entr / n), 2)
             if (s >= 100):
                 ListSatisf_Entr.update({str(an): randint(55, 90)})
             elif (s <= 0):
                 ListSatisf_Entr.update({str(an): randint(16, 45)})
             else:

                 ListSatisf_Entr.update({str(an): int(s)})

    """for x in ListSatisf_Entr:
        print(x)"""
    return ListSatisf_Entr

def _Remplissage_Satisf_Particulier():
    ListSatisf_Part={}
    for an in range(2014, Current_Year):
        n= 0
        nbr_Part=0
        for x in ListAbonnesPart:
                d_avis= int((x["Avis_Abonne"]["Date_Avis"]).split("-")[0])
                if d_avis == an:
                    n += 1
                    if ((x["Avis_Abonne"]['Avis_Rating']==4) or (x["Avis_Abonne"]['Avis_Rating']==5)):
                        nbr_Part = nbr_Part+ 1
                        #print((x["Avis_Abonne"]["Avis_Rating"]))

        if (n == 0):
             ListSatisf_Part.update({str(an): randint(20, 25)})
        else:
             s = 100 * round((nbr_Part / n), 2)
             if (s >= 100):
                 ListSatisf_Part.update({str(an): randint(55, 90)})
             elif (s <= 0):
                 ListSatisf_Part.update({str(an): randint(16, 45)})
             else:

                 ListSatisf_Part.update({str(an): int(s)})
    """for x in ListSatisf_Part:
        print(x)"""

    return ListSatisf_Part



def sommePartCA():
    ListPartM={}
    s = List_performances[0]["PerfCom"]["ListeKPI"]


    for an in range(2014, Current_Year):
        sum = 0
        for j in ListConcurrent:
           d= j["CA_Conc"][str(an)]
           sum=sum+d  #somme de CA des concurrents
        for x in s:
          if (x["Nom_KPI"].lower() == "incomes"):

                sum=sum+x["Valeurs_KPI_Entr"][str(an)]+x["Valeurs_KPI"][str(an)]


        ListPartM.update({str(an): sum})
    return ListPartM


def PartMarcher(): #de l operateur
    listSommeCA=sommePartCA()

    PM={}
    s = List_performances[0]["PerfCom"]["ListeKPI"]
    for an in range(2014, Current_Year):

        sum = 0
        for x in s:
          if (x["Nom_KPI"].lower() == "incomes"):
                sum=sum+x["Valeurs_KPI_Entr"][str(an)]+x["Valeurs_KPI"][str(an)]

        d=listSommeCA[str(an)]
        t=round(100*(sum/d),2)
        PM.update({str(an):t})

    return PM





def Consom_Energie():
    List_energ = {}

    for an in range(2014, Current_Year):
        r = randint(28, 52)  #en TWh
        List_energ.update({str(an):r})
    return List_energ


def CouvertureOperateur():
    List_Couv = {}
    for an in range(2014, Current_Year):
        l = []
        for x in ListAntennes:
            d_instal = int((x["Date_Installation"]).split("-")[0])
            if (d_instal == an):
                c = x["Region"]["Nom_Wilaya"]
                l.append(c)
        nb=len(list(set(l)))-randint(6,22)

        if (nb == 0):
            List_Couv.update({str(an): 0})
        else:
            taux = round(100 * (nb / 48))
            List_Couv.update({str(an): int(taux)})

    """for x in List_Couv:
        print(x)"""

    return List_Couv

def Reputation():

        # apartir de  Caractere Publication + avis abonnés
        ListReputation = {}
        for an in range(2014, Current_Year):
            n = 0
            s = 0
            m = 0
            for x in ListAbonnes:
                p = x["Reseau_Social_Operateur"]["Publication"]
                d_avis = int((x["Avis_Abonne"]["Date_Avis"]).split("-")[0])
                if (p is not None):
                    for t in p:
                        date_Pub = int((t["Date_Publ"]).split("-")[0])
                        if date_Pub == an:
                            n += 1
                            c = t["Caractere"]
                            if (c == "tres_mauvaise"):
                                r = 1
                            elif (c == "mauvaise"):
                                r = 2
                            elif (c == "Moyenne"):
                                r = 3
                            elif (c == "Tres_Bonne"):
                                r = 4
                            else:
                                r = 5
                            s = s + r
                        if(d_avis == an):
                            m += 1
                            s=s+x["Avis_Abonne"]['Avis_Rating']
            if (n == 0 and m == 0):
                ListReputation.update({str(an): 2})
            else:
                y = round((s /(n+ m)))
                ListReputation.update({str(an): y})

        return ListReputation



# Commercial
# CA
Seuils_CA_Part = { "2014": 220000 ,  "2015": 250000 ,  "2016": 250000 ,  "2017": 280000 ,  "2018": 280000 , "2019": 240000 ,  "2020": 270000 ,  "2021": 300000 }
Seuils_CA_Ent = { "2014": 180000 ,  "2015": 230000 ,  "2016": 230000 ,  "2017": 270000 ,  "2018": 240000 ,"2019": 270000 ,  "2020": 280000 ,  "2021": 280000 }

# Taux Satif abonnés
Seuils_Satf_Abon_Part = { "2014": 50 ,  "2015": 55 ,  "2016": 60 ,  "2017": 65 ,  "2018": 60 ,  "2019": 70 ,"2020": 70 ,  "2021": 75 }
Seuils_Satf_Abon_Ent = { "2014": 40 ,  "2015": 45 ,  "2016": 50 ,  "2017": 50 ,  "2018": 40 ,  "2019": 55 ,"2020": 65 ,  "2021": 70 }

# Taux traitement reclamations
Seuils_Tr_Rec_Part = { "2014": 50 ,  "2015": 55 ,  "2016": 60 ,  "2017": 65 ,  "2018": 60 ,  "2019": 60 ,  "2020": 60 ,"2021": 75 }
Seuils_Tr_Rec_Ent = { "2014": 40 ,  "2015": 45 ,  "2016": 50 ,  "2017": 50 ,  "2018": 40 ,  "2019": 55 ,  "2020": 65 ,"2021": 70 }


# Social
# Taux satisfaction des employés
Seuils_Satf_Emp = { "2014": 40 ,  "2015": 50 ,  "2016": 60 ,  "2017": 65 ,  "2018": 60 ,  "2019": 60 ,  "2020": 70 ,"2021": 70 }

# Churn rate
Seuils_Churn_Part = { "2014": 40 ,  "2015": 35 ,  "2016": 35 ,  "2017": 45 ,  "2018": 42 ,  "2019": 40 ,  "2020": 35 ,"2021": 25 }
Seuils_Churn_Ent = { "2014": 45 ,  "2015": 35 ,  "2016": 35 ,  "2017": 45 ,  "2018": 40 ,  "2019": 30 ,  "2020": 25 ,"2021": 23 }
# Taux d'accomplissement des taches
Seuils_Task_Emp = { "2014": 50 ,  "2015": 55 ,  "2016": 65 ,  "2017": 65 ,  "2018": 60 ,  "2019": 70 ,  "2020": 75 ,"2021": 75 }




# Perf Concurrentielle
# Reputation
Seuils_Rep = { "2014": 3 ,  "2015": 3 ,  "2016": 3 ,  "2017": 4 ,  "2018": 3 ,  "2019": 4 ,  "2020": 4 ,  "2021": 4 }

# Part_de_marcher
Seuils_Marcher = { "2014": 20 ,  "2015": 20 ,  "2016": 25 ,  "2017": 20 ,  "2018": 30 ,  "2019": 35 ,  "2020": 35 , "2021": 45 }

# Environnementale
# Energy_Consom
Seuils_Cons_Energy = { "2014": 65 ,  "2015": 50 ,  "2016": 60 ,  "2017": 45 ,  "2018": 45 ,  "2019": 55 ,  "2020": 45 ,"2021": 45 }

# Taux de couverture
Seuils_Cover = { "2014": 30 ,  "2015": 35 ,  "2016": 40 ,  "2017": 35 ,  "2018": 45 ,  "2019": 55 ,  "2020": 60 ,"2021": 70 }



                            ### Type ###
#1 : pour abonnés (pour les 2 types: particuliers et entreprises
#2 : employés
#3 :autres (concur , envir)
def conso():
    ListEnerg ={}
    for an in range(2014, 2023):
        ListEnerg.update({str(an): randint(70,110)})
    return ListEnerg


def _PerfComp():

    PerformanceComp={
    "PerfCom": {
    "NomPerf":"commercial",
    "ListeKPI": [
          {
            "Nom_KPI": "Incomes",
            "Desc_KPI":"Mobile operateur incomes ",
            "Fct_KPI":  "sum(Incomes)",
            "Valeurs_KPI":_Remplissage_CA_Particuliers(),
            "Valeurs_KPI_Entr": _Remplissage_CA_Entrep(),
            "Seuil_KPI": Seuils_CA_Part,
            "Seuil_KPI_Entr":Seuils_CA_Ent,
            "Type": 1,
           },

        {
            "Nom_KPI": "%Satf_Subscr",
            "Desc_KPI": "Subscribers satisfaction rate",
            "Fct_KPI": "avg(Subscribers_satisfaction_rating)",
            "Valeurs_KPI": _Remplissage_Satisf_Particulier(),
            "Valeurs_KPI_Entr": _Remplissage_Satisf_Entrep(),
            "Seuil_KPI":Seuils_Satf_Abon_Part,
            "Seuil_KPI_Entr":Seuils_Satf_Abon_Ent,
            "Type": 1,
        },
        {
            "Nom_KPI": "%Compl_Handling",
            "Desc_KPI":"Complaints handling rate",
            "Fct_KPI": "100*(sum(Resolved)/Complaints)",
            "Valeurs_KPI":Taux_Trait_Reclam_Part(),
            "Valeurs_KPI_Entr":Taux_Trait_Reclam_Entrep(),
            "Seuil_KPI": Seuils_Tr_Rec_Part,
            "Seuil_KPI_Entr":Seuils_Tr_Rec_Ent,
            "Type": 1,
        },
    ],},


    "PerfSoc": {
    "NomPerf":"social",
    "ListeKPI": [
            {
            "Nom_KPI": "%Satf_Employees",
            "Desc_KPI":"Satisfaction rate of employees",
            "Fct_KPI":"avg(Employees_satisfaction_rating)",
            "Valeurs_KPI": Rempl_SatisfactionEmploye(),
            "Seuil_KPI": Seuils_Satf_Emp,
            "Seuil_KPI_Entr": "-",
            "Type": 2,
           },
        {
            "Nom_KPI": "%Churn",
            "Desc_KPI": "Churn rate of Subscribers",
            "Fct_KPI": "100*((sum(unsubscription)/ Number_subscribers)",
            "Valeurs_KPI":Churn_Particulier(),
            "Valeurs_KPI_Entr": _ChurnEntr(),
            "Seuil_KPI": Seuils_Churn_Part,
            "Seuil_KPI_Entr":Seuils_Churn_Ent,
            "Type": 1,
        },
        {
            "Nom_KPI": "%Task_Accompl",
            "Desc_KPI": "Task accomplishement rate",
            "Fct_KPI": "100*((Nbr_Completed_Tasks)/Nbr_Total_Tasks)",
            "Valeurs_KPI":Taux_Accompl_Taches(),
            "Seuil_KPI": Seuils_Task_Emp,
            "Seuil_KPI_Entr": "-",
            "Type": 2,
        },
   ],},

    "PerfConc":
   {
    "NomPerf":"competitive",
    "ListeKPI": [
        {
            "Nom_KPI": "Reputation",
            "Desc_KPI": "Reputation!",
            "Fct_KPI": "(Publication_Rating + Subscribers_satisfaction_rating)/2",
            "Valeurs_KPI": Reputation(),
            "Seuil_KPI": Seuils_Rep,
            "Seuil_KPI_Entr": "-",
            "Type": 3,
        },

        {
            "Nom_KPI": "%Satf_Subscr",
            "Desc_KPI": "Subscribers satisfaction rate",
            "Fct_KPI": "avg(Subscribers_satisfaction_rating)",
            "Valeurs_KPI": _Remplissage_Satisf_Particulier(),
            "Valeurs_KPI_Entr": _Remplissage_Satisf_Entrep(),
            "Seuil_KPI": Seuils_Satf_Abon_Part,
            "Seuil_KPI_Entr": Seuils_Satf_Abon_Ent,
            "Type": 1,
        },
    ],
   },


   "PerfEnv":
        {
            "NomPerf": "environnemental",
            "ListeKPI": [

                {
                    "Nom_KPI": "%Cover",
                    "Desc_KPI": "Coverage rate ",
                    "Fct_KPI": "100 * (Nbr_Covered_wilayas/ 48)",
                    "Valeurs_KPI": CouvertureOperateur(),
                    "Seuil_KPI": Seuils_Cover,
                    "Seuil_KPI_Entr": "-",
                    "Type": 3,
                },
                {
                    "Nom_KPI": "Energy_Consom",
                    "Desc_KPI": "Energy consumption",
                    "Fct_KPI": "Sum(Consom_Energitique)",
                    "Valeurs_KPI": conso(),
                    "Seuil_KPI": Seuils_Cons_Energy,
                    "Seuil_KPI_Entr": "-",
                    "Type": 3,
                }


            ],
        },
    }


    return PerformanceComp


"""{
       "Nom_KPI": "Energy_Consom",
       "Desc_KPI": "Energy consumption",
       "Fct_KPI": "........",
       "Valeurs_KPI": Consom_Energie(),
       "Seuil_KPI": Seuils_Cons_Energy,
       "Seuil_KPI_Entr": "-",
       "Type": 3,
   },"""


def Metadonnee():

      metadonnee={

        "commercial": {
           "Liste_KPI": [ "subscribers_satisfaction_rate", "number_customers" , "seniority","number_complaints","incomes","revenue","loyalty_rate" , "acquiring_customers_rate","%satf_subscr", "%compl_handling" ],
           "Liste_Attributes": [ "Incomes", "Complaints", "Package_duration" ,   "Package_price","Resolved"  ,"Subscribers_satisfaction_rating" ,"Salary" ],
           "Stakeholders": [ "subscribers"],
        },
        "social": {
           "Liste_KPI": [ "absenteeism_rate", "turnover","late_rate","task_accomplishement_rate" , "satisfaction_employees_rate"  ,  "churn"  , "resignation_employees", "%satf_employees" , "%churn" ,"%task_accompl"],
           "Liste_Attributes": [ "unsubscription","work_start_date","Nbr_unfinished_Tasks","Nbr_Completed_Tasks" ,"Resignation", "Date_Absence" , "Employee_satisfaction_rating" ],
           "Stakeholders": ["employees","subscribers" ],
        },
        "competitive": {
           "Liste_KPI": ["reputation","subscribers_satisfaction_rate", "part_of_market" , "competitive_advantage", "%satf_subscr" ],
           "Liste_Attributes": [ "shares" ,"likes" , "comments" ],
           "Stakeholders": ["others","subscribers","employees" ],
        },
        "environnemental": {
           "Liste_KPI": [ "energy_consumption_rate","coverage_rate","rates_of_progress","rate_of_use_of_internet" , "%cover",
                          "rate_of_use_of_calls", "rate_of_use_of_sms", "waste_rate", "energy_consom"],
           "Liste_Attributes": [ "Antenne","Antenne_Frequency" , "Services" ],
           "Stakeholders": ["others" ],
        },
        "economic": {
           "Liste_KPI": ["price_competitiveness","non_price_competitiveness","benefit","economic_rentability" ],
           "Liste_Attributes": ["Incomes" ],
           "Stakeholders": ["subscribers","others" ],
        },
        "strategic": {
           "Liste_KPI": [ "return_rate", "ability_of_innovation" ],
           "Liste_Attributes": ["Nbr_unfinished_Tasks","Nbr_Completed_Tasks" ],
           "Stakeholders": [ "employees" , "others"],
        },
        "societal": {
           "Liste_KPI": ["achieved_performance_levels","progress_of_planned_actions","number_jobs_created", "amounts_of_investments" ],
           "Liste_Attributes": [ "Nbr_unfinished_Tasks","Nbr_Completed_Tasks","Subscribers_satisfaction_rating" ,  "Employee_satisfaction_rating"],
           "Stakeholders": ["subscribers","employees" ],
        },
        "financial": {
           "Liste_KPI": ["value_creation" , "financial_rentability" ,  "net_margin" , "raw_margin","eva" ],
           "Liste_Attributes": [ "Incomes"],
           "Stakeholders": ["subscribers","employees" ],
        },
        "production": {
           "Liste_KPI": ["service_quality" , "overall_rate_of_return", "synthetic_rate_of_return", "trs", "planning_reliability_rate"],
           "Liste_Attributes": ["Incomes" ],
           "Stakeholders": ["subscribers" ,"others" ],
        },
        "organizational": {
           "Liste_KPI": ["quality_information_flow","structural_flexibility" , "level_of_maturity","performance_level"],
           "Liste_Attributes": ["Nbr_unfinished_Tasks","Nbr_Completed_Tasks"  ],
           "Stakeholders": ["employees","subscribers" ],
        },
      }


      return metadonnee




myclient.close()








