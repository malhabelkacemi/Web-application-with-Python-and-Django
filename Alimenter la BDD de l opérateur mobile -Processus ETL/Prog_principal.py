
from Alimentation_BDD import _Alimenter_Operateur
from Performance import _PerfComp,Metadonnee
from Pretraitement_De_Donnees import Supp_Caractere_speciaux_Part, Supp_Caractere_speciaux_Entrp, \
    Supp_Caractere_speciaux_Antenne, Supp_Caractere_speciaux_Absence, Supp_Caractere_speciaux_Employes, \
    Retirer_Unite_CA_Particuliers, Retirer_Unite_CA_Entreprises, Filtrer_donnees_Particulier, \
    Convertir_en_valeurs_numerique, supp_Doublons_Empl
from collectData import _FichierCSV_Externe_Services, _FichierJson_Externe_Particuliers, \
    _FichierJson_Externe_Entreprises, _Generer_abonnes, _FichierCSV_Externe_Antenne, _FichierCSV_Externe_Absences, \
    _AjouterDoublonsEmployes, _FichierCSV_Externe_Employees, _FichierJson_Externe_Concurrent, _Generer_Particulier



from pymongo import MongoClient
myclient = MongoClient('localhost', 27017)



try:

    # simulation de donnees
    _FichierJson_Externe_Concurrent()

    _FichierCSV_Externe_Employees()
    _AjouterDoublonsEmployes()

    _FichierCSV_Externe_Absences()

    _FichierCSV_Externe_Antenne()

    _Generer_abonnes()

    _FichierJson_Externe_Entreprises()
    _FichierJson_Externe_Particuliers()
    _FichierCSV_Externe_Services()

    print("La phase de collecte de données est terminée")



    #pretraitement des données
    supp_Doublons_Empl()
    Convertir_en_valeurs_numerique()

    Filtrer_donnees_Particulier()

    Retirer_Unite_CA_Entreprises()

    Retirer_Unite_CA_Particuliers()
    Supp_Caractere_speciaux_Employes()
    Supp_Caractere_speciaux_Absence()
    Supp_Caractere_speciaux_Antenne()

    Supp_Caractere_speciaux_Entrp()
    Supp_Caractere_speciaux_Part()

    print("La phase de pretraitement de données est terminée")


    #Alimentation de la BDD ( à partir des fichiers externes)

    _Alimenter_Operateur()
    print("La phase d'alimentation de BDD est teminée")




    #Les 4 axes de Performance + Metadonnées

    """def Configuration_Metadonnees():
            Collection_Metadonnees = myclient.myNewDb.get_collection("Metadonnees")

            m = Metadonnee()
            Collection_Metadonnees.insert_one(m)

    Configuration_Metadonnees()


    def _Performance():
            Collection_Performance = myclient.myNewDb.get_collection("Performance")
            p = _PerfComp()
            Collection_Performance.insert_one(p)


    _Performance()

    
   """

except Exception as e:
    print("Exception :", str(e))
myclient.close()