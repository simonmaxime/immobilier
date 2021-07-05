# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 15:21:02 2021

On cherhce à associer chaque section cadastrale à des coordonnées GPS

Origine des fichier JSON :
https://cadastre.data.gouv.fr/datasets/cadastre-etalab

codes communes : 
https://www.data.gouv.fr/en/datasets/base-officielle-des-codes-postaux/#_

@author: simon_max
"""
from shapely.geometry import Polygon
import json
import numpy as np
import csv
import pandas as pd

code_departement = 75

#On met les infos du cadastre dans un dictionnaire
f= open('cadastre-{}-sections.json'.format(code_departement)) 
cadastre = json.load(f)

#On met les infos du csv qui contient les codes communes dans un dataframe
df_communes = pd.read_csv('laposte_hexasmal.csv', dtype={'Code_commune_INSEE' : 'str', 'Code_postal' : 'str'}, sep = ';')
df_communes = df_communes.reset_index()

#On crée un dictionnaire qui va contenir chaque section avec les coordonnées moyennes des différentes parcelles
dict_sections = {}
for i in range (len(cadastre['features'])):
    coordinates = list(Polygon(cadastre['features'][i]['geometry']['coordinates'][0][0]).centroid.coords)[0] #Fonction qui permet de renvoyer le centre d'une liste de coordonnées / donne le centre de la section cadastrale
    coordinates = list(coordinates)
    ville = df_communes[df_communes['Code_commune_INSEE'] == cadastre['features'][i]['properties']['commune']]['Nom_commune'].values[0]
    code_postal = df_communes[df_communes['Nom_commune']==str(ville)]['Code_postal'].values[0]
    section = str(code_postal) + "_" + str(cadastre['features'][i]['properties']['code'])
    if section in dict_sections.keys():
        dict_sections[section][3].append(coordinates)
    else:
        dict_sections[section] = ['France', ville, code_postal, coordinates] 

#On transforme notre dictionnaire en un dataframe facilement exportable
df_sections = pd.DataFrame.from_dict(dict_sections, orient = 'index')
df_sections = df_sections.reset_index()
df_sections.set_axis(['section','pays','ville','code_postal', 'coordonnees'], axis=1, inplace=True)
df_sections['ville'] = np.where(df_sections['ville'].str.slice(0,5) == "PARIS", "Paris", df_sections['ville'])


df_sections['longitude'] = df_sections['coordonnees'].map(lambda x: x[0])
df_sections['latitude'] = df_sections['coordonnees'].map(lambda x: x[1])
df_sections = df_sections.drop(columns = ['coordonnees'])

df_sections.to_csv('cadastre_{}.csv'.format(code_departement), index=False)
df_sections.to_excel('cadastre_{}.xlsx'.format(code_departement), index=False, encoding='utf8')
