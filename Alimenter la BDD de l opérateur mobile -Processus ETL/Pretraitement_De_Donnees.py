import csv
import json
from json import load



def Supp_Caractere_speciaux_Employes():  #pour le fichier des employés
    text = open("External_Files/File_Employees.csv", "r")
    text = ''.join([i for i in text])
    text = text.replace("ï", "i").replace("É", "E").replace("Ã©", "A").replace("ii¿½", "").replace("��", "").replace("¿½", "").replace("é", "e").replace("ê", "e").replace("è", "e").replace("à", "a").replace("ç", "c").replace(",,", ",null,").replace("{", "").replace("}", "").replace("[", "").replace("]", "").replace("$", "").replace("£", "").replace("^", "").replace("ù", "").replace("~", "").replace("§", "")
    x = open("External_Files/File_Employees.csv", "w")
    x.writelines(text)
    #print(text)
    x.close()


def Supp_Caractere_speciaux_Antenne():
    text = open("External_Files/File_Antenne.csv", "r")
    text = ''.join([i for i in text])
    text = text.replace("ï", "i").replace("É", "E").replace("é", "e").replace("ê", "e").replace("è", "e").replace("à", "a").replace("Ã©", "A").replace("ii¿½", "").replace("��", "").replace("¿½", "").replace("ç", "c").replace(",,", ",null,").replace("!", "").replace("{", "").replace("}", "").replace("[", "").replace("]", "").replace("$", "").replace("£", "").replace("^", "").replace("ù", "").replace("~", "").replace("§", "")
    x = open("External_Files/File_Antenne.csv", "w")
    x.writelines(text)
    x.close()


def Supp_Caractere_speciaux_Entrp():
    text = open("External_Files/File_companies.json", "r")
    text = ''.join([i for i in text])
    text = text.replace("ï", "i").replace("É", "E").replace("é", "e").replace("ê", "e").replace("è", "e").replace("à", "a").replace("Ã©", "A").replace("ii¿½", "").replace("��", "").replace("¿½", "").replace("ç", "c").replace(",,", ",null,").replace("!", "").replace("$", "").replace("£", "").replace("^", "").replace("ù", "").replace("~", "").replace("§", "")
    x = open("External_Files/File_companies.json", "w")
    x.writelines(text)
    x.close()


def Supp_Caractere_speciaux_Part():
    text = open("External_Files/File_Particuliers.json", "r")
    text = ''.join([i for i in text])
    text = text.replace("ï", "i").replace("É", "E").replace("é", "e").replace("ê", "e").replace("è", "e").replace("à", "a").replace("ç", "c").replace("Ã©", "A").replace("ii¿½", "").replace("��", "").replace("¿½", "").replace(",,", ",null,").replace("!", "").replace("$", "").replace("£", "").replace("^", "").replace("ù", "").replace("~", "").replace("§", "")
    x = open("External_Files/File_Particuliers.json", "w")
    x.writelines(text)
    x.close()



def Supp_Caractere_speciaux_Absence():
    text = open("External_Files/File_Absences.csv", "r")
    text = ''.join([i for i in text])
    text = text.replace("ï", "i").replace("É", "E").replace("é", "e").replace("ê", "e").replace("è", "e").replace("à", "a").replace("ç", "c").replace(",,", ",null,").replace("{", "").replace("}", "").replace("[", "").replace("]", "").replace("$", "").replace("£", "").replace("^", "").replace("ù", "").replace("~", "").replace("§", "")
    x = open("External_Files/File_Absences.csv", "w")
    x.writelines(text)
    x.close()



