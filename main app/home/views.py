# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
import itertools
import pymongo
from pymongo import MongoClient
from itertools import combinations
import numpy as np 
from datetime import datetime
import csv
import json
import re
from datetime import datetime
from itertools import combinations
from tkinter import filedialog

from bson import ObjectId
from django import template
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
import pymongo
import csv
import json
from json import load
import csv
from tkinter import filedialog

from pymongo import MongoClient
import pandas
import json
from csv import DictWriter
from pyexpat.errors import messages
from pymongo import MongoClient
import re
from datetime import datetime


zutter=()

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def adminpage(request):
    return render(request, 'home/adminpage.html')


@csrf_exempt
def traitement(request):
    
    if request.method == "POST":
        myclient2 = MongoClient('localhost', 27017)
       

        where = myclient2.myNewDb.Performance
        info1 = request.POST
        info = list(request.POST)
        info.pop(0)
        for x in info:
            key = x
            path = x.split(",")
            iteration= len(path)
            dic = dict(request.POST)
            dic.pop("csrfmiddlewaretoken")
            where.update_one({path[1]+".ListeKPI.Nom_KPI": path[0]}, {'$set': {path[1]+".ListeKPI.$."+path[2]+".2022": int(dic[key][0])}})
        msg="seccess"
    return render(request, 'home/add_seuils.html', {'msg':msg})

@csrf_exempt
def add_objectifs(request):

    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["myNewDb"]
    colle = db["Performance"]
    base = colle.find({})
    clone = base.clone()
    bigl=[]
    
    for x in clone:
        x.pop("_id")
        for y in x.values():
            minl={}
            minl["NomPerf"]=y['NomPerf']
            minl["ListeKPI"]=[]
            for k in y['ListeKPI']:
                minl["ListeKPI"].append(k['Nom_KPI'])
                if k['Objectif_Entr'] != '-':
                    minl["ListeKPI"].append(k['Nom_KPI']+"_Ent")
            bigl.append(minl)
        
    
           
    
       
    

    if request.method == "POST":
        myclient2 = MongoClient('localhost', 27017)
       

        where = myclient2.myNewDb.Performance
        info1 = request.POST
        info = list(request.POST)
        info.pop(0)
        ent=[]
        part=[]
        for x in info:
            if len(x.split('_Ent'))==2:
                ent.append(x.split('_Ent').pop(0))
                
            else:
                part.append(x)
        print(ent)
        print(part)
        for x in part:
            key = x
            
            
            where.update_one({"ListeKPI.Nom_KPI": x}, {'$set': {"ListeKPI."+x+".Objectifs.2022": "selected"}})
        msg="seccess"
    return render(request, 'home/add_objectifs.html', {'bigl':bigl})

@csrf_exempt
def partieprenante (request):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["myNewDb"]
    colle = db["Performance"]
    base = colle.find({})
    clone = base.clone()
    lkpi=[]

    listkpi=[]
    partpren=[]

    if request.method == "POST":
        p= list(request.POST)
        p.pop(0)
        request.session['perf']=p
        for x in clone:
            x.pop("_id")
            for y in p:
                lkpi.append(x.pop(y))
        for y in lkpi:
            listkpi.append(y.pop("ListeKPI"))
        for y in listkpi:
            for j in y :
                if j["Type"]==1:
                    if not partpren:
                        partpren.append("Particulier")
                        partpren.append("Entreprise")
                    else:
                        t=0
                        for i in partpren:
                            if i == "Particulier" or i == "Entreprise":
                                t=1
                                break
                        if t == 0:
                            partpren.append("Particulier")
                            partpren.append("Entreprise")
                elif j["Type"] == 2:
                    if not partpren:
                        partpren.append("Employes")
                        
                    else:
                        t=0
                        for i in partpren:
                            if i == "Employes":
                                t=1
                                break
                        if t == 0:
                            partpren.append("Employes")
                else:
                    if not partpren:
                        partpren.append("Other")
                        
                    else:
                        t=0
                        for i in partpren:
                            if i == "Other":
                                t=1
                                break
                        if t == 0:
                            partpren.append("Other")
        
        return render (request, 'home/partieprenante.html', {'partpren': partpren} )
                
                        



@csrf_exempt
def traitementchoixperf(request):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["myNewDb"]
    colle = db["Performance"]
    base = colle.find({})
    clone = base.clone()
    liskpi=[]
    kpi=[]
    lkpi=[]
    combil=[]
    ref=[]

    if request.method == "POST":
        p=1
        p= list(request.POST)
        p.pop(0)
        lp = request.session["perf"]

        for x in clone:
            x.pop("_id")
            for y in lp:
                liskpi.append(x.pop(y))
        for y in liskpi:
            kpi.append(y.pop("ListeKPI"))   

        for k in p:
            for y in kpi:
                for i in y :
                    if k == "Particulier" and i["Type"]==1:
                        lkpi.append(i["Nom_KPI"])
                    elif k == "Entreprise" and i["Type"]==1:
                        name=i["Nom_KPI"]+"_Ent"
                        lkpi.append(name)
                    elif k == "Employes" and i["Type"]==2:
                        lkpi.append(i["Nom_KPI"])
                    elif k == "Other" and i["Type"]==3:
                        lkpi.append(i["Nom_KPI"])
 
        
        return render (request, 'home/traitementchoixperf.html', {"lkpi": lkpi} )

@csrf_exempt
def evalperf(request):
    combil=[]
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["myNewDb"]
    colle = db["Performance"]
    base = colle.find({})
    clone = base.clone()
    for i in base:
        perf=list(i.keys())

    perf.pop(0)
    en="_Ent"
    tes=[]
    lkpi=[]
    vkpi=[]
    fkpi=[]
    skpi=[]
    pkpi=[]
    intra=[]
    inter=[]
    ldic=[]
    looper=[]
    loopra=[]
    ecar={}
    peri=[]

    if request.method == "POST":
        p= list(request.POST)
        q=dict(request.POST)
        
        
        p.pop(0)
        print("here")
        print(p)

        period=p[-2:]
        p.pop(-1)
        p.pop(-1)
        for item in period:
            peri.append(q[item])
        
        for i in peri:
            for k in i:
                period.append(k)
        period.pop(0)
        period.pop(0)      
        print(period)
        combi = list(combinations(p , 2))
        for y in combi:
            combil.append(list(y))
        for x in clone:
            x.pop("_id")
            for i in perf:
                tes.append(x.pop(i))
        for x in tes:
            lkpi.append(x["ListeKPI"])
        for y in combil:
            for c in y:
                for x in tes:
                    for i in x["ListeKPI"]:
                        if en in c:
                            kp=c.split('_Ent').pop(0)
                            if i["Nom_KPI"]==kp:
                                pkpi.append(x["NomPerf"])
                        else:
                            if i["Nom_KPI"]==c:
                                pkpi.append(x["NomPerf"])

        for i in combil:
            for c in i:
                for x in lkpi:
                    for y in x:
                        if en in c:
                            kp=c.split('_Ent').pop(0)
                            if y["Nom_KPI"]==kp:
                                vkpi.append(y["Valeurs_KPI_Entr"])
                                fkpi.append(y["Fct_KPI"])
                                skpi.append(y["Seuil_KPI_Entr"])

                        else:
                            if y["Nom_KPI"]==c:
                                vkpi.append(y["Valeurs_KPI"])
                                fkpi.append(y["Fct_KPI"])
                                skpi.append(y["Seuil_KPI"])
                        
        
        for i in combil:
            l=[]
            for y in i:
                l.append({"nom_kpi": y})
            ldic.append(l)   
        for i in ldic:
            
            for y in i :
                

                y["perf"]=pkpi[0]
                y["fct"]=fkpi[0]
                y["data"]=vkpi[0]
                y["seuil"]=skpi[0]

                
                
                pkpi.pop(0)
                fkpi.pop(0)
                vkpi.pop(0)
                skpi.pop(0)
                
            
        for i in ldic:
            if i[0]["perf"]==i[1]["perf"]:
                intra.append(i)
            else: 
                inter.append(i)
        ra=0
        er=1

        for i in range(0, len(inter)*2):
            looper.append(er)
            er+=2
        for i in range(0, len(intra)*2):
            loopra.append(ra)
            ra+=2
        
        ra=0
        er=1
        for i in inter:
            for k in i:
                k["id"]=er
                er+=2
           
        for i in intra:
            for k in i:
                k["id"]=ra
                ra+=2

        for k in intra:
            d1=k[0]["data"]
            c1=list(d1.values())
            d2=k[1]["data"]
            c2=list(d2.values())
            coef=np.corrcoef(c1, c2)
            
            if coef[0, 1] < 0:
                k[0]["lien"]="Negative correlation"
                k[1]["lien"]="Negative correlation"
            elif coef[0, 1] > 0 :
                k[0]["lien"]="Positive correlation"
                k[1]["lien"]="Positive correlation"
            else:
                k[0]["lien"]="Not linked"
                k[1]["lien"]="Not linked"
           
        
        for k in inter:
            d1=k[0]["data"]
            c1=list(d1.values())
            d2=k[1]["data"]
            c2=list(d2.values())
            coef=np.corrcoef(c1, c2)
            
            if coef[0, 1] < 0:
                k[0]["lien"]="Negative correlation"
                k[1]["lien"]="Negative correlation"
            elif coef[0, 1] > 0 :
                k[0]["lien"]="Positive correlation"
                k[1]["lien"]="Positive correlation"
            else:
                k[0]["lien"]="Not linked"
                k[1]["lien"]="Not linked"
        
        for i in intra:
            for j in i:
                j["sdata"]={}
                j["sseuil"]={}
                for val in range(int(period[0]), int(period[1])+1):
                    j["sdata"][val]=j['data'][str(val)]
                    j["sseuil"][val]=j['seuil'][str(val)]
        

        for val in intra:
            for i in val:
                i["ecart"]={}
                s= list(i['sseuil'].values())
                dd=list(i['sdata'].values())
                for k in i['sseuil'].keys():
                    i["ecart"][k]=dd[0]-s[0]
                    s.pop(0)
                    dd.pop(0)
        
        for i in inter:
            for j in i:
                j["sdata"]={}
                j["sseuil"]={}
                for val in range(int(period[0]), int(period[1])+1):
                    j["sdata"][val]=j['data'][str(val)]
                    j["sseuil"][val]=j['seuil'][str(val)]
        
                

        for val in inter:
            for i in val:
                i["ecart"]={}
                s= list(i['sseuil'].values())
                dd=list(i['sdata'].values())
                for k in i['sseuil'].keys():
                    i["ecart"][k]=dd[0]-s[0]
                    s.pop(0)
                    dd.pop(0)
                
                
        lienintra=[]
        lieninter=[]

        for val in inter:
            lieninter.append({
                    "kpi1": val[0]["nom_kpi"],
                    "kpi2": val[1]["nom_kpi"],
                    "lien": val[0]["lien"],
                })
        
        for val in intra:
            lienintra.append({
                    "kpi1": val[0]["nom_kpi"],
                    "kpi2": val[1]["nom_kpi"],
                    "lien": val[0]["lien"],
                })

        
        request.session['linkintra']=lienintra
        request.session['linkinter']=lieninter
                
       
               
        
        

        
        return render (request, 'home/evalperf.html', {'inter':inter, 'intra':intra, 'ldic':ldic, 'looper':looper, 'loopra':loopra})


def showlinks(request):
    if request.method=="POST":
        linkinter= request.session['linkinter']
        linkintra= request.session['linkintra']

        return render (request, 'home/showlinks.html', {'linkinter':linkinter, 'linkintra':linkintra})


@login_required(login_url="/login/")
def com(request):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["myNewDb"]
    colle = db["COMMERCIAL"]

    data_operateur = colle.find({})
    clonedata = data_operateur.clone()

    nb_clients_par_annees = {}
    CA_par_annees = {}
    CA_en_une_annees = 0
    somme_forfait_client = 0
    nb_clients_perdus_par_années = {}
    nb_clients_perdus_en_une_annees = 0

    abonnes=[]
    for x in clonedata:
        abonnes = x["Abonnes"]

    for an in range(2014, 2023):
        for x in abonnes:
            if x["Forfaits"] is not None and (len(x["Forfaits"]) > 0):
                for y in x["Forfaits"]:

                    forf_an = int(y["Date_Achat_Forfait"].split("-")[0])
                    if forf_an == an:
                        somme_forfait_client = somme_forfait_client + int(y["Prix_Forfait"])

                CA_en_une_annees = CA_en_une_annees + somme_forfait_client

        CA_par_annees[an] = CA_en_une_annees

    nb_client_en_une_annees = 0
    for an in range(2014, 2023):
        for x in abonnes:
            d_contrat = int((x["Contrat"]["Date_Debut_Contrat"]).split("-")[0])
            if d_contrat == an:
                if x["Résiliation"]["Date_Résiliation"] is None:
                    nb_client_en_une_annees = nb_client_en_une_annees + 1
                elif int((x["Résiliation"]["Date_Résiliation"]).split("-")[0]) != an:
                    nb_client_en_une_annees = nb_client_en_une_annees + 1
                else:
                    nb_clients_perdus_en_une_annees = nb_clients_perdus_en_une_annees + 1

        if an == 2014:
            nb_clients_par_annees[an] = nb_client_en_une_annees

        else:
            nb_clients_par_annees[an] = nb_client_en_une_annees + nb_clients_par_annees[an - 1]

        nb_clients_perdus_par_années[an] = nb_clients_perdus_en_une_annees

    labels=[]
    nbr_client=[]
    caffaire=[]
    for item in nb_clients_par_annees.keys():
        labels.append(item)

    for item in nb_clients_par_annees.values():
        nbr_client.append(item)
    for item in CA_par_annees.values():
        caffaire.append(item)

    return render(request, 'home/charts-commercial.html', {'labels': labels, 'nbr_client': nbr_client, 'CA':caffaire})






@csrf_exempt
def choixperflocal(request):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["myNewDb"]
    colle = db["Performance"]
    base = colle.find({})
    clone = base.clone()
    nperf=[]
    for i in base:

        perf=list(i.keys())

    perf.pop(0)
    dicperf={}
    for i in clone:
            
        for y in perf:
            nperf.append(i[y]["NomPerf"])
            dicperf[y]=i[y]["NomPerf"]

    if request.method=="POST":
        po= list(request.POST)
        po.pop(0)
        
        if len(po)>1 or len(po)==0:
            msgerror="You have to chose only one performance"

            return render(request, 'home/choixperflocal.html', {'dicperf':dicperf, 'msgerror':msgerror})
        else:
            request.session["cleperf"]=po
            
            return redirect(partprenlocal)


    else:
        
        return render(request, 'home/choixperflocal.html', {'dicperf':dicperf})


@csrf_exempt
def partprenlocal(request):
    
    dicperf=request.session["cleperf"]

    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["myNewDb"]
    colle = db["Performance"]
    base = colle.find({})
    clone = base.clone()
    clone2 = base.clone()
    lkpi=[]

    listkpi=[]
    partpren=[]
    p= request.session["cleperf"]
    p2= request.session["cleperf"]

    for h in clone2:
        for f in p2:
            nmeeval=h[f]["NomPerf"]
    
    request.session["nmperflocal"]=nmeeval
    

        
    request.session['perf']=p
    for x in clone:
        x.pop("_id")
        for y in p:
            lkpi.append(x.pop(y))
    for y in lkpi:
            listkpi.append(y.pop("ListeKPI"))
    for y in listkpi:
        for j in y :
            if j["Type"]==1:
                if not partpren:
                    partpren.append("Particulier")
                    partpren.append("Entreprise")
                else:
                    t=0
                    for i in partpren:
                        if i == "Particulier" or i == "Entreprise":
                            t=1
                            break
                    if t == 0:
                        partpren.append("Particulier")
                        partpren.append("Entreprise")
            elif j["Type"] == 2:
                if not partpren:
                    partpren.append("Employes")
                        
                else:
                    t=0
                    for i in partpren:
                        if i == "Employes":
                            t=1
                            break
                    if t == 0:
                        partpren.append("Employes")
            else:
                if not partpren:
                    partpren.append("Other")
                        
                else:
                    t=0
                    for i in partpren:
                        if i == "Other":
                            t=1
                            break
                    if t == 0:
                        partpren.append("Other")
    
       
    if request.method == "POST":
        po= list(request.POST)
        po.pop(0)
        
        if len(po)==0:
            msgerror="You have to chose at least one"

            return render(request, 'home/partprenlocal.html', {'partpren':partpren, 'msgerror':msgerror, 'nmeeval': nmeeval})
        else:
            request.session["partpren"]=po
            return redirect(attrlocal)

    else:
        return render(request, 'home/partprenlocal.html', {'partpren':partpren, 'nmeeval': nmeeval})       

@csrf_exempt
def attrlocal(request):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["myNewDb"]
    colle = db["Performance"]
    base = colle.find({})
    clone = base.clone()
    clone2 = base.clone()
    liskpi=[]
    kpi=[]
    lkpi=[]
    combil=[]
    ref=[]
    nmeperf=request.session["nmperflocal"]
    
    p= request.session["partpren"]
    dpk={}
    for i in p:
        dpk[i]=[]
    lp = request.session["perf"]

    for x in clone:
        x.pop("_id")
        for y in lp:
            liskpi.append(x.pop(y))
    for y in liskpi:
        kpi.append(y.pop("ListeKPI"))   

    for k in p:
        for y in kpi:
            for i in y :
                if k == "Particulier" and i["Type"]==1:
                    lkpi.append(i["Nom_KPI"])
                    dpk["Particulier"].append(i["Nom_KPI"])
                elif k == "Entreprise" and i["Type"]==1:
                    name=i["Nom_KPI"]+"_Ent"
                    lkpi.append(name)
                    dpk["Entreprise"].append(name)
                elif k == "Employes" and i["Type"]==2:
                    lkpi.append(i["Nom_KPI"])
                    dpk["Employes"].append(i["Nom_KPI"])
                elif k == "Other" and i["Type"]==3:
                    lkpi.append(i["Nom_KPI"])
                    dpk["Other"].append(i["Nom_KPI"])
    
    if request.method=="POST":
        po= list(request.POST)
        print(po)
        qo= dict(request.POST)
        po.pop(0)
        indicname=list(request.POST)
        indicname.pop(-1)
        indicname.pop(-1)
        

        
        if len(po)<4:
            msgerror="You have to chose at least two"

            return render(request, 'home/attrlocal.html', {"lkpi": lkpi, 'msgerror':msgerror, 'nmeperf': nmeperf})
        else:
            ldpk=list(dpk.keys())
            i=0
            while i<len(ldpk):
               
                trv=False
                lisv=dpk[ldpk[i]]
                y=0
                while trv==False and y<len(lisv):
                    
                    if lisv[y] in indicname:
                        trv=True
                        
                        
                    else:
                        y+=1
                        

                if trv==False:
                    
                    msgerror="Notice: you have to chose at least 1 indicators, per stockholder"
                    return render (request, 'home/attrlocal.html', {"lkpi": lkpi, 'msgerror': msgerror, 'nmeperf': nmeperf})
                
                i+=1



            request.session["lattrper"]=po
            request.session["diclattrper"]=qo
            print(qo)
            print(po)
            return redirect(evaluationperf)

        
        
    
    else:
        
        return render(request, 'home/attrlocal.html', {"lkpi": lkpi, 'nmeperf': nmeperf}) 


