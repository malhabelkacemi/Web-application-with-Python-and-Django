# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('charts-commercial/', views.com, name='charts-commercial'),
    path('adminpage/', views.adminpage, name='adminpage'),
    path('traitement/', views.traitement, name="traitement"),
    path('traitementchoixperf/', views.traitementchoixperf, name="traitementchoixperf"),
    path('evalperf/', views.evalperf, name="evalperf"),
    path('add_objectifs/', views.add_objectifs, name="add_objectifs"),
    path('partieprenante/', views.partieprenante, name="partieprenante"),
    path('addattribut/', views.addattribut, name="addattribut"),
    path('showlinks/', views.showlinks, name="showlinks"),
    path('choixperflocal/', views.choixperflocal, name="choixperflocal"),
    path('partprenlocal/', views.partprenlocal, name="partprenlocal"),
    path('attrlocal/', views.attrlocal, name="attrlocal"),
    path('evaluationperf/', views.evaluationperf, name="evaluationperf"),
    path('attrglobal/', views.attrglobal, name="attrglobal"),
    path('choixperagg/', views.choixperagg, name="choixperagg"),
    path('partprenagg/', views.partprenagg, name="partprenagg"),
    path('attragg/', views.attragg, name="attragg"),
    path('fixthresholds/', views.fixthresholds, name="fixthresholds"),
    path('addclass/', views.addclass, name="addclass"),
    path('Update_KPI/', views.Update_KPI, name='Update_KPI'),
    path('Delete_KPI/', views.Delete_KPI, name='Delete_KPI'),
    path('Insert_New_KPI/', views.Insert_New_KPI, name='Insert_New_KPI'),
    path('_AjoutAxe/', views._AjoutAxe, name='_AjoutAxe'),
    path('redirectlocal/', views.redirectlocal, name='redirectlocal'),
    path('redirectglob/', views.redirectglob, name='redirectglob'),
    path('redirectagg/', views.redirectagg, name='redirectagg'),

    path('Delete_Particulier/', views.Delete_Particulier, name='Delete_Particulier'),
    path('Update_Particulier/', views.Update_Particulier, name='Update_Particulier'),

    path('Delete_Entreprise/', views.Delete_Entreprise, name='Delete_Entreprise'),
    path('Update_Entreprise/', views.Update_Entreprise, name='Update_Entreprise'),

    path('Update_Employe/', views.Update_Employe, name='Update_Employe'),
    path('Delete_Employe/', views.Delete_Employe, name='Delete_Employe'),

    path('Update_Concurrent/', views.Update_Concurrent, name='Update_Concurrent'),
    path('Delete_Concurrent/', views.Delete_Concurrent, name='Delete_Concurrent'),

    #partie de metadonnees
    path('Add_Keyword_KPI/', views.Add_Keyword_KPI, name='Add_Keyword_KPI'),
    path('Update_Keyword_KPI/', views.Update_Keyword_KPI, name='Update_Keyword_KPI'),
    path('Remove_Keyword_KPI/', views.Remove_Keyword_KPI, name='Remove_Keyword_KPI'),

    #stakeholders
    path('Save_Stakeholders_Keyword_KPI/', views.Save_Stakeholders_Keyword_KPI, name='Save_Stakeholders_Keyword_KPI'),
    path('Remove_Keyword_Attribute/', views.Remove_Keyword_Attribute, name='Remove_Keyword_Attribute'),



    #Data stakeholders
    path('_Export_Entreprises_To_JSON/', views._Export_Entreprises_To_JSON, name='_Export_Entreprises_To_JSON'),
    path('_Export_Entreprises_To_CSV/', views._Export_Entreprises_To_CSV, name='_Export_Entreprises_To_CSV'),


    path('_Export_Particuliers_To_CSV/', views._Export_Particuliers_To_CSV, name='_Export_Particuliers_To_CSV'),
    path('_Export_Particuliers_To_JSON/', views._Export_Particuliers_To_JSON, name='_Export_Particuliers_To_JSON'),


    path('_Export_Concurrents_To_CSV/', views._Export_Concurrents_To_CSV, name='_Export_Concurrents_To_CSV'),
    path('_Export_Concurrent_To_JSON/', views._Export_Concurrent_To_JSON, name='_Export_Concurrent_To_JSON'),


    path('_Export_Employes_To_CSV/', views._Export_Employes_To_CSV, name='_Export_Employes_To_CSV'),
    path('_Export_Employes_To_JSON/', views._Export_Employes_To_JSON, name='_Export_Employes_To_JSON'),


    #import Data Files in MongoDB
    path('_ImportDataCompanies_Json/', views._ImportDataCompanies_Json, name='_ImportDataCompanies_Json'),
    path('_ImportDataParticuliers_Json/', views._ImportDataParticuliers_Json, name='_ImportDataParticuliers_Json'),
    path('_ImportDataConcurrents_Json/', views._ImportDataConcurrents_Json, name='_ImportDataConcurrents_Json'),
    path('_ImportDataEmployes/', views._ImportDataEmployes, name='_ImportDataEmployes'),
    path('addaxefromfile/', views.addaxefromfile, name="addaxefromfile"),

    


    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