def supp_Doublons_Empl():
    Supp_Caractere_speciaux_Employes()
    list=[]
    with open("External_Files/File_Employees.csv", "r") as File_Employees:
        f2 = csv.DictReader(File_Employees)
        #for i in range(5):
        for row in f2:
            e = {
                "id": int(row['id']),
                "Prenom": row['Prenom'],
                "Nom": row['Nom'],
                "Date_Naissance": row['Date_Naissance'],
                "Date_Debut_Travail": row['Date_Debut_Travail'],
                "Date_Depart": row['Date_Depart'],
                "Salaire": int(row['Salaire']),
                "Date_Avis": row['Date_Avis'],
                "Avis_Rating": int(row['Avis_Rating']),
                "Nbr_Taches_Accomplies_a_Temps": int(row['Nbr_Taches_Accomplies_a_Temps']),
                "Nbr_Taches_Non_Accomplies": int(row['Nbr_Taches_Non_Accomplies']),
            }
            list.append(e)

    File_Employees.close()
    for row in list:
        for j in list:
                if(row['id']!=j['id']):
                                if(row['Prenom']==j['Prenom'] and row['Nom']==j['Nom']):
                                      if(row['Date_Naissance']==j['Date_Naissance']):
                                          list.remove(j)

    headersCSV = ['id','Prenom','Nom','Date_Naissance','Date_Debut_Travail','Date_Depart','Salaire','Date_Avis','Avis_Rating','Nbr_Taches_Accomplies_a_Temps','Nbr_Taches_Non_Accomplies']

    with open('External_Files/File_Employees.csv', 'w', newline='') as f_object:
        dictwriter_object = csv.DictWriter(f_object, fieldnames=headersCSV)
        csv_writer = csv.writer(f_object, delimiter=',')
        csv_writer.writerow(headersCSV)
        for i in list:
          dictwriter_object.writerow(i)
    f_object.close()





def Retirer_Unite_CA_Entreprises():
    text = open("External_Files/File_companies.json", "r")
    text = ''.join([i for i in text])

    text = text.replace("Dinars", "").replace("dinars", "").replace("Dinars_Algeriens", "").replace("_Algeriens", "")
    x = open("External_Files/File_companies.json", "w")
    x.writelines(text)
    x.close()

def Retirer_Unite_CA_Particuliers():
    text = open("External_Files/File_Particuliers.json", "r")
    text = ''.join([i for i in text])
    text = text.replace("Dinars", "").replace("dinars", "").replace("Dinars_Algeriens", "").replace("_Algeriens", "")
    x = open("External_Files/File_Particuliers.json", "w")
    x.writelines(text)
    x.close()





def Filtrer_donnees_Particulier():      #supp les données inutiles
    with open("External_Files/File_Particuliers.json", "r") as File_part:
        data1 = load(File_part)

        for i in data1:
            if ("Situation_familiale" in i and "professionClient" in i and "lieu_Travail" in i ):
                 del i["Situation_familiale"]
                 del i["professionClient"]
                 del i["lieu_Travail"]

    File_part.close()

    with open('External_Files/File_Particuliers.json', 'w') as File_part:
            json.dump(data1, File_part)
    File_part.close()


def Convertir_en_valeurs_numerique():
    with open("External_Files/File_Particuliers.json", "r") as File_part:
        data1 = load(File_part)
    with open("External_Files/File_companies.json", "r") as File_entrep:
        data2 = load(File_entrep)


        for i in data1:
            if(i['Reclamation'] is not None):
                for k in i['Reclamation']:
                    if(k['Answered']=="Yes"):
                       k['Answered']=1
                    else:
                        k['Answered']=0
                    if(k['Resolved']=="Yes"):
                        k['Resolved']=1
                    else:
                        k['Resolved']=0


        for d in data2:
            if(d['Reclamation'] is not None):
                for k in d['Reclamation']:
                    if(k['Answered']=="Yes"):
                       k['Answered']=1
                    else:
                        k['Answered']=0
                    if(k['Resolved']=="Yes"):
                        k['Resolved']=1
                    else:
                        k['Resolved']=0



    File_part.close()
    File_entrep.close()

    with open('External_Files/File_Particuliers.json', 'w') as File_part:
        json.dump(data1, File_part)
    with open('External_Files/File_companies.json', 'w') as File_entrep:
        json.dump(data2, File_entrep)


    File_part.close()
    File_entrep.close()