@csrf_exempt       
def evaluationperf(request):
    combil=[]
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["myNewDb"]
    colle = db["Performance"]
    base = colle.find({})
    clone = base.clone()
    for i in base:
        perf=list(i.keys())

    perf.pop(0)
    en="_Ent"
    tes=[]
    lkpi=[]
    vkpi=[]
    fkpi=[]
    skpi=[]
    pkpi=[]
    intra=[]
    inter=[]
    ldic=[]
    looper=[]
    loopra=[]
    ecar={}
    peri=[]

    
    p= request.session["lattrper"]
    q= request.session["diclattrper"]
    print("deb eval")
    print(p)
    

    period=p[-2:]
    p.pop(-1)
    p.pop(-1)
    for item in period:
        peri.append(q[item])
    
    for i in peri:
        for k in i:
            period.append(k)
    period.pop(0)
    period.pop(0)      
    
    combi = list(combinations(p , 2))
    for y in combi:
        combil.append(list(y))
    for x in clone:
        x.pop("_id")
        for i in perf:
            tes.append(x.pop(i))
    for x in tes:
        lkpi.append(x["ListeKPI"])
    for y in combil:
        for c in y:
            for x in tes:
                for i in x["ListeKPI"]:
                    if en in c:
                        kp=c.split('_Ent').pop(0)
                        if i["Nom_KPI"]==kp:
                            pkpi.append(x["NomPerf"])
                    else:
                        if i["Nom_KPI"]==c:
                            pkpi.append(x["NomPerf"])

    for i in combil:
        for c in i:
            for x in lkpi:
                for y in x:
                    if en in c:
                        kp=c.split('_Ent').pop(0)
                        if y["Nom_KPI"]==kp:
                            vkpi.append(y["Valeurs_KPI_Entr"])
                            fkpi.append(y["Fct_KPI"])
                            skpi.append(y["Seuil_KPI_Entr"])

                    else:
                        if y["Nom_KPI"]==c:
                            vkpi.append(y["Valeurs_KPI"])
                            fkpi.append(y["Fct_KPI"])
                            skpi.append(y["Seuil_KPI"])
                    
    
    for i in combil:
        l=[]
        for y in i:
            l.append({"nom_kpi": y})
        ldic.append(l)   
    for i in ldic:
        
        for y in i :
            

            y["perf"]=pkpi[0]
            y["fct"]=fkpi[0]
            y["data"]=vkpi[0]
            y["seuil"]=skpi[0]

            
            
            pkpi.pop(0)
            fkpi.pop(0)
            vkpi.pop(0)
            skpi.pop(0)
            
        
    for i in ldic:
        if i[0]["perf"]==i[1]["perf"]:
            intra.append(i)
        else: 
            inter.append(i)
    ra=0
    er=1

    for i in range(0, len(inter)*2):
        looper.append(er)
        er+=2
    for i in range(0, len(intra)*2):
        loopra.append(ra)
        ra+=2
    
    ra=0
    er=1
    for i in inter:
        for k in i:
            k["id"]=er
            er+=2
        
    for i in intra:
        for k in i:
            k["id"]=ra
            ra+=2

    for k in intra:
        d1=k[0]["data"]
        c1=list(d1.values())
        d2=k[1]["data"]
        c2=list(d2.values())
        coef=np.corrcoef(c1, c2)
        
        if coef[0, 1] < 0:
            k[0]["lien"]="Negative correlation"
            k[1]["lien"]="Negative correlation"
            k[0]["coefcor"]=str(coef[0, 1])
            k[1]["coefcor"]=str(coef[0, 1])
        elif coef[0, 1] > 0 :
            k[0]["lien"]="Positive correlation"
            k[1]["lien"]="Positive correlation"
            k[0]["coefcor"]=str(coef[0, 1])
            k[1]["coefcor"]=str(coef[0, 1])
        else:
            indice=0
            cause=True
            while indice<len(c1) and cause==True:
                v1=c1[indice+1]-c1[indice]
                v2=c2[indice+1]-c2[indice]
                if (v1>0 or v1<0) and (v2>0 or v2<0):
                    cause=True
                    indice+=1
                else:
                    cause=False
                    indice+=1
                   
            if cause==True:
                k[0]["lien"]="Causality"
                k[1]["lien"]="Causality"
            else:
                k[0]["lien"]="Not linked"
                k[1]["lien"]="Not linked"
        
    
    for k in inter:
        d1=k[0]["data"]
        c1=list(d1.values())
        d2=k[1]["data"]
        c2=list(d2.values())
        coef=np.corrcoef(c1, c2)
        
        if coef[0, 1] < 0:
            k[0]["lien"]="Negative correlation"
            k[1]["lien"]="Negative correlation"
            k[0]["coefcor"]=str(coef[0, 1])
            k[1]["coefcor"]=str(coef[0, 1])
        elif coef[0, 1] > 0 :
            k[0]["lien"]="Positive correlation"
            k[1]["lien"]="Positive correlation"
            k[0]["coefcor"]=str(coef[0, 1])
            k[1]["coefcor"]=str(coef[0, 1])
        else:
            indice=0
            cause=True
            while indice<len(c1) and cause==True:
                v1=c1[indice+1]-c1[indice]
                v2=c2[indice+1]-c2[indice]
                if (v1>0 or v1<0) and (v2>0 or v2<0):
                    cause=True
                    indice+=1
                else:
                    cause=False
                    indice+=1
                   
            if cause==True:
                k[0]["lien"]="Causality"
                k[1]["lien"]="Causality"
            else:
                k[0]["lien"]="Not linked"
                k[1]["lien"]="Not linked"
    
    for i in intra:
        for j in i:
            j["sdata"]={}
            j["sseuil"]={}
            for val in range(int(period[0]), int(period[1])+1):
                j["sdata"][val]=j['data'][str(val)]
                j["sseuil"][val]=j['seuil'][str(val)]
    

    for val in intra:
        for i in val:
            i["ecart"]={}
            s= list(i['sseuil'].values())
            dd=list(i['sdata'].values())
            for k in i['sseuil'].keys():
                i["ecart"][k]=dd[0]-s[0]
                s.pop(0)
                dd.pop(0)
    
    for i in inter:
        for j in i:
            j["sdata"]={}
            j["sseuil"]={}
            for val in range(int(period[0]), int(period[1])+1):
                j["sdata"][val]=j['data'][str(val)]
                j["sseuil"][val]=j['seuil'][str(val)]
    
            

    for val in inter:
        for i in val:
            i["ecart"]={}
            s= list(i['sseuil'].values())
            dd=list(i['sdata'].values())
            for k in i['sseuil'].keys():
                i["ecart"][k]=dd[0]-s[0]
                s.pop(0)
                dd.pop(0)
            
            
    lienintra=[]
    lieninter=[]

    for val in inter:
        if val[0]["lien"]=="Negative correlation" or val[0]["lien"]=="Positive correlation":
            lieninter.append({
                    "kpi1": val[0]["nom_kpi"],
                    "perf1": val[0]["perf"],
                    "kpi2": val[1]["nom_kpi"],
                    "perf2": val[1]["perf"],
                    "lien": val[0]["lien"]+" with a coefficient of ("+val[0]["coefcor"]+")",
                })
        else:
            lieninter.append({
                    "kpi1": val[0]["nom_kpi"],
                    "perf1": val[0]["perf"],
                    "kpi2": val[1]["nom_kpi"],
                    "perf2": val[1]["perf"],
                    "lien": val[0]["lien"],
                })

    
    for val in intra:
        if val[0]["lien"]=="Negative correlation" or val[0]["lien"]=="Positive correlation":
            lienintra.append({
                    "kpi1": val[0]["nom_kpi"],
                    "perf1": val[0]["perf"],
                    "kpi2": val[1]["nom_kpi"],
                    "perf2": val[1]["perf"],
                    "lien": val[0]["lien"]+" with a coefficient of ("+val[0]["coefcor"]+")",
                })
        else:

            lienintra.append({
                    "kpi1": val[0]["nom_kpi"],
                    "perf1": val[0]["perf"],
                    "kpi2": val[1]["nom_kpi"],
                    "perf2": val[1]["perf"],
                    "lien": val[0]["lien"],
                })

    
    request.session['linkintra']=lienintra
    request.session['linkinter']=lieninter
            
    
               
        


    return render (request, 'home/evaluationperf.html', {'inter':inter, 'intra':intra, 'ldic':ldic, 'looper':looper, 'loopra':loopra})

@csrf_exempt       
def attrglobal(request):

    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["myNewDb"]
    colle = db["Performance"]
    base = colle.find({})
    clone = base.clone()
    clone2 = base.clone()
    lnkpi=[]
    d={}
    dd={}
    for i in base:
        perf=list(i.keys())
    perf.pop(0)
    perf2=perf

    for i in clone:
    
        for y in perf:
            dl=[]
            
            for n in i[y]["ListeKPI"]:
                lnkpi.append(n["Nom_KPI"])
                dl.append(n["Nom_KPI"])
                if n["Type"]==1:
                    name=n["Nom_KPI"]+"_Ent"
                    lnkpi.append(name)
                    dl.append(name)

            
            d[y]=dl

    print(d)

    for i in clone2:
        for y in d.keys():
            dd[i[y]["NomPerf"]]={y: d[y]}
    print(dd)

    if request.method=="POST":
        po= list(request.POST)
        
        qo= dict(request.POST)
        po.pop(0)
        print("hiiiiiiiiiiiiiiiiiiiiiii")
        print(qo)
        print(po)
        val=list(qo.values())
        val.pop(0)
        val.pop(-1)
        val.pop(-1)
        
        val2=[]
        for v in val:
            val2.append(v[0])
        r=0
        for v in perf2:
            if v in val2:
                r+=1
        
        if r>=4:
            request.session["lattrper"]=po
            request.session["diclattrper"]=qo
            print(qo)
            print(po)
            return redirect(evaluationperf)
        else:
            msgerror="Notice: you have to chose at least 1 from each performance"
            return render (request, 'home/attrglobal.html', {'dd':dd, 'msgerror': msgerror})



        


    


    return render (request, 'home/attrglobal.html', {'dd':dd})

@csrf_exempt
def choixperagg(request):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["myNewDb"]
    colle = db["Performance"]
    base = colle.find({})
    clone = base.clone()
    nperf=[]
    for i in base:

        perf=list(i.keys())

    perf.pop(0)
    dicperf={}
    for i in clone:
            
        for y in perf:
            nperf.append(i[y]["NomPerf"])
            dicperf[y]=i[y]["NomPerf"]

    if request.method=="POST":
        po= list(request.POST)
        po.pop(0)
        
        if len(po)<=1 or len(po)==len(perf):
            msgerror="You have to chose at least two performances and at most all minus one"

            return render(request, 'home/choixperagg.html', {'dicperf':dicperf, 'msgerror':msgerror})
        else:
            request.session["cleperf"]=po
            
            return redirect(partprenagg)


    else:
        
        return render(request, 'home/choixperagg.html', {'dicperf':dicperf})

    
@csrf_exempt
def partprenagg(request):
    
    dicperf=request.session["cleperf"]

    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["myNewDb"]
    colle = db["Performance"]
    base = colle.find({})
    clone = base.clone()
    clone2=base.clone()
    lkpi=[]

    listkpi=[]
    partpren=[]
    p= request.session["cleperf"]
        
    request.session['perf']=p
    for x in clone:
        x.pop("_id")
        for y in p:
            lkpi.append(x.pop(y))
    for y in lkpi:
            listkpi.append(y.pop("ListeKPI"))
    for y in listkpi:
        for j in y :
            if j["Type"]==1:
                if not partpren:
                    partpren.append("Particulier")
                    partpren.append("Entreprise")
                else:
                    t=0
                    for i in partpren:
                        if i == "Particulier" or i == "Entreprise":
                            t=1
                            break
                    if t == 0:
                        partpren.append("Particulier")
                        partpren.append("Entreprise")
            elif j["Type"] == 2:
                if not partpren:
                    partpren.append("Employes")
                        
                else:
                    t=0
                    for i in partpren:
                        if i == "Employes":
                            t=1
                            break
                    if t == 0:
                        partpren.append("Employes")
            else:
                if not partpren:
                    partpren.append("Other")
                        
                else:
                    t=0
                    for i in partpren:
                        if i == "Other":
                            t=1
                            break
                    if t == 0:
                        partpren.append("Other")
    
       
    if request.method == "POST":
        po= list(request.POST)
        po.pop(0)
        dicperfpart={}
        for i in p:
            dicperfpart[i]=[]
        
        for i in clone2:
            for y in p:
                for n in i[y]["ListeKPI"]:
                    if n["Type"]==1:
                        dicperfpart[y].append("Particulier")
                       
                        dicperfpart[y].append("Entreprise")
                    if n["Type"]==2:
                        
                        dicperfpart[y].append("Employes")
                    if n["Type"]>2:
                       
                        dicperfpart[y].append("Other")
        print(dicperfpart)
        for y in p:
            i=0
            trv=False
            while i<len(dicperfpart[y]) and trv==False:
                if dicperfpart[y][i] in po:
                    trv=True
                else:
                    i+=1
            
            if trv==False:
                msgerror="You have to chose at least one stakeholder per performance chosed"

                return render(request, 'home/partprenagg.html', {'partpren':partpren, 'msgerror':msgerror})


                    


        
        
        request.session["partpren"]=po
        return redirect(attragg)

        

    else:
        return render(request, 'home/partprenagg.html', {'partpren':partpren})



@csrf_exempt       
def attragg(request):

    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["myNewDb"]
    colle = db["Performance"]
    base = colle.find({})
    clone = base.clone()
    clone2 = base.clone()
    clone3 = base.clone()
    liskpi=[]
    kpi=[]
    lkpi=[]
    combil=[]
    ref=[]
    dicperfindic={}
    dd={}
    p=1
    p= request.session["partpren"]
    dpk={}
    for i in p:
        dpk[i]=[]
    
    lp = request.session["perf"]
    print("lpppppppppppppppppppppppppp")
    print(lp)
    nbperf=False
    nbpartpren=False
    for x in clone:
        x.pop("_id")
        for y in lp:
            liskpi.append(x.pop(y))
    for y in liskpi:
        kpi.append(y.pop("ListeKPI"))   

    for k in p:
        for y in kpi:
            for i in y :
                if k == "Particulier" and i["Type"]==1:
                    lkpi.append(i["Nom_KPI"])
                    dpk["Particulier"].append(i["Nom_KPI"])
                elif k == "Entreprise" and i["Type"]==1:
                    name=i["Nom_KPI"]+"_Ent"
                    lkpi.append(name)
                    dpk["Entreprise"].append(name)
                elif k == "Employes" and i["Type"]==2:
                    lkpi.append(i["Nom_KPI"])
                    dpk["Employes"].append(i["Nom_KPI"])
                elif k == "Other" and i["Type"]==3:
                    lkpi.append(i["Nom_KPI"])
                    dpk["Other"].append(i["Nom_KPI"])
    
    for i in lp:
        dicperfindic[i]=[]

    
    for i in clone2:
        
        for y in lp:
            for n in i[y]["ListeKPI"]:
                if n["Type"]==1:
                    name=n["Nom_KPI"]+"_Ent"
                    if name in lkpi:
                        dicperfindic[y].append(name)
                    if n["Nom_KPI"] in lkpi:
                        dicperfindic[y].append(n["Nom_KPI"])
                elif n["Nom_KPI"] in lkpi:
                    dicperfindic[y].append(n["Nom_KPI"])

    
    for i in clone3:
        for y in dicperfindic.keys():
            dd[i[y]["NomPerf"]]={y: dicperfindic[y]}

    if request.method=="POST":
        po= list(request.POST) #nom indicateur
        print("deb req")
        print(po)
        qo= dict(request.POST)
        po.pop(0)
        
        indicname=list(request.POST)
        indicname.pop(-1)
        indicname.pop(-1)
        print('0')
        print(po)
        
        val=list(qo.values())
        val.pop(0)
        val.pop(-1)
        val.pop(-1)
        
        val2=[]
        for v in val:
            val2.append(v[0])
        r=0
        
        for v in lp:
            if v in val2:
                r+=1
        
        if r >= len(lp):
            
            ldpk=list(dpk.keys())
            i=0
            while i<len(ldpk):
               
                trv=False
                lisv=dpk[ldpk[i]]
                y=0
                while trv==False and y<len(lisv):
                    
                    if lisv[y] in indicname:
                        trv=True
                        
                        
                    else:
                        y+=1
                        

                if trv==False:
                    
                    msgerror="Notice: you have to chose at least 1 indicators, per stockholder per performance"
                    return render (request, 'home/attragg.html', {"dd": dd, 'msgerror': msgerror})
                
                i+=1
            
            request.session["lattrper"]=po
            print(po)
            request.session["diclattrper"]=qo
            return redirect(evaluationperf)
            

        else:
            msgerror="Notice: you have to chose at least 1 indicator per performance"
            return render (request, 'home/attragg.html', {"dd": dd, 'msgerror': msgerror})
    

    return render (request, 'home/attragg.html', {"dd": dd})


@csrf_exempt  
def fixthresholds(request):

    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["myNewDb"]
    colle = db["Performance"]
    base = colle.find({})
    clone = base.clone()
    clone2 = base.clone()
    lnkpi=[]
    nomperform={}
    dicdic={}
    d={}
    for i in base:
        perf=list(i.keys())
    perf.pop(0)
    perf2=perf
    for i in clone2:
        for y in perf:
            nomperform[y]=i[y]["NomPerf"]
        

    for i in clone:
    
        for y in perf:
            dl=[]
            
            for n in i[y]["ListeKPI"]:
                lnkpi.append(n["Nom_KPI"])
                dl.append(n["Nom_KPI"])
                if n["Type"]==1:
                    name=n["Nom_KPI"]+"_Ent"
                    lnkpi.append(name)
                    dl.append(name)

            
            d[y]=dl
   
    for i in perf:
        dicdic[i]={}
    
    for i in perf:
        dicdic[i]["nomperf"]=nomperform[i]
    
    for i in perf:
        dicdic[i]["lk"]=d[i]
    
    print(dicdic)


    if request.method=="POST":
        donnee= list(request.POST)
        donnee.pop(0)
        dovalues=dict(request.POST)
        year=datetime.today().strftime('%Y')
        print(type(year))
        for t in donnee:
            if dovalues[t][0]=="":
                msg="You have to fix all the tresholds"
                return render (request, 'home/fixthresholds.html', {"dicdic":dicdic, "msg":msg})
            

        myclient2 = MongoClient('localhost', 27017)
       

        where = myclient2.myNewDb.Performance
        
        for x in donnee:
            pa=x.split(",")
            
            if "_Ent" in pa[1]:
                name=pa[1]
                name=(name.split("_Ent"))[0]
                where.update_one({pa[0]+".ListeKPI.Nom_KPI": name}, {'$set': {pa[0]+".ListeKPI.$.Seuil_KPI_Entr."+year: int(dovalues[x][0])}})
            
            else:


                where.update_one({pa[0]+".ListeKPI.Nom_KPI": pa[1]}, {'$set': {pa[0]+".ListeKPI.$.Seuil_KPI."+year: int(dovalues[x][0])}})
        
        msg="Values saved"
        
        return render (request, 'home/fixthresholds.html', {"dicdic":dicdic, "msg":msg})
    return render (request, 'home/fixthresholds.html', {"dicdic":dicdic})



@csrf_exempt
def addattribut(request):

    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["myNewDb"]
    colle = db["Classes"]
    base = colle.find({})
    clone = base.clone()
    for i in clone:

        classes=i['Name']

    if request.method=="POST":
        dicform=dict(request.POST)
        print(dicform)
        classname=dicform["classname"][0]
        conn = pymongo.MongoClient("mongodb://localhost:27017/")
        db = conn["myNewDb"]
        collection = db["OPERATEUR"]
        x=collection.find()

        attrname= dicform["attributname"][0]

        synonym= dicform["synonym"][0]

        attrib=[]



        for i in x:
            base=i
        
        path=[]
        found=0
        def findpath(bdd, classname, classes, chemin, found):

            global zutter
            for i in bdd:
                
                if i==classname:
                    
                    chemin.append(i)
                    
                    
                    if type(bdd[i])==list:
                        chemin.append('$')
                        fil=list(bdd[i][0].keys())
                        
                        chemin.append(fil[0])
                        found=1
                        
                        zutter=tuple(chemin)
                        
                        return chemin
                    else:
                        
                        found=1 
                        fil=list(bdd[i].keys())
                        
                        chemin.append(fil[0])
                        
                        zutter=tuple(chemin)
                        
                        return chemin
                else:
                    if i in classes:
                        chemin.append(i)
                        if type(bdd[i])==list:

                            chemin.append('$')
                            findpath(bdd[i][1], classname, classes, chemin, found)
                        else:
                            findpath(bdd[i], classname, classes, chemin, found)
            if found==0:
                print(chemin)
                if chemin[-1]=='$':
                    chemin.pop()
                    chemin.pop()
                    
                else:
                    chemin.pop()


        def filters( bdd, lattr, path):
    
            if type(bdd)==list:
                lattexi=list(bdd[0].keys())
                if path[-1] in lattexi:
                    for i in bdd:
                        
                        lattr.append(i[path[-1]])
                    return lattr
                else:
                    path.pop(0)
                    path.pop(0)
                    
                    for i in bdd:
                        
                        filters(i[path[0]], lattr, path.copy())
            else:
                
                lattexi=list(bdd.keys())
                
                if path[-1] in lattexi:
                    
                        
                    lattr.append(bdd[path[-1]])
                    return lattr
                else:
                    
                    path.pop(0)
                    
                    filters(bdd[path[0]], lattr, path.copy())


        findpath(base, classname, classes, path, found)

        z=list(zutter)

        zclone=[]
        for i in z:
            if i!= '$':
                zclone.append(i)


        li=[]
        filters(base[zclone[0]], li, z.copy())


        filtr=zclone[0]         

        for i in range(1,len(zclone)):
            filtr=filtr+"."+zclone[i]

        chem=z[0]
        for i in range(1,len(z)-1):
            chem=chem+"."+z[i]

        chem=chem+"."+attrname
        
        namefile=str(dicform["filename"][0])
        filepath='/home/nassim/Desktop/telecom/apps/static/FilesCSV/'+namefile

        existe=True

        with open('/home/nassim/Desktop/telecom/apps/static/FilesCSV/'+namefile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            test=0
            for row in csv_reader:
                if line_count == 0:
                    line_count+=1
                elif line_count == 1:
                    listattr=row
                    print(listattr)
                    try:
                        i= listattr.index(attrname)
                    except:
                        try:
                            i= listattr.index(synonym)
                        except:
                            existe=False
                            break
                    line_count+=1
                        
                elif line_count>1:
                    attrib.append(row[i])
                else:
                    break

        for i in range(0, len(li)):

            collection.update_one({filtr:li[i]}, {"$set": {chem: attrib[i]}})
        
        


        return render(request, 'home/addattribut.html', {'classes':classes})

    


       
        
        
        
        
        
    return render(request, 'home/addattribut.html', {'classes':classes})


@csrf_exempt
def addclass(request):

    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["myNewDb"]
    colle = db["Classes"]
    base = colle.find({})
    clone = base.clone()
    cloneclass=base.clone()
    for i in clone:

        classes=i['Name']
    
    if request.method=="POST":
        dicform=dict(request.POST)
        nomclass=dicform["classname"][0]
        listeclasseassos=[] 
        listeclasseassos.append(dicform["classnameassos"][0])

        conn = pymongo.MongoClient("mongodb://localhost:27017/")
        db = conn["myNewDb"]
        collection = db["OPERATEUR"]
        x=collection.find()

        for i in x:
            base=i   #bdd operateur

        conn2 = pymongo.MongoClient("mongodb://localhost:27017/")
        db2 = conn2["myNewDb"]
        collection2 = db2["Classes"]
        x2=collection2.find()

        for i in x2:
            classes=i["Name"]  #classes name that exist

        def findpath(bdd, classname, classes, chemin, found):
            global zutter
            for i in bdd:
                
                if i==classname:
                    
                    chemin.append(i)
                    
                    
                    if type(bdd[i])==list:
                        chemin.append('$')
                        fil=list(bdd[i][0].keys())
                        
                        chemin.append(fil[0])
                        found=1
                        
                        zutter=tuple(chemin)
                        
                        return chemin
                    else:
                        
                        found=1 
                        fil=list(bdd[i].keys())
                        
                        chemin.append(fil[0])
                        
                        zutter=tuple(chemin)
                        
                        return chemin
                else:
                    if i in classes:
                        chemin.append(i)
                        if type(bdd[i])==list:

                            chemin.append('$')
                            findpath(bdd[i][1], classname, classes, chemin, found)
                        else:
                            findpath(bdd[i], classname, classes, chemin, found)
            if found==0:
                
                if chemin[-1]=='$':
                    chemin.pop()
                    chemin.pop()
                    
                else:
                    chemin.pop()

        def filters( bdd, lattr, path):
            
            if type(bdd)==list:
                lattexi=list(bdd[0].keys())
                if path[-1] in lattexi:
                    for i in bdd:
                        
                        lattr.append(i[path[-1]])
                    return lattr
                else:
                    path.pop(0)
                    path.pop(0)
                    
                    for i in bdd:
                        
                        filters(i[path[0]], lattr, path.copy())
            else:
                
                lattexi=list(bdd.keys())
                
                if path[-1] in lattexi:
                    
                        
                    lattr.append(bdd[path[-1]])
                    return lattr
                else:
                    
                    path.pop(0)
                    
                    filters(bdd[path[0]], lattr, path.copy())

        #etape 1 ajouter la classe vide aux classe selectionner
        for n in listeclasseassos:
            path=[]
            found=0
            
            
                
                        
                

            findpath(base, n, classes, path, found)



            z=list(zutter)
            print("2",z)
            zclone=[]
            for i in z:
                if i!= '$':
                    zclone.append(i)

            li=[]
            filters(base[zclone[0]], li, z.copy())
            
            

            


            filtr=zclone[0]         

            for i in range(1,len(zclone)):
                filtr=filtr+"."+zclone[i]

            chem=z[0]
            for i in range(1,len(z)-1):
                chem=chem+"."+z[i]


            chem=chem+"."+nomclass


            dicnary={}
            listattr=[]

            for i in range(0, len(li)):
                dicnary[i]={}

            namefile=str(dicform["filename"][0])
            filepath='/home/nassim/Desktop/telecom/apps/static/FilesCSV/'+namefile
            

            with open('/home/nassim/Desktop/telecom/apps/static/FilesCSV/'+namefile) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                test=0
                indice=0
                for row in csv_reader:
                    if line_count == 0:
                        line_count+=1
                    elif line_count == 1:
                        listattr=row
                        
                        
                        line_count+=1
                            
                    elif line_count>1:
                        
                        for col in range(0, len(listattr)):
                            dicnary[indice][listattr[col]]=row[col]
                            
                        indice+=1    
                    else:
                        break




            for i in range(0, len(li)):

                collection.update_one({filtr:li[i]}, {"$set": {chem: dicnary[i]}})
            for r in cloneclass:
                iddd=r["_id"]
            
            colle.update_one({"_id":iddd}, {"$push": {"Name": nomclass}})
            client1 = pymongo.MongoClient("mongodb://localhost:27017")
            db1 = client1["myNewDb"]
            colle1 = db1["Classes"]
            base1 = colle1.find({})
            clone11 = base1.clone()
            for i in clone11:

                classes=i['Name']
            
            
            return render(request, 'home/addclass.html', {'classes':classes})

    


    return render(request, 'home/addclass.html', {'classes':classes})


#newwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww


myclient = MongoClient('localhost', 27017)
def _AjoutAxe(request):
    Name_Axis = request.POST.get("NameAxis", None)

    print(Name_Axis)
    if request.method == "POST":


        #ajout l'axe dans le ref
        Collection_Performance = myclient.myNewDb.get_collection("Performance")
        NameAxe=Name_Axis.lower()
        List_performances = list(Collection_Performance.find())

        # verifier d'abord l'existance de l'axe
        if(NameAxe in List_performances[0]):
            print("existing...")
        else :
            #inserer l'axe dans ce cas
            Collection_Performance.update(
                { },
                {"$set": {NameAxe:{"NomPerf":NameAxe,  "ListeKPI": [],}
                    }
                }
            )

        # ajout l'axe dans le metadonnes

        CollectionMetadonnees = myclient.myNewDb.get_collection("Metadonnees")
        Metadonnees = list(CollectionMetadonnees.find())[0]
        Metadonnees.pop("_id")
        Metadata = []
        for x in Metadonnees:
            Metadata.append({'Nom_Axe': x, 'Liste_KPI': ','.join(map(str, Metadonnees[x]['Liste_KPI'])).lower(),
                                 'Liste_Attributes': ' , '.join(map(str, Metadonnees[x]['Liste_Attributes'])),
                                 'Stakeholders': ' , '.join(map(str, Metadonnees[x]['Stakeholders']))})

        NameAxe = NameAxe.lower().strip()

        # verifier d'abord l'existance de l'axe dans le metadonnes
        listAxeExistants = []
        for i in Metadata:
            listAxeExistants.append(i['Nom_Axe'])

        if (NameAxe in listAxeExistants):
            print("existing...")
        else:
            CollectionMetadonnees.update_one(
                {},
                {"$set": {NameAxe: {"Liste_KPI": [], "Liste_Attributes": [], "Stakeholders": []}
                   }
                 }
            )


    return render(request, "home/TableReferentiel.html")





myclient = MongoClient('localhost', 27017)
collection = myclient.myNewDb.get_collection("OPERATEUR")

xx = collection.find()
classes = ["Contrat", "Abonnes", "Employés", "Reclamation","Antenne","Resiliation","Absences", "Concurrent","Reseau_Social_Operateur" ,"Contrat", "Service", "Avis_Employe", "Forfaits"]

for i in xx:
    base = i

import random

path = []
found = 0
zutter = ()
def findpath(bdd, NameAttr, classes, chemin, found):
    global zutter

    for i in bdd:
        if i == NameAttr:

            chemin.append(i)
            if type(bdd[i]) == list:
                # chemin.append('$')

                found = 1
                # print(chemin)

                zutter = tuple(chemin)

                return chemin
            else:

                found = 1
                # print(chemin)

                zutter = tuple(chemin)

                return chemin
        else:

            if i in classes:
                chemin.append(i)
                if type(bdd[i]) == list:

                    # chemin.append('$')
                    findpath(bdd[i][0], NameAttr, classes, chemin, found)
                else:
                    findpath(bdd[i], NameAttr, classes, chemin, found)
    if found == 0:

        if chemin[-1] == '$':
            chemin.pop()
            chemin.pop()

        else:
            chemin.pop()


def ChooseDate(attribute,NameCollection):
    date="null"
    print("choose date")
    print(attribute)
    if(attribute=="Incomes" or attribute== "Type_Client"):
        date="$Abonnes.Contrat.Date_Debut_Contrat"

    elif(attribute=="idEntr"  or attribute== "idPart"):
        date="$Abonnes.Date"

    elif(attribute=="likes" or attribute== "comments" or attribute== "shares"):
        date="$Reseau_Social_Operateur.Publication.Date_Publ"

    elif(attribute=="Speed_of_Answer" or attribute=="Call_Duration"  or attribute== "Complaints" or attribute=="Satisfaction_rating" ):
        date="$Abonnes.Reclamation.Date_Call" #"Satisfaction_rating" #pour réclamation

    elif(attribute == "Type_Service" or attribute=="SMS" or attribute=="Calls" or attribute=="Internet"):
        date="$Abonnes.Service.Date_Service"

    elif(attribute=="Package_price" or attribute=="Package_duration"): #forfaits
        date="$Abonnes.Forfaits.Date_Achat_Forfait"



    elif(attribute=="Avis_Rating"):
        date="$Employés.Avis_Employe.Date_Avis"

    elif(attribute=="Nbr_Completed_Tasks" or attribute == "Salary"or attribute == "Date_Debut_Travail" or attribute=="Nbr_unfinished_Tasks" or attribute=="Employee_Rating"):
        date = "$Employés.Date_Debut_Travail"

    elif (attribute == "Resiliation"):
        date= "$Abonnes.Resiliation.Date_Resiliation"

    elif (attribute == "Date_Demission"):
        print("okk")
        date= "$Employés.Date_Demission"

    elif(attribute=="Date_Absence"):
        date="$Employés.Absences.Date_Absence"

    elif(attribute=="Antenne" or attribute=="Antenne_Frequency"):
        date="$Antenne.Date_Installation"


    elif(date=="null"):
        if(NameCollection=="$Abonnes"):
            date="$Abonnes.Contrat.Date_Debut_Contrat"
        elif(NameCollection=="$Employés"):
            date = "$Employés.Date_Debut_Travail"
        elif(NameCollection=="$Antenne"):
            date="$Antenne.Date_Installation"
        elif(NameCollection=="Service"):
            date="$Abonnes.Service.Date_Service"
        elif(NameCollection=="Forfaits"):
            date="$Abonnes.Forfaits.Date_Achat_Forfait"
        elif(NameCollection=="Reclamation"):
            date="$Abonnes.Reclamation.Date_Call"
        elif(NameCollection=="Absences"):
            date="$Employés.Absences.Date_Absence"
        else:
            date="$Abonnes.Date"

    return date

def PathAttribut():

    path=list(zutter)
    p = []
    for i in path:
        i = i.replace("$", "")
        if (i in p):
            pass
        else:
            p.append(i)
    print(p)

    PathAttribut="$"
    a=0
    for i in p:
        a+=1
        if(a<len(p)):
            PathAttribut=PathAttribut+i+"."
        else:
            PathAttribut = PathAttribut + i

    print(PathAttribut)

    return PathAttribut



def NomAttribut(NomAttr):

        print(NomAttr)
        if(NomAttr=="idEntr"):
            nom="idEntr"
        elif(NomAttr=="idPart"):
            nom = "idPart"
        elif(NomAttr=="Incomes"):
            nom = "CA"
        elif(NomAttr=="work_start_date"):
            nom = "Date_Debut_Travail"
        elif(NomAttr=="unsubscription"):
            nom = "Resiliation"
        elif(NomAttr=="Complaints"):
            nom = "Date_Call"
        elif(NomAttr=="Package_duration"):
            nom = "Duree_Forfait"
        elif(NomAttr=="Package_price"):
            nom = "Prix_Forfait"
        elif(NomAttr=="Resolved"):
            nom = "Resolved"
        elif(NomAttr=="Subscribers_satisfaction_rating"):
            nom = "Satisfaction_rating"
        elif(NomAttr=="Salary"):
            nom = "Salaire"
        elif(NomAttr=="Nbr_unfinished_Tasks"):
            nom ="Nbr_Taches_Non_Accompl"
        elif(NomAttr=="Nbr_Completed_Tasks"):
            nom = "Nbr_Taches_Accomplies_a_Temps"
        elif(NomAttr=="Resignation"):
            nom = "Date_Demission"
        elif(NomAttr=="Employee_satisfaction_rating"):
            nom = "Avis_Rating"
        elif(NomAttr=="shares"):
            nom = "Nbr_Partages"
        elif(NomAttr=="likes"):
            nom = "Nbr_likes"
        elif(NomAttr=="comments"):
            nom = "Nbr_Comments"
        elif(NomAttr=="Antenne_Frequency"):
            nom = "Frequence"
        elif(NomAttr=="SMS"):
            nom = "SMS"
        elif(NomAttr=="Calls"):
            nom = "Appel"
        elif(NomAttr=="Internet"):
            nom = "Internet"
        elif(NomAttr=="Internet"):
            nom = "Volume_Internet"
        elif(NomAttr=="Services"):
            nom = "Nom_Service"
        elif(NomAttr=="Date_Absence"):
            nom = "Date_Absence"
        elif(NomAttr=="Call_Duration"):
            nom = "Avg_Call_Duration"

        else:

            nom=NomAttr

        return nom




def CalculAttribut(NameAttribute, FctAggregation):

    print("NameAttribute")
    print(NameAttribute)
    NameAttr=NomAttribut(NameAttribute)
    print(NameAttr)

    findpath(base, NameAttr, classes, path, found)
    pathAttribute = PathAttribut()
    print(pathAttribute)

    print(FctAggregation)

    if(NameAttr=="Contrat" or NameAttr=="Resiliation" ):
        FctAggregation="count"

    path.clear()


    Lpath = pathAttribute.split('.')
    print("lpath")
    print(Lpath)
    print(len(Lpath))
    if(len(Lpath) == 3):
        NameCollection=Lpath[1]

    else:
        NameCollection = Lpath[0]

    print("NameCollection")
    print(NameCollection)
    date = ChooseDate(NameAttr, NameCollection)
    print("daaate")
    print(date)


    resultat = {}
    listVal = {}

    if (len(Lpath) == 3):

        if(pathAttribute==date):
            print("count")
            for j in list( Operateur.aggregate([
                {"$unwind": Lpath[0]},
                {"$unwind": Lpath[0] + "." + Lpath[1]},
                {"$group": {
                    "_id": {"date": {"$substr": [date, 0, 4]}},
                    "sum": {"$sum": 1},}},
                {"$sort": {"_id": 1}},
            ])):
                               if(j["_id"]["date"].isnumeric()):
                                   if (type(j[FctAggregation]) is float):
                                        val = round(j[FctAggregation], 2)
                                        listVal.update({j["_id"]["date"]:val})

                                   else:
                                       listVal.update({j["_id"]["date"]:j[FctAggregation]})

        else:
            if(FctAggregation=="sum"):

                for j in list( Operateur.aggregate([
                    {"$unwind": Lpath[0]},
                    {"$unwind": Lpath[0] + "." + Lpath[1]},
                        {"$group": {

                                 "_id": {"date": {"$substr": [date, 0, 4]}},
                                 "sum": {"$sum": {"$sum": pathAttribute}},

                        }},
                        {"$sort": {"_id": 1}},
                    ])):
                        if (j["_id"]["date"].isnumeric()):
                            if(type(j[FctAggregation]) is float):
                                val = round(j[FctAggregation], 2)
                                listVal.update({j["_id"]["date"]: val})
                            else:
                                listVal.update({j["_id"]["date"]: j[FctAggregation]})



            elif(FctAggregation=="avg"):

                for j in list( Operateur.aggregate([
                {"$unwind": Lpath[0]},
                {"$unwind": Lpath[0] + "." + Lpath[1]},
                    {"$group": {
                             "_id": {"date": {"$substr": [date, 0, 4]}},
                              "avg": {"$avg": {"$avg": pathAttribute}},
                    }},
                    {"$sort": {"_id": 1}},
                ])):


                    if (j["_id"]["date"].isnumeric()):
                        if (type(j[FctAggregation]) is float):
                            val = round(j[FctAggregation], 2)
                            listVal.update({j["_id"]["date"]: val})
                        else:
                            listVal.update({j["_id"]["date"]: j[FctAggregation]})


            elif(FctAggregation=="count"):
                for j in list( Operateur.aggregate([
                {"$unwind": Lpath[0]},
                {"$unwind": Lpath[0] + "." + Lpath[1]},
                    {"$group": {
                             "_id": {"date": {"$substr": [date, 0, 4]}},
                             "count": {"$sum":1 },
                    }},
                    {"$sort": {"_id": 1}},
                ])):

                    if (j["_id"]["date"].isnumeric()):
                        if (type(j[FctAggregation]) is float):
                           val = round(j[FctAggregation], 2)
                           listVal.update({j["_id"]["date"]: val})
                        else:
                          listVal.update({j["_id"]["date"]: j[FctAggregation]})




            """for i in list(resultat):
                               
                               if (i["_id"]["date"].isnumeric()):
                                   if (type(i[FctAggregation]) is float):
                                        val = round(i[FctAggregation], 2)
                                        listVal.update({i["_id"]["date"]:val})

                                   else:
                                       listVal.update({i["_id"]["date"]:i[FctAggregation]})

                                   print(listVal)"""

    else:
      print("inferieur à < 3")
      if (pathAttribute == date):

        resultat = Operateur.aggregate([
            {"$unwind": NameCollection},
            {"$group": {
                "_id": {
                    "$substr": [date, 0, 4]},
                "sum": {"$sum": 1},
            }},
            {"$sort": {"_id": 1}},
        ])



      elif (FctAggregation == "sum"):

            resultat = Operateur.aggregate([
                {"$unwind": NameCollection},
                {"$group": {
                    "_id": {
                        "$substr": [date, 0, 4]},
                    "sum": {"$sum": pathAttribute},
                }},
                {"$sort": {"_id": 1}},
            ])

      elif (FctAggregation == "avg"):

            resultat = Operateur.aggregate([
                {"$unwind": NameCollection},
                {"$group": {
                    "_id": {
                        "$substr": [date, 0, 4]},
                    "avg": {"$avg": pathAttribute},
                }},
                {"$sort": {"_id": 1}},
            ])



      elif (FctAggregation == "count"):
            resultat = Operateur.aggregate([
                {"$unwind": NameCollection},
                {"$group": {
                    "_id": {
                        "$substr": [date, 0, 4]},
                    "count": {"$sum": 1},
                }},
                {"$sort": {"_id": 1}},
            ])

      for i in resultat:
          if (i['_id'].isnumeric() ):
                if (type(i[FctAggregation]) is float):
                    val = round(i[FctAggregation], 2)
                    listVal.update({i["_id"]: val})
                else:
                    listVal.update({i["_id"]: i[FctAggregation]})
      Current_Year = int(datetime.today().strftime('%Y'))
      for an in range(2014, Current_Year + 1):
          if(str(an) in listVal):
              pass
          else:
              listVal.update({str(an): 0})

    return listVal


def CalculAttributEntreprise(NameAttribute, FctAggregation):

   print("CalculAttributEntreprise")
   print("NameAttribute")
   print(NameAttribute)
   NameAttr = NomAttribut(NameAttribute)
   print(NameAttr)

   findpath(base, NameAttr, classes, path, found)
   pathAttribute = PathAttribut()
   print(pathAttribute)

   print(FctAggregation)

   if (NameAttr == "Contrat" or NameAttr == "Resiliation"):
       FctAggregation = "count"

   path.clear()

   Lpath = pathAttribute.split('.')
   print("lpath")
   print(Lpath)
   print(len(Lpath))
   if (len(Lpath) == 3):
       NameCollection = Lpath[1]

   else:
       NameCollection = Lpath[0]

   print("NameCollection")
   print(NameCollection)
   date = ChooseDate(NameAttr, NameCollection)
   print("daaate")
   print(date)

   resultat = {}
   listVal = {}

   if (len(Lpath) == 3):

       if (pathAttribute == date):
           print("count")
           for j in list(Operateur.aggregate([
               {"$unwind": Lpath[0]},
               {"$unwind": Lpath[0] + "." + Lpath[1]},
               {"$match": {"Abonnes.Type_Client": "Entreprise"}},
               {"$group": {
                   "_id": {"date": {"$substr": [date, 0, 4]}},
                   "sum": {"$sum": 1}, }},
               {"$sort": {"_id": 1}},
           ])):
               if (j["_id"]["date"].isnumeric()):
                   if (type(j[FctAggregation]) is float):
                       val = round(j[FctAggregation], 2)
                       listVal.update({j["_id"]["date"]: val})

                   else:
                       listVal.update({j["_id"]["date"]: j[FctAggregation]})

       else:
           if (FctAggregation == "sum"):

               for j in list(Operateur.aggregate([
                   {"$unwind": Lpath[0]},
                   {"$unwind": Lpath[0] + "." + Lpath[1]},
                   {"$match": {"Abonnes.Type_Client": "Entreprise"}},
                   {"$group": {

                       "_id": {"date": {"$substr": [date, 0, 4]}},
                       "sum": {"$sum": {"$sum": pathAttribute}},

                   }},
                   {"$sort": {"_id": 1}},
               ])):
                   if (j["_id"]["date"].isnumeric()):
                       if (type(j[FctAggregation]) is float):
                           val = round(j[FctAggregation], 2)
                           listVal.update({j["_id"]["date"]: val})
                       else:
                           listVal.update({j["_id"]["date"]: j[FctAggregation]})



           elif (FctAggregation == "avg"):

               for j in list(Operateur.aggregate([
                   {"$unwind": Lpath[0]},
                   {"$unwind": Lpath[0] + "." + Lpath[1]},
                   {"$match": {"Abonnes.Type_Client": "Entreprise"}},
                   {"$group": {
                       "_id": {"date": {"$substr": [date, 0, 4]}},
                       "avg": {"$avg": {"$avg": pathAttribute}},
                   }},
                   {"$sort": {"_id": 1}},
               ])):

                   if (j["_id"]["date"].isnumeric()):
                       if (type(j[FctAggregation]) is float):
                           val = round(j[FctAggregation], 2)
                           listVal.update({j["_id"]["date"]: val})
                       else:
                           listVal.update({j["_id"]["date"]: j[FctAggregation]})


           elif (FctAggregation == "count"):
               for j in list(Operateur.aggregate([
                   {"$unwind": Lpath[0]},
                   {"$unwind": Lpath[0] + "." + Lpath[1]},
                   {"$match": {"Abonnes.Type_Client": "Entreprise"}},
                   {"$group": {
                       "_id": {"date": {"$substr": [date, 0, 4]}},
                       "count": {"$sum": 1},
                   }},
                   {"$sort": {"_id": 1}},
               ])):

                   if (j["_id"]["date"].isnumeric()):
                       if (type(j[FctAggregation]) is float):
                           val = round(j[FctAggregation], 2)
                           listVal.update({j["_id"]["date"]: val})
                       else:
                           listVal.update({j["_id"]["date"]: j[FctAggregation]})

           """for i in list(resultat):

                              if (i["_id"]["date"].isnumeric()):
                                  if (type(i[FctAggregation]) is float):
                                       val = round(i[FctAggregation], 2)
                                       listVal.update({i["_id"]["date"]:val})

                                  else:
                                      listVal.update({i["_id"]["date"]:i[FctAggregation]})

                                  print(listVal)"""

   else:
       print("inferieur à < 3")
       if (pathAttribute == date):

           resultat = Operateur.aggregate([
               {"$unwind": NameCollection},
               {"$match": {"Abonnes.Type_Client": "Entreprise"}},
               {"$group": {
                   "_id": {
                       "$substr": [date, 0, 4]},
                   "sum": {"$sum": 1},
               }},
               {"$sort": {"_id": 1}},
           ])



       elif (FctAggregation == "sum"):

           resultat = Operateur.aggregate([
               {"$unwind": NameCollection},
               {"$match": {"Abonnes.Type_Client": "Entreprise"}},
               {"$group": {
                   "_id": {
                       "$substr": [date, 0, 4]},
                   "sum": {"$sum": pathAttribute},
               }},
               {"$sort": {"_id": 1}},
           ])

       elif (FctAggregation == "avg"):

           resultat = Operateur.aggregate([
               {"$unwind": NameCollection},
               {"$match": {"Abonnes.Type_Client": "Entreprise"}},
               {"$group": {
                   "_id": {
                       "$substr": [date, 0, 4]},
                   "avg": {"$avg": pathAttribute},
               }},
               {"$sort": {"_id": 1}},
           ])



       elif (FctAggregation == "count"):
           resultat = Operateur.aggregate([
               {"$unwind": NameCollection},
               {"$match": {"Abonnes.Type_Client": "Entreprise"}},
               {"$group": {
                   "_id": {
                       "$substr": [date, 0, 4]},
                   "count": {"$sum": 1},
               }},
               {"$sort": {"_id": 1}},
           ])

       for i in resultat:
           if (i['_id'].isnumeric()):
               if (type(i[FctAggregation]) is float):
                   val = round(i[FctAggregation], 2)
                   listVal.update({i["_id"]: val})
               else:
                   listVal.update({i["_id"]: i[FctAggregation]})
       Current_Year = int(datetime.today().strftime('%Y'))
       for an in range(2014, Current_Year + 1):
           if (str(an) in listVal):
               pass
           else:
               listVal.update({str(an): 0})

   return listVal



def CalculAttributParticulier(NameAttribute, FctAggregation):

   print("CalculAttributParticulier")
   print("NameAttribute")
   print(NameAttribute)
   NameAttr = NomAttribut(NameAttribute)
   print(NameAttr)

   findpath(base, NameAttr, classes, path, found)
   pathAttribute = PathAttribut()
   print(pathAttribute)

   print(FctAggregation)

   if (NameAttr == "Contrat" or NameAttr == "Resiliation"):
       FctAggregation = "count"

   path.clear()

   Lpath = pathAttribute.split('.')
   print("lpath")
   print(Lpath)
   print(len(Lpath))
   if (len(Lpath) == 3):
       NameCollection = Lpath[1]

   else:
       NameCollection = Lpath[0]

   print("NameCollection")
   print(NameCollection)
   date = ChooseDate(NameAttr, NameCollection)
   print("daaate")
   print(date)

   resultat = {}
   listVal = {}

   if (len(Lpath) == 3):

       if (pathAttribute == date):
           print("count")
           for j in list(Operateur.aggregate([
               {"$unwind": Lpath[0]},
               {"$unwind": Lpath[0] + "." + Lpath[1]},
               {"$match": {"Abonnes.Type_Client": "Particulier"}},
               {"$group": {
                   "_id": {"date": {"$substr": [date, 0, 4]}},
                   "sum": {"$sum": 1}, }},
               {"$sort": {"_id": 1}},
           ])):
               if (j["_id"]["date"].isnumeric()):
                   if (type(j[FctAggregation]) is float):
                       val = round(j[FctAggregation], 2)
                       listVal.update({j["_id"]["date"]: val})

                   else:
                       listVal.update({j["_id"]["date"]: j[FctAggregation]})

       else:
           if (FctAggregation == "sum"):

               for j in list(Operateur.aggregate([
                   {"$unwind": Lpath[0]},
                   {"$unwind": Lpath[0] + "." + Lpath[1]},
                   {"$match": {"Abonnes.Type_Client": "Particulier"}},
                   {"$group": {

                       "_id": {"date": {"$substr": [date, 0, 4]}},
                       "sum": {"$sum": {"$sum": pathAttribute}},

                   }},
                   {"$sort": {"_id": 1}},
               ])):
                   if (j["_id"]["date"].isnumeric()):
                       if (type(j[FctAggregation]) is float):
                           val = round(j[FctAggregation], 2)
                           listVal.update({j["_id"]["date"]: val})
                       else:
                           listVal.update({j["_id"]["date"]: j[FctAggregation]})



           elif (FctAggregation == "avg"):

               for j in list(Operateur.aggregate([
                   {"$unwind": Lpath[0]},
                   {"$unwind": Lpath[0] + "." + Lpath[1]},
                   {"$match": {"Abonnes.Type_Client": "Particulier"}},
                   {"$group": {
                       "_id": {"date": {"$substr": [date, 0, 4]}},
                       "avg": {"$avg": {"$avg": pathAttribute}},
                   }},
                   {"$sort": {"_id": 1}},
               ])):

                   if (j["_id"]["date"].isnumeric()):
                       if (type(j[FctAggregation]) is float):
                           val = round(j[FctAggregation], 2)
                           listVal.update({j["_id"]["date"]: val})
                       else:
                           listVal.update({j["_id"]["date"]: j[FctAggregation]})


           elif (FctAggregation == "count"):
               for j in list(Operateur.aggregate([
                   {"$unwind": Lpath[0]},
                   {"$unwind": Lpath[0] + "." + Lpath[1]},
                   {"$match": {"Abonnes.Type_Client": "Particulier"}},
                   {"$group": {
                       "_id": {"date": {"$substr": [date, 0, 4]}},
                       "count": {"$sum": 1},
                   }},
                   {"$sort": {"_id": 1}},
               ])):

                   if (j["_id"]["date"].isnumeric()):
                       if (type(j[FctAggregation]) is float):
                           val = round(j[FctAggregation], 2)
                           listVal.update({j["_id"]["date"]: val})
                       else:
                           listVal.update({j["_id"]["date"]: j[FctAggregation]})

           """for i in list(resultat):

                              if (i["_id"]["date"].isnumeric()):
                                  if (type(i[FctAggregation]) is float):
                                       val = round(i[FctAggregation], 2)
                                       listVal.update({i["_id"]["date"]:val})

                                  else:
                                      listVal.update({i["_id"]["date"]:i[FctAggregation]})

                                  print(listVal)"""

   else:
       print("inferieur à < 3")
       if (pathAttribute == date):

           resultat = Operateur.aggregate([
               {"$unwind": NameCollection},
               {"$match": {"Abonnes.Type_Client": "Particulier"}},
               {"$group": {
                   "_id": {
                       "$substr": [date, 0, 4]},
                   "sum": {"$sum": 1},
               }},
               {"$sort": {"_id": 1}},
           ])



       elif (FctAggregation == "sum"):

           resultat = Operateur.aggregate([
               {"$unwind": NameCollection},
               {"$match": {"Abonnes.Type_Client": "Particulier"}},
               {"$group": {
                   "_id": {
                       "$substr": [date, 0, 4]},
                   "sum": {"$sum": pathAttribute},
               }},
               {"$sort": {"_id": 1}},
           ])

       elif (FctAggregation == "avg"):

           resultat = Operateur.aggregate([
               {"$unwind": NameCollection},
               {"$match": {"Abonnes.Type_Client": "Particulier"}},
               {"$group": {
                   "_id": {
                       "$substr": [date, 0, 4]},
                   "avg": {"$avg": pathAttribute},
               }},
               {"$sort": {"_id": 1}},
           ])



       elif (FctAggregation == "count"):
           resultat = Operateur.aggregate([
               {"$unwind": NameCollection},
               {"$match": {"Abonnes.Type_Client": "Particulier"}},
               {"$group": {
                   "_id": {
                       "$substr": [date, 0, 4]},
                   "count": {"$sum": 1},
               }},
               {"$sort": {"_id": 1}},
           ])

       for i in resultat:
           if (i['_id'].isnumeric()):
               if (type(i[FctAggregation]) is float):
                   val = round(i[FctAggregation], 2)
                   listVal.update({i["_id"]: val})
               else:
                   listVal.update({i["_id"]: i[FctAggregation]})
       Current_Year = int(datetime.today().strftime('%Y'))
       for an in range(2014, Current_Year + 1):
           if (str(an) in listVal):
               pass
           else:
               listVal.update({str(an): 0})

   return listVal




def CalculFormule(Expression, ListCalulated_Attrbutes):
    Current_Year = int(datetime.today().strftime('%Y'))

    listVal = {}
    for an in range(2014, Current_Year + 1):

        x = Expression
        #print(ListCalulated_Attrbutes)
        #print(ListCalulated_Attrbutes.keys())

        for j in ListCalulated_Attrbutes.keys():
            print(j)

            print(list(ListCalulated_Attrbutes[j][0].values())[0])
            listAnnees=list(list(ListCalulated_Attrbutes[j][0].values())[0].keys())
            print(listAnnees)


            if (str(an) in listAnnees):
                    value = list(ListCalulated_Attrbutes[j][0].values())[0][str(an)]
                    x = x.replace(j, str(value))
            else:
                    listVal.update({str(an): 0})


        val = eval(x)
        if (type(val) is float):
            val = round(val, 2)
        listVal.update({str(an): val})
    return listVal




listAttrbutsExistants=[]

def Insert_New_KPI(request):  #Ajout d un nouveau kpi dans une seule ou plusieurs dimensions
    from datetime import datetime
    ExistInMetadata = request.POST.get("ExistInMetadata", None)
    Name_kpi = request.POST.get("Name_kpi", None)
    Name_kpi = Name_kpi.lower()
    Descr = request.POST.get("Descr", None)
    perf = request.POST.get("perf", None)
    listAttrbutsExistants = request.POST.get("Attributes", None)
    Expression = request.POST.get("Expression", None)
    partie_prenante = request.POST.get("partie_prenante", None)

    ListPerfSelected = perf.split(",")
    print("ListPerfSelected")
    print(ListPerfSelected)
    Expression = Expression.replace(" ", "")
    print("Expression")
    print(Expression)
    ExistInMetadata=int(ExistInMetadata)
    print(ExistInMetadata)
    print("Attributes")
    print(listAttrbutsExistants)


    if(ExistInMetadata==0):#ie ce nvx kpi n existe pas deja dans le metadonnees
        myclient = MongoClient('localhost', 27017)
        CollectionMetadonnees = myclient.myNewDb.get_collection("Metadonnees")
        Metadonnees = list(CollectionMetadonnees.find())[0]
        Metadonnees.pop("_id")


        Metadata = []
        for x in Metadonnees:
            Metadata.append({'Nom_Axe': x, 'Liste_KPI': ','.join(map(str, Metadonnees[x]['Liste_KPI'])).lower(),
                             'Liste_Attributes': ' , '.join(map(str, Metadonnees[x]['Liste_Attributes'])),
                             'Stakeholders': ' , '.join(map(str, Metadonnees[x]['Stakeholders']))})
        Name_kpi = Name_kpi.lower().strip()
        ListePerf = perf.split(',')

        for j in ListePerf:
                for i in Metadata:
                    if (j == i['Nom_Axe']):
                        PerfInd = "Perf.Liste_KPI"
                        PerfInd = PerfInd.replace("Perf", j.strip())
                        CollectionMetadonnees.update_one({}, {"$push": {PerfInd: Name_kpi}})



                        """if (i['Nom_Axe'].strip() == "commercial"):
                            CollectionMetadonnees.update_one({}, {"$push": {"commercial.Liste_KPI": Name_kpi}})


                        if (i['Nom_Axe'].strip() == "social"):
                            CollectionMetadonnees.update_one({}, {"$push": {"social.Liste_KPI": Name_kpi}})

                        if (i['Nom_Axe'].strip() == "competitive"):
                            CollectionMetadonnees.update_one({}, {"$push": {"competitive.Liste_KPI": Name_kpi}})

                        if (i['Nom_Axe'].strip() == "environnemental"):
                            CollectionMetadonnees.update_one({}, {"$push": {"environnemental.Liste_KPI": Name_kpi}})

                        if (i['Nom_Axe'].strip() == "organizational"):
                            CollectionMetadonnees.update_one({}, {"$push": {"organizational.Liste_KPI": Name_kpi}})

                        if (i['Nom_Axe'].strip() == "production"):
                            CollectionMetadonnees.update_one({}, {"$push": {"production.Liste_KPI": Name_kpi}})

                        if (i['Nom_Axe'].strip() == "financial"):
                            CollectionMetadonnees.update_one({}, {"$push": {"financial.Liste_KPI": Name_kpi}})

                        if (i['Nom_Axe'].strip() == "societal"):
                            CollectionMetadonnees.update_one({}, {"$push": {"societal.Liste_KPI": Name_kpi}})

                        if (i['Nom_Axe'].strip() == "strategic"):
                            CollectionMetadonnees.update_one({}, {"$push": {"strategic.Liste_KPI": Name_kpi}})

                        if (i['Nom_Axe'].strip() == "economic"):
                            CollectionMetadonnees.update_one({}, {"$push": {"economic.Liste_KPI": Name_kpi}})"""

    else:#ie kpi existant dans le metadonnees
        pass #on l insere seulement dans le ref


    if request.method == "POST":
         print(request.POST)

         myclient = MongoClient('localhost', 27017)
         CollectionPerformance = myclient.myNewDb.get_collection("Performance")

         Expression = Expression.replace(" ", "")
         expr = re.split(r"\*|\+|\/|-", Expression)
         Current_Year = int(datetime.today().strftime('%Y'))
         print(expr)

         try:
              if(partie_prenante=="subscribers"):
                  print("entrep")
                  #entreprises
                  ListesValeursAttributs = {}
                  for i in expr:
                      print(i)
                      if(i.isnumeric()):
                          print("numeric")
                          pass

                      else:

                          if (i[:3] == "sum"):
                              element = i
                              if (i[3:4] == "("):
                                  i = i.replace("sum", "").replace("(", "").replace(")", "")

                                  print(i)
                                  namelist = element
                                  ListesValeursAttributs[namelist] = []
                                  resultatAttrib = CalculAttributEntreprise(i, "sum")
                                  ListesValeursAttributs[namelist].append({element: resultatAttrib})


                              else:  # sans parentheses

                                  print(i)
                                  i = i.replace("sum", "")
                                  print(i)
                                  namelist = element
                                  ListesValeursAttributs[namelist] = []
                                  resultatAttrib = CalculAttributEntreprise(i, "sum")
                                  ListesValeursAttributs[namelist].append({element: resultatAttrib})


                          elif (i[:3] == "avg"):

                              element = i
                              if (i[3:4] == "("):
                                  i = i.replace("avg", "").replace("(", "").replace(")", "")
                                  namelist = element
                                  ListesValeursAttributs[namelist] = []
                                  resultatAttrib = CalculAttributEntreprise(i, "avg")
                                  ListesValeursAttributs[namelist].append({element: resultatAttrib})

                              else:  # sans parentheses
                                  print(i)
                                  i = i.replace("avg", "")
                                  print(i)
                                  namelist = element
                                  ListesValeursAttributs[namelist] = []
                                  resultatAttrib = CalculAttributEntreprise(i, "avg")
                                  print(resultatAttrib)
                                  ListesValeursAttributs[namelist].append({element: resultatAttrib})


                          elif (i[:5] == "count"):
                              element = i
                              if (i[3:4] == "("):
                                  i = i.replace("count", "").replace("(", "").replace(")", "")
                                  namelist = element
                                  ListesValeursAttributs[namelist] = []
                                  resultatAttrib = CalculAttributEntreprise(i, "count")
                                  ListesValeursAttributs[namelist].append({element: resultatAttrib})


                              else:  # sans parentheses
                                  print(i)
                                  i = i.replace("count", "")
                                  print(i)
                                  namelist = element
                                  ListesValeursAttributs[namelist] = []
                                  resultatAttrib = CalculAttributEntreprise(i, "count")
                                  ListesValeursAttributs[namelist].append({element: resultatAttrib})


                          elif (i in listAttrbutsExistants or i[1:-1] in listAttrbutsExistants):
                              print(i)
                              element = i
                              if (i[3:4] == "("):
                                  i = i.replace("count", "").replace("(", "").replace(")", "")
                                  namelist = element
                                  ListesValeursAttributs[namelist] = []
                                  resultatAttrib = CalculAttributEntreprise(i, "count")

                                  ListesValeursAttributs[namelist].append({element: resultatAttrib})


                              else:  # sans parentheses
                                  print(i)
                                  i = i.replace("count", "")
                                  print(i)
                                  namelist = element
                                  ListesValeursAttributs[namelist] = []
                                  resultatAttrib = CalculAttributEntreprise(i, "count")
                                  ListesValeursAttributs[namelist].append({element: resultatAttrib})



                  ListCalulated_Attrbutes = ListesValeursAttributs
                  listVal = CalculFormule(Expression, ListCalulated_Attrbutes)
                  print("Resultat valeurs entreprises ")
                  for i in listVal.items():
                      print(i)





                  ###############particuliers #########
                  print("part")

                  ListesValeursAttributsParcticulier = {}

                  for i in expr:
                      print(i)
                      if(i.isnumeric()):
                          print("numeric")
                          pass
                      else:

                          if (i[:3] == "sum"):
                              element = i
                              if (i[3:4] == "("):
                                  i = i.replace("sum", "").replace("(", "").replace(")", "")

                                  print(i)
                                  namelist = element
                                  ListesValeursAttributsParcticulier[namelist] = []
                                  resultatAttrib = CalculAttributParticulier(i, "sum")
                                  ListesValeursAttributsParcticulier[namelist].append({element: resultatAttrib})


                              else:  # sans parentheses

                                  print(i)
                                  i = i.replace("sum", "")
                                  print(i)
                                  namelist = element
                                  ListesValeursAttributsParcticulier[namelist] = []
                                  resultatAttrib = CalculAttributParticulier(i, "sum")
                                  ListesValeursAttributsParcticulier[namelist].append({element: resultatAttrib})


                          elif (i[:3] == "avg"):

                              element = i
                              if (i[3:4] == "("):
                                  i = i.replace("avg", "").replace("(", "").replace(")", "")
                                  namelist = element
                                  ListesValeursAttributsParcticulier[namelist] = []
                                  resultatAttrib = CalculAttributParticulier(i, "avg")
                                  ListesValeursAttributsParcticulier[namelist].append({element: resultatAttrib})

                              else:  # sans parentheses
                                  print(i)
                                  i = i.replace("avg", "")
                                  print(i)
                                  namelist = element
                                  ListesValeursAttributsParcticulier[namelist] = []
                                  resultatAttrib = CalculAttributParticulier(i, "avg")
                                  print(resultatAttrib)
                                  ListesValeursAttributsParcticulier[namelist].append({element: resultatAttrib})


                          elif (i[:5] == "count"):
                              element = i
                              if (i[3:4] == "("):
                                  i = i.replace("count", "").replace("(", "").replace(")", "")
                                  namelist = element
                                  ListesValeursAttributsParcticulier[namelist] = []
                                  resultatAttrib = CalculAttributParticulier(i, "count")
                                  ListesValeursAttributsParcticulier[namelist].append({element: resultatAttrib})


                              else:  # sans parentheses
                                  print(i)
                                  i = i.replace("count", "")
                                  print(i)
                                  namelist = element
                                  ListesValeursAttributsParcticulier[namelist] = []
                                  resultatAttrib = CalculAttributParticulier(i, "count")
                                  ListesValeursAttributsParcticulier[namelist].append({element: resultatAttrib})


                          elif (i in listAttrbutsExistants or i[1:-1] in listAttrbutsExistants):
                              print(i)
                              element = i
                              if (i[3:4] == "("):
                                  i = i.replace("count", "").replace("(", "").replace(")", "")
                                  namelist = element
                                  ListesValeursAttributsParcticulier[namelist] = []
                                  resultatAttrib = CalculAttributParticulier(i, "count")

                                  ListesValeursAttributsParcticulier[namelist].append({element: resultatAttrib})


                              else:  # sans parentheses
                                  print(i)
                                  i = i.replace("count", "")
                                  print(i)
                                  namelist = element
                                  ListesValeursAttributsParcticulier[namelist] = []
                                  resultatAttrib = CalculAttributParticulier(i, "count")
                                  ListesValeursAttributsParcticulier[namelist].append({element: resultatAttrib})



                  ListCalulated_AttrbutesParcticulier = ListesValeursAttributsParcticulier
                  listValParticulier = CalculFormule(Expression, ListCalulated_AttrbutesParcticulier)
                  print("Resultat valeurs particuliers")
                  for i in listValParticulier.items():
                      print(i)



                  newKpi = {"Nom_KPI": Name_kpi, "Desc_KPI": Descr,"Fct_KPI":Expression,"Valeurs_KPI": listValParticulier ,"Valeurs_KPI_Entr": listVal, "Seuil_KPI":{} , "Seuil_KPI_Entr": {}, "Type":1}


                  for perf in ListPerfSelected:
                          print(perf)
                          if (perf == "commercial"):
                              CollectionPerformance.update({}, {"$push": {"PerfCom.ListeKPI": newKpi}})
                          elif (perf == "social"):
                              CollectionPerformance.update({}, {"$push": {"PerfSoc.ListeKPI": newKpi}})
                          elif (perf == "competitive"):
                              CollectionPerformance.update({}, {"$push": {"PerfConc.ListeKPI": newKpi}})
                          elif (perf=="environnemental"):
                              CollectionPerformance.update({}, {"$push": {"PerfEnv.ListeKPI": newKpi}})
                          else:
                              PerfInd = "Perf.ListeKPI"
                              PerfInd = PerfInd.replace("Perf", perf.strip())
                              CollectionPerformance.update({}, {"$push": {PerfInd: newKpi}})




              elif (partie_prenante == "Employees" or  partie_prenante == "others" ):

                  print("Employees")

                  ListesValeursAttributs = {}

                  # Expression = "sum ( Resignation ) +sum Absence +avg (Absence) + count( Resignation) +8 * 1 1 -25/9"

                  #Expression="sum (Incomes) +sum Salary + count  Resignation + sum Absence + avg Salary / 55" +sum ( Resignation )+ sum ( unsubscription ) +
                 # Expression="  sum ( unsubscription ) + sum ( Date_Absence ) ++avg Antenne_Frequency+ sum ( Resignation )- avg Salary / 55 + sum Employee_satisfaction_rating + sum  Subscribers_satisfaction_rating + avg Antenne_Frequency" #avg Absence



                  print(expr)
                  for i in expr:
                      print(i)
                      if(i.isnumeric()):
                          print("numeric")
                          pass
                      else:

                          if (i[:3] == "sum"):
                              element = i
                              if (i[3:4] == "("):
                                  i = i.replace("sum", "").replace("(", "").replace(")", "")

                                  print(i)
                                  namelist = element
                                  ListesValeursAttributs[namelist] = []
                                  resultatAttrib = CalculAttribut(i, "sum")
                                  ListesValeursAttributs[namelist].append({element: resultatAttrib})


                              else:  # sans parentheses

                                  print(i)
                                  i = i.replace("sum", "")
                                  print(i)
                                  namelist = element
                                  ListesValeursAttributs[namelist] = []
                                  resultatAttrib = CalculAttribut(i, "sum")
                                  ListesValeursAttributs[namelist].append({element: resultatAttrib})


                          elif (i[:3] == "avg"):

                              element = i
                              if (i[3:4] == "("):
                                  i = i.replace("avg", "").replace("(", "").replace(")", "")
                                  namelist = element
                                  ListesValeursAttributs[namelist] = []
                                  resultatAttrib = CalculAttribut(i, "avg")
                                  ListesValeursAttributs[namelist].append({element: resultatAttrib})

                              else:  # sans parentheses
                                  print(i)
                                  i = i.replace("avg", "")
                                  print(i)
                                  namelist = element
                                  ListesValeursAttributs[namelist] = []
                                  resultatAttrib = CalculAttribut(i, "avg")
                                  print(resultatAttrib)
                                  ListesValeursAttributs[namelist].append({element: resultatAttrib})


                          elif (i[:5] == "count"):
                              element = i
                              if (i[3:4] == "("):
                                  i = i.replace("count", "").replace("(", "").replace(")", "")
                                  namelist = element
                                  ListesValeursAttributs[namelist] = []
                                  resultatAttrib = CalculAttribut(i, "count")
                                  ListesValeursAttributs[namelist].append({element: resultatAttrib})


                              else:  # sans parentheses
                                  print(i)
                                  i = i.replace("count", "")
                                  print(i)
                                  namelist = element
                                  ListesValeursAttributs[namelist] = []
                                  resultatAttrib = CalculAttribut(i, "count")
                                  ListesValeursAttributs[namelist].append({element: resultatAttrib})


                          elif (i in listAttrbutsExistants or i[1:-1] in listAttrbutsExistants):
                              print(i)
                              element = i
                              if (i[3:4] == "("):
                                  i = i.replace("count", "").replace("(", "").replace(")", "")
                                  namelist = element
                                  ListesValeursAttributs[namelist] = []
                                  resultatAttrib = CalculAttribut(i, "count")

                                  ListesValeursAttributs[namelist].append({element: resultatAttrib})


                              else:  # sans parentheses
                                  print(i)
                                  i = i.replace("count", "")
                                  print(i)
                                  namelist = element
                                  ListesValeursAttributs[namelist] = []
                                  resultatAttrib = CalculAttribut(i, "count")
                                  ListesValeursAttributs[namelist].append({element: resultatAttrib})



                  ListCalulated_Attrbutes = ListesValeursAttributs
                  listVal = CalculFormule(Expression, ListCalulated_Attrbutes)
                  print("Resultat valeurs")
                  for i in listVal.items():
                      print(i)

                  if(partie_prenante == "Employees" ):
                      typ=2
                  else:
                      typ=3

                  newKpi = {"Nom_KPI": Name_kpi, "Desc_KPI": Descr,"Fct_KPI":Expression,"Valeurs_KPI": listVal , "Seuil_KPI": {} , "Type":typ}


                  for perf in ListPerfSelected:
                          print(perf)
                          if (perf == "commercial"):
                              CollectionPerformance.update({}, {"$push": {"PerfCom.ListeKPI": newKpi}})
                          elif (perf == "social"):
                              CollectionPerformance.update({}, {"$push": {"PerfSoc.ListeKPI": newKpi}})
                          elif (perf == "competitive"):
                              CollectionPerformance.update({}, {"$push": {"PerfConc.ListeKPI": newKpi}})
                          elif (perf == "environnemental"):
                              CollectionPerformance.update({}, {"$push": {"PerfEnv.ListeKPI": newKpi}})
                          else:
                              PerfInd = "Perf.ListeKPI"
                              PerfInd = PerfInd.replace("Perf", perf.strip())
                              CollectionPerformance.update({}, {"$push": {PerfInd: newKpi}})



         except Exception as e:
            print("Exception :", str(e))

    return render(request, "home/TableReferentiel.html")


def Delete_KPI(request):

    org_nameKpi = request.POST.get("org_nameKpi", None)
    org_perf = request.POST.get("org_perf", None)

    if request.method == "POST":
        print(request.POST)
        org_nameKpi = org_nameKpi.strip()
        org_perf = org_perf.strip()

        myclient = MongoClient('localhost', 27017)
        CollectionPerformance = myclient.myNewDb.get_collection("Performance")




        if(org_perf=="commercial"):
         CollectionPerformance.update_one({}, {"$pull": {"PerfCom.ListeKPI": {"Nom_KPI": org_nameKpi }}})
        elif(org_perf=="social"):
         CollectionPerformance.update_one({}, {"$pull": {"PerfSoc.ListeKPI": {"Nom_KPI": org_nameKpi }}})
        elif(org_perf=="competitive"):
         CollectionPerformance.update_one({}, {"$pull": {"PerfConc.ListeKPI": {"Nom_KPI": org_nameKpi }}})
        elif(org_perf=="financial"):
         CollectionPerformance.update_one({}, {"$pull": {"financial.ListeKPI": {"Nom_KPI": org_nameKpi }}})
        elif(org_perf=="economic"):
         CollectionPerformance.update_one({}, {"$pull": {"economic.ListeKPI": {"Nom_KPI": org_nameKpi }}})
        elif(org_perf=="organizational"):
         CollectionPerformance.update_one({}, {"$pull": {"organizational.ListeKPI": {"Nom_KPI": org_nameKpi }}})
        elif(org_perf=="strategic"):
         CollectionPerformance.update_one({}, {"$pull": {"strategic.ListeKPI": {"Nom_KPI": org_nameKpi }}})
        elif(org_perf=="production"):
         CollectionPerformance.update_one({}, {"$pull": {"production.ListeKPI": {"Nom_KPI": org_nameKpi }}})
        elif(org_perf=="societal"):
         CollectionPerformance.update_one({}, {"$pull": {"societal.ListeKPI": {"Nom_KPI": org_nameKpi }}})
        else: #org_perf=="environnemental"
         CollectionPerformance.update_one({}, {"$pull": {"PerfEnv.ListeKPI": {"Nom_KPI": org_nameKpi }}})


    return render(request, "home/TableReferentiel.html")







              ################################      Metadonnées       #########################

def Update_Keyword_KPI(request):
    CollectionMetadonnees = myclient.myNewDb.get_collection("Metadonnees")
    Metadonnees = list(CollectionMetadonnees.find())[0]

    Metadonnees.pop("_id")
    Metadata = []
    for x in Metadonnees:
        Metadata.append({'Nom_Axe': x, 'Liste_KPI': ','.join(map(str, Metadonnees[x]['Liste_KPI'])).lower(),
                         'Liste_Attributes': ' , '.join(map(str, Metadonnees[x]['Liste_Attributes'])),
                         'Stakeholders': ' , '.join(map(str, Metadonnees[x]['Stakeholders']))})


    NomPerf = request.POST.get("NomPerf", None)   #l'axe  initial de keyword
    ListperfKeyword = request.POST.get("ListperfKeyword", None) #les perf ou le keyword existe
    selectedPerf = request.POST.get("selectedPerf", None)  #les perf que le concepteur a selectionner lors de *update
    OldKeyword = request.POST.get("OldKeyword", None)
    NewKeyword = request.POST.get("NewKeyword", None)
    OldKeyword = OldKeyword.strip()
    NewKeyword = NewKeyword.strip()

    """for i in Metadata:
        print(i['Nom_Axe'])
        Liste = i['Liste_KPI'].split(',')
        print(Liste)"""

    ListePerf = selectedPerf.split(',')

    PerfToUpdate=[]
    PerfToDelete=[]
    PerfToAdd=[]
    L2=ListperfKeyword.split(',')
    for k in L2:
        print(k)
        if(k in ListePerf): #update seulement
            PerfToUpdate.append(k)
        else: #delete
            PerfToDelete.append(k)

    for m in ListePerf:
        if((m in PerfToUpdate) or(m in PerfToDelete) ): #add
            pass
        else:
            PerfToAdd.append(m)

    print(L2)
    print(ListePerf)
    print(PerfToUpdate)
    print(PerfToDelete)
    print(PerfToAdd)


    ### les perf à mettre à jour
    for j in PerfToUpdate:
      for i in Metadata:
        if (j==i['Nom_Axe']):
               Liste = i["Liste_KPI"].split(',')
               print("Liste")
               print(Liste)
               index=Liste.index(OldKeyword.lower().strip())
               Liste[index]=NewKeyword

               PerfInd = "Perf.Liste_KPI"
               PerfInd = PerfInd.replace("Perf", j.strip())
               CollectionMetadonnees.update_one({},
                                                {"$set":
                                                     {PerfInd: Liste}
                                                 })




               """if(i['Nom_Axe'].strip()=="commercial"):
                   CollectionMetadonnees.update_one({},
                                                    {"$set":
                                                         {'commercial.Liste_KPI': Liste}
                                                     })

               if(i['Nom_Axe'].strip()=="social"):
                   CollectionMetadonnees.update_one({},
                                                    {"$set":
                                                         {'social.Liste_KPI': Liste}
                                                     })
               if(i['Nom_Axe'].strip()=="competitive"):
                   CollectionMetadonnees.update_one({},
                                                    {"$set":
                                                         {'competitive.Liste_KPI': Liste}
                                                     })
               if(i['Nom_Axe'].strip()=="environnemental"):
                   CollectionMetadonnees.update_one({},
                                                    {"$set":
                                                         {'environnemental.Liste_KPI': Liste}
                                                     })
               if(i['Nom_Axe'].strip()=="organizational"):
                   CollectionMetadonnees.update_one({},
                                                    {"$set":
                                                         {'organizational.Liste_KPI': Liste}
                                                     })
               if(i['Nom_Axe'].strip()=="production"):
                   CollectionMetadonnees.update_one({},
                                                    {"$set":
                                                         {'production.Liste_KPI': Liste}
                                                     })
               if(i['Nom_Axe'].strip()=="financial"):
                   CollectionMetadonnees.update_one({},
                                                    {"$set":
                                                         {'financial.Liste_KPI': Liste}
                                                     })
               if(i['Nom_Axe'].strip()=="societal"):
                   CollectionMetadonnees.update_one({},
                                                    {"$set":
                                                         {'societal.Liste_KPI': Liste}
                                                     })
               if(i['Nom_Axe'].strip()=="strategic"):
                   CollectionMetadonnees.update_one({},
                                                    {"$set":
                                                         {'strategic.Liste_KPI': Liste}
                                                     })
               if(i['Nom_Axe'].strip()=="economic"):
                   CollectionMetadonnees.update_one({},
                                                    {"$set":
                                                         {'economic.Liste_KPI': Liste}
                                                     })"""




    for j in PerfToDelete:  ### retirer le keyword de la liste de kpi de ces perf
      for i in Metadata:
        if (j==i['Nom_Axe']):
                PerfInd = "Perf.Liste_KPI"
                PerfInd = PerfInd.replace("Perf", j.strip())
                CollectionMetadonnees.update_one({}, {"$pull": {PerfInd: OldKeyword}})


        """ if (i['Nom_Axe'].strip() == "commercial"):
                    CollectionMetadonnees.update_one({}, {"$pull": {"commercial.Liste_KPI": OldKeyword}})

                if (i['Nom_Axe'].strip() == "social"):
                    CollectionMetadonnees.update_one({}, {"$pull": {"social.Liste_KPI": OldKeyword}})

                if (i['Nom_Axe'].strip() == "competitive"):
                    CollectionMetadonnees.update_one({}, {"$pull": {"competitive.Liste_KPI": OldKeyword}})

                if (i['Nom_Axe'].strip() == "environnemental"):
                    CollectionMetadonnees.update_one({}, {"$pull": {"environnemental.Liste_KPI": OldKeyword}})

                if (i['Nom_Axe'].strip() == "organizational"):
                    CollectionMetadonnees.update_one({}, {"$pull": {"organizational.Liste_KPI": OldKeyword}})

                if (i['Nom_Axe'].strip() == "production"):
                    CollectionMetadonnees.update_one({}, {"$pull": {"production.Liste_KPI": OldKeyword}})

                if (i['Nom_Axe'].strip() == "financial"):
                    CollectionMetadonnees.update_one({}, {"$pull": {"financial.Liste_KPI": OldKeyword}})

                if (i['Nom_Axe'].strip() == "societal"):
                    CollectionMetadonnees.update_one({}, {"$pull": {"societal.Liste_KPI": OldKeyword}})

                if (i['Nom_Axe'].strip() == "strategic"):
                    CollectionMetadonnees.update_one({}, {"$pull": {"strategic.Liste_KPI": OldKeyword}})

                if (i['Nom_Axe'].strip() == "economic"):
                    CollectionMetadonnees.update_one({}, {"$pull": {"economic.Liste_KPI": OldKeyword}})"""


    ### ajouter le keyword à la liste de kpi de ces  perf
    #verifier d abord qu ils n existent pas deja dans la BDD

    for j in PerfToAdd:
      for i in Metadata:
            if (j==i['Nom_Axe']):

                PerfInd = "Perf.Liste_KPI"
                PerfInd = PerfInd.replace("Perf", j.strip())

                exist = CollectionMetadonnees.find_one({PerfInd: NewKeyword.lower()})
                if (exist is not None):
                    print("exists")
                else:
                    CollectionMetadonnees.update_one({}, {"$push": {PerfInd: NewKeyword.lower()}})



                """if (i['Nom_Axe'].strip() == "commercial"):
                    exist = CollectionMetadonnees.find_one({'commercial.Liste_KPI': NewKeyword.lower()})
                    if (exist is not None):
                        print("exists")
                    else:
                        CollectionMetadonnees.update_one({}, {"$push": {"commercial.Liste_KPI": NewKeyword.lower()}})




                if (i['Nom_Axe'].strip() == "social"):

                    exist = CollectionMetadonnees.find_one({'social.Liste_KPI': NewKeyword})
                    if (exist is not None):
                        print("exists")
                    else:
                        CollectionMetadonnees.update_one({}, {"$push": {"social.Liste_KPI": NewKeyword}})




                if (i['Nom_Axe'].strip() == "competitive"):
                    exist = CollectionMetadonnees.find_one({'competitive.Liste_KPI': NewKeyword})
                    if (exist is not None):
                        print("exists")
                    else:
                       CollectionMetadonnees.update_one({}, {"$push": {"competitive.Liste_KPI": NewKeyword}})





                if (i['Nom_Axe'].strip() == "environnemental"):
                    exist = CollectionMetadonnees.find_one({'environnemental.Liste_KPI': NewKeyword})
                    if (exist is not None):
                        print("exists")
                    else:
                        CollectionMetadonnees.update_one({}, {"$push": {"environnemental.Liste_KPI": NewKeyword}})





                if (i['Nom_Axe'].strip() == "organizational"):
                    exist = CollectionMetadonnees.find_one({'commercial.Liste_KPI': NewKeyword})
                    if (exist is not None):
                        print("exists")
                    else:
                        CollectionMetadonnees.update_one({}, {"$push": {"organizational.Liste_KPI": NewKeyword}})




                if (i['Nom_Axe'].strip() == "production"):
                    exist = CollectionMetadonnees.find_one({'production.Liste_KPI': NewKeyword})
                    if (exist is not None):
                        print("exists")
                    else:
                        CollectionMetadonnees.update_one({}, {"$push": {"production.Liste_KPI": NewKeyword}})




                if (i['Nom_Axe'].strip() == "financial"):
                    exist = CollectionMetadonnees.find_one({'financial.Liste_KPI': NewKeyword})
                    if (exist is not None):
                        print("exists")
                    else:
                        CollectionMetadonnees.update_one({}, {"$push": {"financial.Liste_KPI": NewKeyword}})




                if (i['Nom_Axe'].strip() == "societal"):
                    exist = CollectionMetadonnees.find_one({'societal.Liste_KPI': NewKeyword})
                    if (exist is not None):
                        print("exists")
                    else:
                        CollectionMetadonnees.update_one({}, {"$push": {"societal.Liste_KPI": NewKeyword}})





                if (i['Nom_Axe'].strip() == "strategic"):
                    exist = CollectionMetadonnees.find_one({'strategic.Liste_KPI': NewKeyword})
                    if (exist is not None):
                        print("exists")
                    else:
                        CollectionMetadonnees.update_one({}, {"$push": {"strategic.Liste_KPI": NewKeyword}})





                if (i['Nom_Axe'].strip() == "economic"):
                    exist = CollectionMetadonnees.find_one({'economic.Liste_KPI': NewKeyword})
                    if (exist is not None):
                        print("exists")
                    else:
                        CollectionMetadonnees.update_one({}, {"$push": {"economic.Liste_KPI": NewKeyword}})"""






    return render(request, "home/Configuration.html")



def Add_Keyword_KPI(request):
    CollectionMetadonnees = myclient.myNewDb.get_collection("Metadonnees")
    Metadonnees = list(CollectionMetadonnees.find())[0]

    Metadonnees.pop("_id")
    Metadata = []
    for x in Metadonnees:
        Metadata.append({'Nom_Axe': x, 'Liste_KPI': ','.join(map(str, Metadonnees[x]['Liste_KPI'])).lower(),
                         'Liste_Attributes': ' , '.join(map(str, Metadonnees[x]['Liste_Attributes'])),
                         'Stakeholders': ' , '.join(map(str, Metadonnees[x]['Stakeholders']))})

    Name_kpi = request.POST.get("Name_kpi", None)
    perf = request.POST.get("perf", None)
    Name_kpi = Name_kpi.strip().lower()
    ListNomAxes=[]
    for m in Metadata:
        ListNomAxes.append(m['Nom_Axe'])


    ListePerf = perf.split(',')

    for j in ListePerf:
      for i in ListNomAxes:
            if (j==i.strip()):
                    new = "Perf.Liste_KPI"
                    new=new.replace("Perf",i.strip())
                    CollectionMetadonnees.update_one({}, {"$push": {new: Name_kpi}})


            """if (i['Nom_Axe'].strip() == "social"):
                    CollectionMetadonnees.update_one({}, {"$push": {"social.Liste_KPI": Name_kpi}})

                if (i['Nom_Axe'].strip() == "competitive"):
                    CollectionMetadonnees.update_one({}, {"$push": {"competitive.Liste_KPI": Name_kpi}})

                if (i['Nom_Axe'].strip() == "environnemental"):
                    CollectionMetadonnees.update_one({}, {"$push": {"environnemental.Liste_KPI": Name_kpi}})

                if (i['Nom_Axe'].strip() == "organizational"):
                    CollectionMetadonnees.update_one({}, {"$push": {"organizational.Liste_KPI": Name_kpi}})

                if (i['Nom_Axe'].strip() == "production"):
                    CollectionMetadonnees.update_one({}, {"$push": {"production.Liste_KPI": Name_kpi}})

                if (i['Nom_Axe'].strip() == "financial"):
                    CollectionMetadonnees.update_one({}, {"$push": {"financial.Liste_KPI": Name_kpi}})

                if (i['Nom_Axe'].strip() == "societal"):
                    CollectionMetadonnees.update_one({}, {"$push": {"societal.Liste_KPI": Name_kpi}})

                if (i['Nom_Axe'].strip() == "strategic"):
                    CollectionMetadonnees.update_one({}, {"$push": {"strategic.Liste_KPI": Name_kpi}})

                if (i['Nom_Axe'].strip() == "economic"):
                    CollectionMetadonnees.update_one({}, {"$push": {"economic.Liste_KPI": Name_kpi}})"""

    return render(request, "home/Configuration.html")


def Remove_Keyword_KPI(request):

    CollectionMetadonnees = myclient.myNewDb.get_collection("Metadonnees")
    Metadonnees = list(CollectionMetadonnees.find())[0]

    Metadonnees.pop("_id")
    Metadata = []
    for x in Metadonnees:
        Metadata.append({'Nom_Axe': x, 'Liste_KPI': ','.join(map(str, Metadonnees[x]['Liste_KPI'])).lower(),
                         'Liste_Attributes': ' , '.join(map(str, Metadonnees[x]['Liste_Attributes'])),
                         'Stakeholders': ' , '.join(map(str, Metadonnees[x]['Stakeholders']))})

    NomPerf = request.POST.get("NomPerf", None)
    OldKeyword = request.POST.get("OldKeyword", None)
    OldKeyword = OldKeyword.strip()


    for i in Metadata:
        if (NomPerf.strip() == i['Nom_Axe']):
            print("i['Nom_Axe']")
            print(i['Nom_Axe'])
            PerfInd = "Perf.Liste_KPI"
            PerfInd = PerfInd.replace("Perf",NomPerf.strip())
            CollectionMetadonnees.update_one({}, {"$pull": {PerfInd: OldKeyword}})
            print("dooone")

            """if (i['Nom_Axe'].strip() == "commercial"):
                CollectionMetadonnees.update_one({}, {"$pull": {"commercial.Liste_KPI": OldKeyword}})

            if (i['Nom_Axe'].strip() == "social"):
                CollectionMetadonnees.update_one({}, {"$pull": {"social.Liste_KPI": OldKeyword}})

            if (i['Nom_Axe'].strip() == "competitive"):
                CollectionMetadonnees.update_one({}, {"$pull": {"competitive.Liste_KPI": OldKeyword}})

            if (i['Nom_Axe'].strip() == "environnemental"):
                CollectionMetadonnees.update_one({}, {"$pull": {"environnemental.Liste_KPI": OldKeyword}})

            if (i['Nom_Axe'].strip() == "organizational"):
                CollectionMetadonnees.update_one({}, {"$pull": {"organizational.Liste_KPI": OldKeyword}})

            if (i['Nom_Axe'].strip() == "production"):
                CollectionMetadonnees.update_one({}, {"$pull": {"production.Liste_KPI": OldKeyword}})

            if (i['Nom_Axe'].strip() == "financial"):
                CollectionMetadonnees.update_one({}, {"$pull": {"financial.Liste_KPI": OldKeyword}})

            if (i['Nom_Axe'].strip() == "societal"):
                CollectionMetadonnees.update_one({}, {"$pull": {"societal.Liste_KPI": OldKeyword}})

            if (i['Nom_Axe'].strip() == "strategic"):
                CollectionMetadonnees.update_one({}, {"$pull": {"strategic.Liste_KPI": OldKeyword}})

            if (i['Nom_Axe'].strip() == "economic"):
                CollectionMetadonnees.update_one({}, {"$pull": {"economic.Liste_KPI": OldKeyword}})"""

    return render(request, "home/Configuration.html")




####### supprimer un attribut ########

def Remove_Keyword_Attribute(request):
    perf = request.POST.get("NomPerf", None)
    OldKeyword = request.POST.get("OldKeyword", None)


    CollectionMetadonnees = myclient.myNewDb.get_collection("Metadonnees")
    Metadonnees = list(CollectionMetadonnees.find())[0]

    Metadonnees.pop("_id")
    Metadata = []
    for x in Metadonnees:
        Metadata.append({'Nom_Axe': x, 'Liste_KPI': ','.join(map(str, Metadonnees[x]['Liste_KPI'])).lower(),
                         'Liste_Attributes': ' , '.join(map(str, Metadonnees[x]['Liste_Attributes'])),
                         'Stakeholders': ' , '.join(map(str, Metadonnees[x]['Stakeholders']))})

    OldKeyword = OldKeyword.strip()


    for i in Metadata:
        if (perf == i['Nom_Axe']):
            if (i['Nom_Axe'].strip() == "commercial"):
                CollectionMetadonnees.update_one({}, {"$pull": {"commercial.Liste_Attributes": OldKeyword}})

            if (i['Nom_Axe'].strip() == "social"):
                CollectionMetadonnees.update_one({}, {"$pull": {"social.Liste_Attributes": OldKeyword}})

            if (i['Nom_Axe'].strip() == "competitive"):
                CollectionMetadonnees.update_one({}, {"$pull": {"competitive.Liste_Attributes": OldKeyword}})

            if (i['Nom_Axe'].strip() == "environnemental"):
                CollectionMetadonnees.update_one({}, {"$pull": {"environnemental.Liste_Attributes": OldKeyword}})

            if (i['Nom_Axe'].strip() == "organizational"):
                CollectionMetadonnees.update_one({}, {"$pull": {"organizational.Liste_Attributes": OldKeyword}})

            if (i['Nom_Axe'].strip() == "production"):
                CollectionMetadonnees.update_one({}, {"$pull": {"production.Liste_Attributes": OldKeyword}})

            if (i['Nom_Axe'].strip() == "financial"):
                CollectionMetadonnees.update_one({}, {"$pull": {"financial.Liste_Attributes": OldKeyword}})

            if (i['Nom_Axe'].strip() == "societal"):
                CollectionMetadonnees.update_one({}, {"$pull": {"societal.Liste_Attributes": OldKeyword}})

            if (i['Nom_Axe'].strip() == "strategic"):
                CollectionMetadonnees.update_one({}, {"$pull": {"strategic.Liste_Attributes": OldKeyword}})

            if (i['Nom_Axe'].strip() == "economic"):
                CollectionMetadonnees.update_one({}, {"$pull": {"economic.Liste_Attributes": OldKeyword}})

    return render(request, "home/Configuration.html")

                          ##################################################################################

#sauvegarder les changements apportés sur les parties prennantes dans le métadonnées
def Save_Stakeholders_Keyword_KPI(request):
    perf = request.POST.get("perf", None)  #la perf initiale
    Stakeholders = request.POST.get("Stakeholders", None)  #liste de stakeholders


    CollectionMetadonnees = myclient.myNewDb.get_collection("Metadonnees")
    Metadonnees = list(CollectionMetadonnees.find())[0]

    Metadonnees.pop("_id")
    Metadata = []
    for x in Metadonnees:
        Metadata.append({'Nom_Axe': x, 'Liste_KPI': ','.join(map(str, Metadonnees[x]['Liste_KPI'])).lower(),
                         'Liste_Attributes': ' , '.join(map(str, Metadonnees[x]['Liste_Attributes'])),
                         'Stakeholders': ' , '.join(map(str, Metadonnees[x]['Stakeholders']))})




    Liste = Stakeholders.split(',')

    ### les perf à mettre à jour


    for i in Metadata:
            if (perf== i['Nom_Axe']):

                if (i['Nom_Axe'].strip() == "commercial"):
                    CollectionMetadonnees.update_one({},
                                                     {"$set":
                                                          {'commercial.Stakeholders': Liste}
                                                      })

                if (i['Nom_Axe'].strip() == "social"):
                    CollectionMetadonnees.update_one({},
                                                     {"$set":
                                                          {'social.Stakeholders': Liste}
                                                      })
                if (i['Nom_Axe'].strip() == "competitive"):
                    CollectionMetadonnees.update_one({},
                                                     {"$set":
                                                          {'competitive.Stakeholders': Liste}
                                                      })
                if (i['Nom_Axe'].strip() == "environnemental"):
                    CollectionMetadonnees.update_one({},
                                                     {"$set":
                                                          {'environnemental.Stakeholders': Liste}
                                                      })
                if (i['Nom_Axe'].strip() == "organizational"):
                    CollectionMetadonnees.update_one({},
                                                     {"$set":
                                                          {'organizational.Stakeholders': Liste}
                                                      })
                if (i['Nom_Axe'].strip() == "production"):
                    CollectionMetadonnees.update_one({},
                                                     {"$set":
                                                          {'production.Stakeholders': Liste}
                                                      })
                if (i['Nom_Axe'].strip() == "financial"):
                    CollectionMetadonnees.update_one({},
                                                     {"$set":
                                                          {'financial.Stakeholders': Liste}
                                                      })
                if (i['Nom_Axe'].strip() == "societal"):
                    CollectionMetadonnees.update_one({},
                                                     {"$set":
                                                          {'societal.Stakeholders': Liste}
                                                      })
                if (i['Nom_Axe'].strip() == "strategic"):
                    CollectionMetadonnees.update_one({},
                                                     {"$set":
                                                          {'strategic.Stakeholders': Liste}
                                                      })
                if (i['Nom_Axe'].strip() == "economic"):
                    CollectionMetadonnees.update_one({},
                                                     {"$set":
                                                          {'economic.Stakeholders': Liste}
                                                      })


    return render(request, "home/Configuration.html")




                        ##################################################################################

def Update_KPI(request):
 

    #old values
    org_perf = request.POST.get("org_perf", None)
    org_nameKpi = request.POST.get("org_nameIndic", None)
    ListAxes = request.POST.get("ListAxes", None)
    #org_fct = request.POST.get("org_fct", None)


    #new values
    perf = request.POST.get("selected", None)
    nameKpi = request.POST.get("Name_kpi", None)
    descr = request.POST.get("Descr", None)
    #new_fct = request.POST.get("newFct", None)
    #stackholders = request.POST.get("stackholders", None)



    if request.method == "POST":
        print(request.POST)

        org_perf=org_perf.strip()
        print("org_perf")
        print(org_perf)

        org_nameKpi = org_nameKpi.strip()
        print(org_nameKpi)


        print("perf")

        print(type(perf))
        print(perf)
        perf=perf.split(",")

        ListAxes = ListAxes.split(",")

        nameKpi=nameKpi.strip()
        print(nameKpi)

        descr=descr.strip()
        print(descr)
        myclient = MongoClient('localhost', 27017)
        CollectionPerformance = myclient.myNewDb.get_collection("Performance")

        """ print("fct")
        new_fct=new_fct.strip()
        print(new_fct)


        org_fct=org_fct.strip()
        print(org_fct)"""
        # perf #nvx
        # ListAxes#old
        PerfToUpdate = []
        PerfToDelete = []
        PerfToAdd = []

        for k in ListAxes:
            print(k)
            if (k in perf):  # update seulement
                PerfToUpdate.append(k)
            else:  # delete
                PerfToDelete.append(k)

        for m in perf:
            if ((m in PerfToUpdate) or (m in PerfToDelete)):  # add
                pass
            else:
                PerfToAdd.append(m)

        print("LiiiiiiiistAxes")
        print(ListAxes)
        print("perf")#list perf
        print(perf)
        print("PerfToUpdate")
        print(PerfToUpdate)
        print("PerfToDelete")
        print(PerfToDelete)
        print("PerfToAdd")
        print(PerfToAdd)



        #CollectionPerformance=myclient.myNewDb.get_collection("Performance")
        Collectionkpi = myclient.myNewDb.get_collection("Performance")
        kpi = list(Collectionkpi.find())

        listPerf = []
        for x in kpi:
            for y in x:
                listPerf.append(y)

        listPerf.pop(0)

        listPerf.pop(-1)
        TablPerf = []
        for i in listPerf:
            t = Collectionkpi.find_one({}, {i})
            TablPerf.append({'NomPerf': t[i]['NomPerf'], 'ListeKPI': t[i]['ListeKPI']})

        if(PerfToUpdate is not None):
          ### les perf à mettre à jour
          for j in PerfToUpdate:
            for i in TablPerf:
                if (j == i['NomPerf']):
                    if (i['NomPerf'].strip() == "commercial"):
                      CollectionPerformance.update_one({"PerfCom.ListeKPI.Nom_KPI": org_nameKpi },
                                                     {"$set":
                                                          {"PerfCom.ListeKPI.$.Nom_KPI": nameKpi,
                                                          "PerfCom.ListeKPI.$.Desc_KPI": descr,
                                                      }})


                    if (i['NomPerf'].strip() == "social"):
                        CollectionPerformance.update_one({"PerfSoc.ListeKPI.Nom_KPI": org_nameKpi, },
                                                     {"$set":
                                                          {"PerfSoc.ListeKPI.$.Nom_KPI": nameKpi,
                                                           "PerfSoc.ListeKPI.$.Desc_KPI": descr,
                                                           }})

                    if (i['NomPerf'].strip() == "competitive"):
                        CollectionPerformance.update_one({"PerfConc.ListeKPI.Nom_KPI": org_nameKpi, },
                                                 {"$set":
                                                      {"PerfConc.ListeKPI.$.Nom_KPI": nameKpi,
                                                       "PerfConc.ListeKPI.$.Desc_KPI": descr,
                                                       }})

                    if (i['NomPerf'].strip() == "environnemental"):
                        CollectionPerformance.update_one({"PerfEnv.ListeKPI.Nom_KPI": org_nameKpi, },
                                                     {"$set":
                                                          {"PerfEnv.ListeKPI.$.Nom_KPI": nameKpi,
                                                           "PerfEnv.ListeKPI.$.Desc_KPI": descr,
                                                           }})
                    if (i['NomPerf'].strip() == "organizational"):
                        CollectionPerformance.update_one({"organizational.ListeKPI.Nom_KPI": org_nameKpi, },
                                                 {"$set":
                                                      {"organizational.ListeKPI.$.Nom_KPI": nameKpi,
                                                       "organizational.ListeKPI.$.Desc_KPI": descr,
                                                       }})
                    if (i['NomPerf'].strip() == "production"):
                        CollectionPerformance.update_one({"production.ListeKPI.Nom_KPI": org_nameKpi, },
                                                 {"$set":
                                                      {"production.ListeKPI.$.Nom_KPI": nameKpi,
                                                       "production.ListeKPI.$.Desc_KPI": descr,
                                                       }})
                    if (i['NomPerf'].strip() == "financial"):
                        CollectionPerformance.update_one({"financial.ListeKPI.Nom_KPI": org_nameKpi, },
                                                 {"$set":
                                                      {"financial.ListeKPI.$.Nom_KPI": nameKpi,
                                                       "financial.ListeKPI.$.Desc_KPI": descr,
                                                       }})
                    if (i['NomPerf'].strip() == "societal"):
                        CollectionPerformance.update_one({"societal.ListeKPI.Nom_KPI": org_nameKpi, },
                                                 {"$set":
                                                      {"societal.ListeKPI.$.Nom_KPI": nameKpi,
                                                       "societal.ListeKPI.$.Desc_KPI": descr,
                                                       }})
                    if (i['NomPerf'].strip() == "strategic"):
                        CollectionPerformance.update_one({"strategic.ListeKPI.Nom_KPI": org_nameKpi, },
                                                 {"$set":
                                                      {"strategic.ListeKPI.$.Nom_KPI": nameKpi,
                                                       "strategic.ListeKPI.$.Desc_KPI": descr,
                                                       }})
                    if (i['NomPerf'].strip() == "economic"):
                        CollectionPerformance.update_one({"economic.ListeKPI.Nom_KPI": org_nameKpi, },
                                                 {"$set":
                                                      {"economic.ListeKPI.$.Nom_KPI": nameKpi,
                                                       "economic.ListeKPI.$.Desc_KPI": descr,
                                                       }})
                    else:
                        PerfInd1 = "Perf.ListeKPI.Nom_KPI"
                        PerfInd2 = "Perf.ListeKPI.$.Nom_KPI"
                        PerfDescr = "Perf.ListeKPI.$.Desc_KPI"

                        PerfInd1 = PerfInd1.replace("Perf", j.strip())
                        PerfInd2 = PerfInd2.replace("Perf", j.strip())
                        PerfDescr = PerfDescr.replace("Perf", j.strip())

                        CollectionPerformance.update_one({PerfInd1: org_nameKpi, },
                                                 {"$set":
                                                      {PerfInd2: nameKpi,
                                                       PerfDescr: descr,
                                                       }})

        #les perf à ajouter

        if (PerfToAdd is not None):
            print("voilaaaaaa")
            List_performances = list(CollectionPerformance.find())
            if (ListAxes[0] == "commercial"):
                              Listp = List_performances[0]["PerfCom"]["ListeKPI"]
                              for x in Listp:
                                  if (x["Nom_KPI"] == org_nameKpi):
                                      newKpi = x
            elif (ListAxes[0]   == "social"):
                              Listp = List_performances[0]["PerfSoc"]["ListeKPI"]
                              for x in Listp:
                                  if (x["Nom_KPI"] == org_nameKpi):
                                      newKpi = x
            elif (ListAxes[0]  == "competitive"):
                              print("competitiiiiiiiiiiive")
                              Listp = List_performances[0]["PerfConc"]["ListeKPI"]
                              for x in Listp:
                                  if (x["Nom_KPI"] == org_nameKpi):
                                      newKpi = x

            elif (ListAxes[0]  == "economic"):
                              Listp = List_performances[0]["economic"]["ListeKPI"]
                              for x in Listp:
                                  if (x["Nom_KPI"] == org_nameKpi):
                                      newKpi = x

            elif (ListAxes[0]  == "organizational"):
                              Listp = List_performances[0]["organizational"]["ListeKPI"]
                              for x in Listp:
                                  if (x["Nom_KPI"] == org_nameKpi):
                                      newKpi = x

            elif (ListAxes[0]   == "financial"):
                              Listp = List_performances[0]["financial"]["ListeKPI"]
                              for x in Listp:
                                  if (x["Nom_KPI"] == org_nameKpi):
                                      newKpi = x


            elif (ListAxes[0] == "environnemental"):
                              Listp = List_performances[0]["PerfEnv"]["ListeKPI"]
                              for x in Listp:
                                  if (x["Nom_KPI"] == org_nameKpi):
                                      newKpi = x


            """ else:
                              print("new axe")
                              Listp = List_performances[0]["PerfEnv"]["ListeKPI"]
                              for x in Listp:
                                  if (x["Nom_KPI"] == org_nameKpi):
                                      newKpi = x"""


            print("newKpi")
            print(newKpi)
            print(newKpi["Nom_KPI"])
            newKpi["Nom_KPI"]= nameKpi
            newKpi["Desc_KPI"]=descr
            #newKpi["Type"]=type

            # verifier d abord qu ils n existent pas deja dans la BDD
            #newKpi= newKpi.lower()
            print("ccc")
            print(PerfToAdd)

            for j in PerfToAdd:
                print(j)

                for i in TablPerf:
                    if (j == i['NomPerf']):
                        print(j)

                        if(i['NomPerf'].strip() =="commercial"):
                                exist = CollectionPerformance.find_one({'PerfCom.$.ListeKPI.Nom_KPI': newKpi})
                                if (exist is not None):
                                    print("exists")
                                else:
                                   CollectionPerformance.update({}, {"$push": {"PerfCom.ListeKPI": newKpi}})
                        elif(i['NomPerf'].strip() =="social"):

                            exist = CollectionPerformance.find_one({'PerfSoc.$.ListeKPI.Nom_KPI': newKpi})
                            if (exist is not None):
                                print("exists")
                            else:
                               CollectionPerformance.update({}, {"$push": {"PerfSoc.ListeKPI": newKpi}})

                        elif(j.strip() =="competitive"):
                            exist = CollectionPerformance.find_one({'PerfConc.$.ListeKPI.Nom_KPI': newKpi})
                            if (exist is not None):
                                print("exists")
                            else:
                               CollectionPerformance.update({}, {"$push": {"PerfConc.ListeKPI": newKpi}})

                        elif(i['NomPerf'].strip() =="environnemental"):
                            exist = CollectionPerformance.find_one({'PerfEnv.$.ListeKPI.Nom_KPI': newKpi})
                            if (exist is not None):
                                print("exists")
                            else:
                               CollectionPerformance.update({}, {"$push": {"PerfEnv.ListeKPI": newKpi}})

                        elif(i['NomPerf'].strip() =="organizational"):
                            exist = CollectionPerformance.find_one({'organizational.$.ListeKPI.Nom_KPI': newKpi})
                            if (exist is not None):
                                print("exists")
                            else:
                               CollectionPerformance.update({}, {"$push": {"organizational.ListeKPI": newKpi}})

                        elif(i['NomPerf'].strip() =="financial"):
                            exist = CollectionPerformance.find_one({'financial.$.ListeKPI.Nom_KPI': newKpi})
                            if (exist is not None):
                                print("exists")
                            else:
                               CollectionPerformance.update({}, {"$push": {"financial.ListeKPI": newKpi}})

                        elif(i['NomPerf'].strip() =="economic"):
                            exist = CollectionPerformance.find_one({'economic.$.ListeKPI.Nom_KPI': newKpi})
                            if (exist is not None):
                                print("exists")
                            else:
                               CollectionPerformance.update({}, {"$push": {"economic.ListeKPI": newKpi}})

                        else:
                            print(i['NomPerf'])
                            PerfInd = "Perf.$.ListeKPI.Nom_KPI"
                            PerfInd = PerfInd.replace("Perf", j.strip())

                            PerfInd2 = "Perf.ListeKPI"
                            PerfInd2 = PerfInd2.replace("Perf", j.strip())

                            exist = CollectionPerformance.find_one({PerfInd: newKpi})
                            if (exist is not None):
                                print("exists")
                            else:

                               CollectionPerformance.update({}, {"$push": {PerfInd2: newKpi}})





        # supprimer l'indicateur dans la liste de l'ancienne perf ou il y était
        if(PerfToDelete is not None):

            for j in PerfToDelete:
                for i in TablPerf:
                    if (j == i['NomPerf']):
                            print(j)
                            if(i['NomPerf'].strip() =="commercial"):
                                    CollectionPerformance.update_one({}, {"$pull": {"PerfCom.ListeKPI": {"Nom_KPI": org_nameKpi}}})
                            elif (i['NomPerf'].strip()  == "social"):
                                    CollectionPerformance.update_one({}, {"$pull": {"PerfSoc.ListeKPI": {"Nom_KPI": org_nameKpi}}})

                            elif (i['NomPerf'].strip()  == "competitive"):
                                    CollectionPerformance.update_one({}, {"$pull": {"PerfConc.ListeKPI": {"Nom_KPI": org_nameKpi}}})

                            elif (i['NomPerf'].strip()  == "organizational"):
                                    CollectionPerformance.update_one({}, {"$pull": {"organizational.ListeKPI": {"Nom_KPI": org_nameKpi}}})

                            elif (i['NomPerf'].strip()  == "financial"):
                                    CollectionPerformance.update_one({}, {"$pull": {"financial.ListeKPI": {"Nom_KPI": org_nameKpi}}})

                            elif (i['NomPerf'].strip()  == "economic"):
                                    CollectionPerformance.update_one({}, {"$pull": {"economic.ListeKPI": {"Nom_KPI": org_nameKpi}}})
                            elif (i['NomPerf'].strip() == "environnemental"):
                                    CollectionPerformance.update_one({}, {"$pull": {"PerfEnv.ListeKPI": {"Nom_KPI": org_nameKpi}}})
                            else:
                                PerfInd = "Perf.ListeKPI"
                                PerfInd = PerfInd.replace("Perf", i['NomPerf'].strip())
                                CollectionPerformance.update_one({}, {"$pull": {PerfInd: {"Nom_KPI": org_nameKpi}}})

    return render(request, "home/TableReferentiel.html")




def Update_Concurrent(request):

    #old values
    id = request.POST.get("id", None)

    #new values
    Name2 = request.POST.get("Name2", None)
    Nbr_Subscribes2 = request.POST.get("Nbr_Subscribes2", None)
    CA2 = request.POST.get("CA2", None)
    Reputation2 = request.POST.get("Reputation2", None)


    if request.method == "POST":
        print(request.POST)

        #new values
        Name2 = Name2.strip()
        Nbr_Subscribes2 = Nbr_Subscribes2.strip()
        CA2 = CA2.strip()
        Reputation2 = Reputation2.strip()

        myclient = MongoClient('localhost', 27017)
        CollectionOperateur = myclient.myNewDb.get_collection("OPERATEUR")
        print(id)
        id=int(id)

        print(type(id))
        try:
          CollectionOperateur.update_one({"Concurrent.idConc": id  },
                                         {"$set":
                                               {
                                               "Concurrent.$.Nom_Concurrent": Name2,
                                               }})
        except Exception as e:

            # "Concurrent.Nombre_Abonnes": Nbr_Subscribes2,
            # "Concurrent.CA_Conc": CA2,
            # "Concurrent.Reputation": Reputation2,
            print("Exception :", str(e))
    return render(request, "home/TableReferentiel.html")




def Delete_Concurrent(request):

    id = request.POST.get("id", None)
    if request.method == "POST":
        print(request.POST)
        myclient = MongoClient('localhost', 27017)
        CollectionOperateur = myclient.myNewDb.get_collection("OPERATEUR")
        print(id)
        id=int(id)
        CollectionOperateur.update_one({}, {"$pull": {"Concurrent": {"idConc": id }}})

    return render(request, "home/TableReferentiel.html")








def Update_Employe(request):

    #old values
    id = request.POST.get("id", None)

    #new values
    FirstName2 = request.POST.get("FirstName2", None)
    LastName2 = request.POST.get("LastName2", None)
    Date_birth2 = request.POST.get("Date_birth2", None)
    Admission_Date2 = request.POST.get("Admission_Date2", None)
    Salary2 = request.POST.get("Salary2", None)


    if request.method == "POST":
        print(request.POST)

        #new values
        FirstName2 = FirstName2.strip()
        LastName2 = LastName2.strip()
        Date_birth2 = Date_birth2.strip()
        Admission_Date2 = Admission_Date2.strip()
        Salary2 = Salary2.strip()

        myclient = MongoClient('localhost', 27017)
        CollectionOperateur = myclient.myNewDb.get_collection("OPERATEUR")
        id = id
        id=int(id)
        try:

          CollectionOperateur.update_one({ "Employés.idEmploye": id },
                                            {"$set":
                                               {
                                               "Employés.$.Employe_Nom": FirstName2,
                                               "Employés.$.Employe_Prenom": LastName2,
                                               "Employés.$.Date_Naissance": Date_birth2,
                                               "Employés.$.Date_Debut_Travail": Admission_Date2,
                                               "Employés.$.Salaire": Salary2,
                                               }})
        except Exception as e:
          print("Exception :", str(e))
    return render(request, "home/TableReferentiel.html")

def Delete_Employe(request):

    id = request.POST.get("id", None)

    if request.method == "POST":
        print(request.POST)
        print(id)
        myclient = MongoClient('localhost', 27017)
        CollectionOperateur = myclient.myNewDb.get_collection("OPERATEUR")
        id = id
        id=int(id)
        CollectionOperateur.update_one({}, {"$pull": {"Employés": {"idEmploye": id }}})

    return render(request, "home/TableReferentiel.html")





def Delete_Entreprise(request):

    id = request.POST.get("id", None)

    if request.method == "POST":
        print(request.POST)
        myclient = MongoClient('localhost', 27017)
        CollectionOperateur = myclient.myNewDb.get_collection("OPERATEUR")
        id = id
        id=int(id)

        CollectionOperateur.update_one({}, {"$pull": {"Abonnes": {"idEntr": id }}})

    return render(request, "home/TableReferentiel.html")




def Update_Entreprise(request):
    id = request.POST.get("id", None)

    #new values
    NumTel2 = request.POST.get("NumTel2", None)
    LastName2 = request.POST.get("LastName2", None)
    Date_birth2 = request.POST.get("Date_birth2", None)
    Contract_Date2 = request.POST.get("Contract_Date2", None)
    Wilaya2 = request.POST.get("Wilaya2", None)


    if request.method == "POST":
        print(request.POST)
        NumTel2 = NumTel2.strip()
        LastName2 = LastName2.strip()
        Date_birth2 = Date_birth2.strip()
        Contract_Date2 = Contract_Date2.strip()
        Wilaya2 = Wilaya2.strip()

        myclient = MongoClient('localhost', 27017)
        CollectionOperateur = myclient.myNewDb.get_collection("OPERATEUR")
        id = id
        id=int(id)
        try:

          CollectionOperateur.update_one({"Abonnes.idEntr": id },
                                         {"$set":
                                               {
                                                   "Abonnes.$.Numero_Tel": NumTel2,
                                                   "Abonnes.$.Client_Nom": LastName2,
                                                   "Abonnes.$.Date": Date_birth2,
                                                   "Abonnes.$.Contrat":{"Date_Debut_Contrat": Contract_Date2},
                                                   "Abonnes.$.Adresse": Wilaya2,

                                               }})
        except Exception as e:
          print("Exception :", str(e))

    return render(request, "home/TableReferentiel.html")





def Update_Particulier(request):


    id = request.POST.get("id", None)

    #new values
    NumTel2 = request.POST.get("NumTel2", None)
    FirstName2 = request.POST.get("FirstName2", None)
    LastName2 = request.POST.get("LastName2", None)
    Date_birth2 = request.POST.get("Date_birth2", None)
    Contract_Date2 = request.POST.get("Contract_Date2", None)
    Wilaya2 = request.POST.get("Wilaya2", None)


    if request.method == "POST":
        print(request.POST)
        NumTel2 = NumTel2.strip()
        FirstName2 = FirstName2.strip()
        LastName2 = LastName2.strip()
        Date_birth2 = Date_birth2.strip()
        Contract_Date2 = Contract_Date2.strip()
        Wilaya2 = Wilaya2.strip()

        myclient = MongoClient('localhost', 27017)
        CollectionOperateur = myclient.myNewDb.get_collection("OPERATEUR")
        id = id
        id=int(id)
        try:

          CollectionOperateur.update_one({"Abonnes.idPart": id },
                                         {"$set":
                                               {
                                                   "Abonnes.$.Numero_Tel": NumTel2,
                                                   "Abonnes.$.Client_Prenom": FirstName2,
                                                   "Abonnes.$.Client_Nom": LastName2,
                                                   "Abonnes.$.Date": Date_birth2,
                                                   "Abonnes.$.Contrat":{"Date_Debut_Contrat": Contract_Date2},
                                                   "Abonnes.$.Adresse": Wilaya2,

                                               }})
        except Exception as e:
          print("Exception :", str(e))

    return render(request, "home/TableReferentiel.html")




def Delete_Particulier(request):

    id = request.POST.get("id", None)

    if request.method == "POST":
        print(request.POST)
        myclient = MongoClient('localhost', 27017)
        CollectionOperateur = myclient.myNewDb.get_collection("OPERATEUR")
        id = id
        id=int(id)

        CollectionOperateur.update_one({}, {"$pull": {"Abonnes": {"idPart": id }}})

    return render(request, "home/TableReferentiel.html")













#####DATA STAKEHOLDERS #####
Operateur = myclient.myNewDb.get_collection("OPERATEUR")
def _Export_Employes_To_JSON(request):

        ListOperateur = list(Operateur.find({}))[0]

        data = []
        for x in ListOperateur["Employés"]:
            data.append(x)
        with open('apps/static/FilesJson/Employes.json', 'w') as json_file:
            json.dump(data, json_file)
        json_file.close()

        return render(request, "home/Data_Employes.html")




def _Export_Entreprises_To_JSON(request):
        ListOperateur = list(Operateur.find({}))[0]

        data = []
        for x in ListOperateur["Abonnes"]:
            if (x["Type_Client"] == "Entreprise"):
                data.append(x)

        with open('apps/static/FilesJson/Entreprises.json', 'w') as json_file:
            json.dump(data, json_file)
        json_file.close()
        return render(request, "home/Data_Entreprises.html")


def _Export_Concurrent_To_JSON(request):
        ListOperateur = list(Operateur.find({}))[0]

        data = []
        for x in ListOperateur["Concurrent"]:
            data.append(x)
        with open('apps/static/FilesJson/Concurrent.json', 'w') as json_file:
            json.dump(data, json_file)
        json_file.close()



        return render(request, "home/Data_Concurrents.html")

def _Export_Particuliers_To_JSON(request):
        ListOperateur = list(Operateur.find({}))[0]

        data = []
        for x in ListOperateur["Abonnes"]:
            if (x["Type_Client"] == "Particulier"):
                data.append(x)

        with open('apps/static/FilesJson/Particuliers.json', 'w') as json_file:
            json.dump(data, json_file)
        json_file.close()

        return render(request, "home/Data_Particuliers.html")

def _Export_Employes_To_CSV(request):
        ListOperateur = list(Operateur.find({}))[0]

        data = []
        for x in ListOperateur["Employés"]:

            if (x["Absences"] is None):
                x["Absences"] = "null"
            data.append(x)

        headersCSV = ['idEmploye', 'Employe_Prenom', 'Employe_Nom', 'Date_Naissance', 'Date_Debut_Travail',
                      'Date_Demission', 'Salaire', 'Avis_Employe', 'Nbr_Taches_Accomplies_a_Temps',
                      'Nbr_Taches_Non_Accomplies', 'Absences']

        with open('apps/static/FilesCSV/Employes.csv', 'w', newline='') as f_object:
            dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
            csv_writer = csv.writer(f_object, delimiter=',')
            csv_writer.writerow(headersCSV)
            for i in data:
                dictwriter_object.writerow(i)
        f_object.close()

        text = open("apps/static/FilesCSV/Employes.csv", "r")
        text = ''.join([i for i in text])
        text = text.replace("ï", "i").replace("É", "E").replace("é", "e").replace("ê", "e").replace("è", "e").replace(
            "à", "a").replace("ç", "c").replace(",,", ",null,").replace("{", "").replace("}", "").replace("[",
                                                                                                          "").replace(
            "]", "")
        x = open("apps/static/FilesCSV/Employes.csv", "w")
        x.writelines(text)
        x.close()

        return render(request, "home/Data_Employes.html")


def _Export_Entreprises_To_CSV(request):
        ListOperateur = list(Operateur.find({}))[0]

        data = []
        for x in ListOperateur["Abonnes"]:
            if (x["Type_Client"] == "Entreprise"):

                if (x["Client_Prenom"] is None):
                    x["Client_Prenom"] = "null"

                if (x["Resiliation"] is None):
                    x["Resiliation"] = "null"

                if (x["Reclamation"] is None):
                    x["Reclamation"] = "null"

                if (x["Service"] is None):
                    x["Service"] = "null"

                if (x["Forfaits"] is None):
                    x["Forfaits"] = "null"

                data.append(x)

        headersCSV = ['idEntr', 'Numero_Tel', 'Type_Client', 'Categorie_Client', 'Client_Prenom', 'Client_Nom',
                      'Adresse',
                      'Date', 'CA', 'Contrat', 'Service', 'Forfaits', 'Reclamation', 'Avis_Abonne', 'Resiliation',
                      'Reseau_Social_Operateur']


        with open('apps/static/FilesCSV/Entreprises.csv', 'w', newline='') as f_object:
            dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
            csv_writer = csv.writer(f_object, delimiter=',')
            csv_writer.writerow(headersCSV)
            for i in data:
                dictwriter_object.writerow(i)
        f_object.close()


        text = open("apps/static/FilesCSV/Entreprises.csv", "r")
        text = ''.join([i for i in text])
        text = text.replace("ï", "i").replace("É", "E").replace("é", "e").replace("ê", "e").replace("è", "e").replace("à", "a").replace("ç", "c").replace(",,", ",null,").replace("{", "").replace("}", "").replace("[",
                   "").replace("]", "")
        x = open("apps/static/FilesCSV/Entreprises.csv", "w")
        x.writelines(text)
        x.close()

        return render(request, "home/Data_Entreprises.html")


def _Export_Particuliers_To_CSV(request):
        ListOperateur = list(Operateur.find({}))[0]

        data = []
        for x in ListOperateur["Abonnes"]:
            if (x["Type_Client"] == "Particulier"):

                if (x["Resiliation"] is None):
                    x["Resiliation"] = "null"

                if (x["Reclamation"] is None):
                    x["Reclamation"] = "null"

                if (x["Service"] is None):
                    x["Service"] = "null"

                if (x["Forfaits"] is None):
                    x["Forfaits"] = "null"

                data.append(x)

        headersCSV = ['idPart', 'Numero_Tel', 'Type_Client', 'Categorie_Client', 'Client_Prenom', 'Client_Nom',
                      'Adresse',
                      'Date', 'CA', 'Contrat', 'Service', 'Forfaits', 'Reclamation', 'Avis_Abonne', 'Resiliation',
                      'Reseau_Social_Operateur']

        with open('apps/static/FilesCSV/Particuliers.csv', 'w', newline='') as f_object:
            dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
            csv_writer = csv.writer(f_object, delimiter=',')
            csv_writer.writerow(headersCSV)
            for i in data:
                dictwriter_object.writerow(i)
        f_object.close()

        text = open("apps/static/FilesCSV/Particuliers.csv", "r")
        text = ''.join([i for i in text])
        text = text.replace("ï", "i").replace("É", "E").replace("é", "e").replace("ê", "e").replace("è", "e").replace(
            "à", "a").replace("ç", "c").replace(",,", ",null,").replace("{", "").replace("}", "").replace("[",
                                                                                                          "").replace(
            "]", "")
        x = open("apps/static/FilesCSV/Particuliers.csv", "w")
        x.writelines(text)
        x.close()

        return render(request, "home/Data_Particuliers.html")

def _Export_Concurrents_To_CSV(request):
        ListOperateur = list(Operateur.find({}))[0]

        data = []
        for x in ListOperateur["Concurrent"]:
            data.append(x)

        headersCSV = ['idConc', 'Nom_Concurrent', 'Nombre_Abonnes', 'CA_Conc', 'Taux_couverture', 'Reputation']

        with open('apps/static/FilesCSV/Concurrents.csv', 'w', newline='') as f_object:
            dictwriter_object = DictWriter(f_object, fieldnames=headersCSV)
            csv_writer = csv.writer(f_object, delimiter=',')
            csv_writer.writerow(headersCSV)
            for i in data:
                dictwriter_object.writerow(i)
        f_object.close()

        text = open("apps/static/FilesCSV/Concurrents.csv", "r")
        text = ''.join([i for i in text])
        text = text.replace("ï", "i").replace("É", "E").replace("é", "e").replace("ê", "e").replace("è", "e").replace(
            "à", "a").replace("ç", "c").replace(",,", ",null,").replace("{", "").replace("}", "").replace("[",
                                                                                                          "").replace(
            "]", "")
        x = open("apps/static/FilesCSV/Concurrents.csv", "w")
        x.writelines(text)
        x.close()

        return render(request, "home/Data_Concurrents.html")





# Exporter tte la BDD
def _Connection(NomCollection):
        Collection_Operateur = myclient.myNewDb.get_collection(NomCollection)
        return Collection_Operateur

Collection_Operateur = _Connection("OPERATEUR")

def _Export_All_DataBase_To_JSON(request):
        cursor = Collection_Operateur.find()
        mongo_docs = list(cursor)

        # mongo_docs = mongo_docs[:50] # slice the list
        print("total docs:", len(mongo_docs))

        # create an empty DataFrame for storing documents
        docs = pandas.DataFrame(columns=[])

        # iterate over the list of MongoDB dict documents
        for num, doc in enumerate(mongo_docs):
            # convert ObjectId() to str
            doc["_id"] = str(doc["_id"])

            # get document _id from dict
            doc_id = doc["_id"]

            # create a Series obj from the MongoDB dict
            series_obj = pandas.Series(doc, name=doc_id)

            # append the MongoDB Series obj to the DataFrame obj
            docs = docs.append(series_obj)

        """  # only print every 10th document
        if num % 10 == 0:
            print (type(doc))
            print (type(doc["_id"]))
            print (num, "--", doc, "\n")
        """

        # export the MongoDB documents as a JSON file

        docs.to_json("apps/static/FilesJson/All_BDD_Operateur.json")

        # have Pandas return a JSON string of the documents
        json_export = docs.to_json()  # return JSON data

def _Export_All_DataBase_To_CSV(request):
        cursor = Collection_Operateur.find()
        mongo_docs = list(cursor)

        # restrict the number of docs to export
        print("total docs:", len(mongo_docs))

        # create an empty DataFrame for storing documents
        docs = pandas.DataFrame(columns=[])

        # iterate over the list of MongoDB dict documents
        for num, doc in enumerate(mongo_docs):
            # convert ObjectId() to str
            doc["_id"] = str(doc["_id"])

            # get document _id from dict
            doc_id = doc["_id"]

            # create a Series obj from the MongoDB dict
            series_obj = pandas.Series(doc, name=doc_id)

            # append the MongoDB Series obj to the DataFrame obj
            docs = docs.append(series_obj)

        # export MongoDB documents to a CSV file
        docs.to_csv("apps/static/FilesCSV/All_BDD_Operateur.csv", ",")  # CSV delimited by commas

        # export MongoDB documents to CSV
        csv_export = docs.to_csv(sep=",")  # CSV delimited by commas

        text = open("apps/static/FilesCSV/All_BDD_Operateur.csv", "r")
        text = ''.join([i for i in text])
        text = text.replace("ï", "i").replace("É", "E").replace("é", "e").replace("ê", "e").replace("è", "e").replace(
            "à", "a").replace("ç", "c").replace(",,", ",null,").replace("{", "").replace("}", "").replace("[",
                                                                                                          "").replace(
            "]", "")
        x = open("apps/static/FilesCSV/All_BDD_Operateur.csv", "w")
        x.writelines(text)
        x.close()




        ##### import Data ####






def _ImportDataCompanies_Json(request):

    myclient = MongoClient('localhost', 27017)
    CollectionOperateur = myclient.myNewDb.get_collection("OPERATEUR")

    SelectedFile = request.POST.get("SelectedFile", None)
    path="apps/static/DataFiles/FichierX"
    fichier=str(SelectedFile)
    print(fichier)
    path=path.replace("FichierX",fichier)
    print(path)

    if request.method == "POST":
        print(request.POST)
        try:
            #Supp_Caractere_speciaux_Entrp
            text = open(path, "r")
            text = ''.join([i for i in text])
            text = text.replace("ï", "i").replace("É", "E").replace("é", "e").replace("ê", "e").replace("è", "e").replace("à", "a").replace("Ã©", "A").replace("ii¿½", "").replace("��", "").replace("¿½", "").replace("ç", "c").replace(",,", ",null,").replace("!", "").replace("$", "").replace("£", "").replace("^", "").replace("ù", "").replace("~", "").replace("§", "")
            x = open(path, "w")
            x.writelines(text)
            x.close()

            #Retirer_Unite_CA_Entreprises():
            text = open(path, "r")
            text = ''.join([i for i in text])

            text = text.replace("Dinars", "").replace("dinars", "").replace("Dinars_Algeriens", "").replace("_Algeriens", "")
            x = open(path, "w")
            x.writelines(text)
            x.close()

            #Convertir_en_valeurs_numerique
            with open(path, "r") as File_entrep:
                data2 = load(File_entrep)
                for i in data2:
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

            File_entrep.close()
            with open(path, 'w') as File_entrep:
                json.dump(data2, File_entrep)



            #import data to Abonnes
            with open(path) as file:
                file_data = json.load(file)

            #if isinstance(file_data, list):
            print(type(file_data))
            #for i in file_data:
                #CollectionOperateur.update_one({}, {"$push": {"Abonnes": i}})

            file.close()

        except Exception as e:
         print("Exception! check if the file structure is correct")

    return render(request, "home/Data_Entreprises.html")


def _ImportDataParticuliers_Json(request):


    myclient = MongoClient('localhost', 27017)
    CollectionOperateur = myclient.myNewDb.get_collection("OPERATEUR")

    SelectedFile = request.POST.get("SelectedFile", None)
    path="/home/nassim/Desktop/telecom/apps/static/DataFiles/FichierX"
    fichier=str(SelectedFile)
    path=path.replace("FichierX",fichier)


    if request.method == "POST":
        print(request.POST)
        try:

            #Filtrer_donnees_Particulier
            with open('/home/nassim/Desktop/telecom/apps/static/DataFiles/'+fichier, "r") as File_part:
                data1 = load(File_part)

                for i in data1:
                    if ("Situation_familiale" in i and "professionClient" in i and "lieu_Travail" in i):
                        del i["Situation_familiale"]
                        del i["professionClient"]
                        del i["lieu_Travail"]

            File_part.close()
            with open(path, 'w') as File_part:
                json.dump(data1, File_part)
            File_part.close()

            #Supp_Caractere_speciaux
            text = open(path, "r")
            text = ''.join([i for i in text])
            text = text.replace("ï", "i").replace("É", "E").replace("é", "e").replace("ê", "e").replace("è", "e").replace("à", "a").replace("Ã©", "A").replace("ii¿½", "").replace("��", "").replace("¿½", "").replace("ç", "c").replace(",,", ",null,").replace("!", "").replace("$", "").replace("£", "").replace("^", "").replace("ù", "").replace("~", "").replace("§", "")
            x = open(path, "w")
            x.writelines(text)
            x.close()

            #Retirer_Unite_CA_
            text = open(path, "r")
            text = ''.join([i for i in text])
            text = text.replace("Dinars", "").replace("dinars", "").replace("Dinars_Algeriens", "").replace("_Algeriens",
                                                                                                            "")
            x = open(path, "w")
            x.writelines(text)
            x.close()

            #Convertir_en_valeurs_numerique
            with open(path, "r") as File_entrep:
                data2 = load(File_entrep)
                for i in data2:
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

            File_entrep.close()
            with open(path, 'w') as File_entrep:
                json.dump(data2, File_entrep)



            #import data to Abonnes
            with open(path) as file:
                file_data = json.load(file)

            #if isinstance(file_data, list):
            print(type(file_data))
            for i in file_data:
                CollectionOperateur.update_one({}, {"$push": {"Abonnes": i}})

            file.close()
        except Exception as e:
         print("Exception! check if the file structure is correct")

    return render(request, "home/Data_Particuliers.html")


def _ImportDataConcurrents_Json(request):

    myclient = MongoClient('localhost', 27017)
    CollectionOperateur = myclient.myNewDb.get_collection("OPERATEUR")

    SelectedFile = request.POST.get("SelectedFile", None)
    path="apps/static/DataFiles/FichierX"
    fichier=str(SelectedFile)
    path=path.replace("FichierX",fichier)


    if request.method == "POST":
        print(request.POST)
        try:

            #import data
            with open(path) as file:
                file_data = json.load(file)

            #if isinstance(file_data, list):
            print(type(file_data))
            for i in file_data:
               CollectionOperateur.update_one({}, {"$push": {"Concurrent": i}})

            file.close()

        except Exception as e:
            print("Exception! check if the file structure is correct")

    return render(request, "home/Data_Concurrents.html")


def _ImportDataEmployes(request):
    myclient = MongoClient('localhost', 27017)
    CollectionOperateur = myclient.myNewDb.get_collection("OPERATEUR")

    SelectedFile1 = request.POST.get("SelectedFile1", None)
    SelectedFile2 = request.POST.get("SelectedFile2", None)
    path="apps/static/DataFiles/FichierX"
    path2="apps/static/DataFiles/FichierX"


    path=path.replace("FichierX",SelectedFile1) #employes
    path2=path2.replace("FichierX",SelectedFile2) #Absences

    print(path)
    print(path2)

    if request.method == "POST":
        print("heeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeerrerweeeeeeeeeeeeeeee")
        print(request.POST)
        try:

            #Supp_Caractere_speciaux_Employes

            text = open(path, "r")
            text = ''.join([i for i in text])
            text = text.replace("ï", "i").replace("É", "E").replace("Ã©", "A").replace("ii¿½", "").replace("��",
                                                                                                           "").replace("¿½",
                                                                                                                       "").replace(
                "é", "e").replace("ê", "e").replace("è", "e").replace("à", "a").replace("ç", "c").replace(",,",
                                                                                                          ",null,").replace(
                "{", "").replace("}", "").replace("[", "").replace("]", "").replace("$", "").replace("£", "").replace("^",
                                                                                                                      "").replace(
                "ù", "").replace("~", "").replace("§", "")
            x = open(path, "w")
            x.writelines(text)
            # print(text)
            x.close()

            #Supp_Caractere_speciaux_Absence
            text = open(path2, "r")
            text = ''.join([i for i in text])
            text = text.replace("ï", "i").replace("É", "E").replace("é", "e").replace("ê", "e").replace("è", "e").replace(
                "à", "a").replace("ç", "c").replace(",,", ",null,").replace("{", "").replace("}", "").replace("[",
                                                                                                              "").replace(
                "]", "").replace("$", "").replace("£", "").replace("^", "").replace("ù", "").replace("~", "").replace("§",
                                                                                                                      "")
            x = open(path2, "w")
            x.writelines(text)
            x.close()


            with open(path, "r") as File_Employee:
                """fichier = csv.reader(File_Employee)
                header=next(fichier)"""

                f = csv.DictReader(File_Employee)

                for row in f:
                    with open(path2, "r") as File_Absences:
                        f2 = csv.DictReader(File_Absences)
                        List = []
                        a = 0
                        for row2 in f2:
                            if (int(row2['Id_Employee']) == int(row['id'])):
                                a = 1
                                abs = {
                                    "Date_Absence": row2['Date_Absence'],
                                    "Raison": row2['Raison']
                                }
                                List.append(abs)
                            if (a == 1 and row2['Id_Employee'] != row['id']):
                                break
                        if (a == 0):
                            List = None
                        if (row['Date_Depart'] == ""):
                            p = None
                        else:
                            p = row['Date_Depart']
                        Employe = {
                            "idEmploye": int(row['id']),
                            "Employe_Prenom": row['Prenom'],
                            "Employe_Nom": row['Nom'],
                            "Date_Naissance": row['Date_Naissance'],
                            "Date_Debut_Travail": row['Date_Debut_Travail'],
                            "Date_Demission": p,
                            "Salaire": int(row['Salaire']),
                            "Avis_Employe": {
                                "Date_Avis": row['Date_Avis'],
                                "Avis_Rating": int(row['Avis_Rating']),
                            },
                            "Nbr_Taches_Accomplies_a_Temps": int(row['Nbr_Taches_Accomplies_a_Temps']),
                            "Nbr_Taches_Non_Accomplies": int(row['Nbr_Taches_Non_Accomplies']),
                            "Absences": List
                        }

                        CollectionOperateur.update_one({}, {"$push": {"Employés": Employe}})

            File_Employee.close()
            File_Absences.close()


        except Exception as e:
            print("Exception! check if the file structure is correct")

    return render(request, "home/Data_Concurrents.html")

@csrf_exempt
def addaxefromfile(request):


    if request.method=="POST":
        listkpi=[]
        dicform=dicform=dict(request.POST)
        namefile=str(dicform["filename"][0])
        filepath='/home/nassim/Desktop/telecom/apps/static/FilesCSV/'+namefile
        with open('/home/nassim/Desktop/telecom/apps/static/FilesCSV/'+namefile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    
                    
                    for item in row:
                        if item != '':
                            nomperf = item
                            break

                    

                    line_count += 1
                elif line_count==1:
                    listcol=row
                    lon=len(listcol)-4
                    
                    line_count += 1
                elif line_count==2:
                    listannee=[]
                    for i in range(2,(lon//2)+2):
                        listannee.append(row[i])

                    
                    line_count += 1
                else:
                    dicval={}
                    dicseuil={}
                    listval=[]
                    listseuil=[]
                    for i in range(2,(lon//2)+2):
                        listval.append(int(row[i]))
                    
                    for i in range((lon//2)+2,len(listcol)-2):
                        listseuil.append(int(row[i]))
                    
                    print(listval)
                    print(listseuil)
                    print(listannee)
                    for i in range(len(listannee)):
                        dicval[listannee[i]]=listval[i]
                        dicseuil[listannee[i]]=listseuil[i]
                    
                    typ=row[len(row)-2]
                    
                    typ=int(typ)
                    
                    listkpi.append({
                        "Nom_KPI": row[0],
                        "Desc_KPI": row[1],
                        "Valeurs_KPI": dicval,
                        "Seuil_KPI": dicseuil,
                        "Type": typ,
                        "Fct_KPI": row[len(row)-1],
                    })


        # listkpi + le nom de la performance depuis le csv
        nouvelleperf={
            "NomPerf": nomperf,
            "ListeKPI": listkpi
        }



                    
        conn = pymongo.MongoClient("mongodb://localhost:27017/")
        db = conn["myNewDb"]
        collection = db["Performance"]
        x=collection.find()

        for i in x:
            lisk=list(i.keys())
            vid=i[lisk[0]]
            

        collection.update_one({"_id":vid}, {"$set": {"Perf"+nomperf: nouvelleperf}})
        msg ="Axis succesfully added"

        return render(request, "home/Configuration.html",{"msg":msg})

    return render(request, "home/addaxefromfile.html")


def redirectlocal(request):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["myNewDb"]
    colle = db["Performance"]
    base = colle.find({})
    clone = base.clone()
    clone2 = base.clone()
    for i in clone:
        keykey=list(i.keys())
    
    keykey.pop(0)
    last =keykey[-1]

    for i in clone2:
        lskpi=i[last]["ListeKPI"][0]["Seuil_KPI"]
    
    year=datetime.today().strftime('%Y')
    if year in lskpi.keys():
        return redirect(choixperflocal)
    else:
        return redirect(fixthresholds)

def redirectagg(request):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["myNewDb"]
    colle = db["Performance"]
    base = colle.find({})
    clone = base.clone()
    clone2 = base.clone()
    for i in clone:
        keykey=list(i.keys())
    
    keykey.pop(0)
    last =keykey[-1]

    for i in clone2:
        lskpi=i[last]["ListeKPI"][0]["Seuil_KPI"]
    
    year=datetime.today().strftime('%Y')
    if year in lskpi.keys():
        return redirect(choixperagg)
    else:
        return redirect(fixthresholds)

def redirectglob(request):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["myNewDb"]
    colle = db["Performance"]
    base = colle.find({})
    clone = base.clone()
    clone2 = base.clone()
    for i in clone:
        keykey=list(i.keys())
    
    keykey.pop(0)
    last =keykey[-1]

    for i in clone2:
        lskpi=i[last]["ListeKPI"][0]["Seuil_KPI"]
    
    year=datetime.today().strftime('%Y')
    if year in lskpi.keys():
        return redirect(attrglobal)
    else:
        return redirect(fixthresholds)
    
    

