# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 10:55:14 2021

@author: simon_max
"""

import pandas as pd
import numpy as np

code_departement = [75]

#On met les infos du csv dans un dataframe
df = pd.read_csv('full-2020.csv')

#On supprimme des colonnes inutiles
df = df.drop(columns = ["ancien_code_commune","ancien_nom_commune","ancien_id_parcelle", 
                        "numero_volume","lot1_numero","lot1_surface_carrez","lot2_numero",
                        "lot2_surface_carrez","lot3_numero","lot3_surface_carrez",
                        "lot4_numero","lot4_surface_carrez","lot5_numero",
                        "lot5_surface_carrez"])

#On supprime les lignes pour lesquelles il manque des informations essentielles
df = df.dropna(subset=['valeur_fonciere', 'nombre_pieces_principales', 'code_postal'])
#On filtre sur la zone géographique qui nous intéresse
df = df.loc[df["code_departement"].isin (code_departement)]
#On enlève les locaux commerciaux et les dépendances
df = df.loc[df["type_local"].isin (['Appartement','Maison'])]
#On enlève les biens spéciaux
df = df.loc[df["code_nature_culture"].isnull()]
#On supprime les lignes qui ont un même id_mutation - difficile de bien récuperer la surface et le prix associé sinon
df.drop_duplicates(subset ="id_mutation",keep = False, inplace = True)

#On enlève le ".0" qui s'est mis sur certains codes - qui ont été interprétés à tord comme des nombres
df["code_postal"] = df["code_postal"].astype(str)
df["code_postal"] = np.where(df["code_postal"].str.slice(-2,) == ".0", df["code_postal"].str.slice(0,-2).astype(int), df["code_postal"])

df["code_type_local"] = df["code_type_local"].astype(str)
df["code_type_local"] = np.where(df["code_type_local"].str.slice(-2,) == ".0", df["code_type_local"].str.slice(0,-2).astype(int), df["code_type_local"])

df["nombre_pieces_principales"] = df["nombre_pieces_principales"].astype(str)
df["nombre_pieces_principales"] = np.where(df["nombre_pieces_principales"].str.slice(-2,) == ".0", df["nombre_pieces_principales"].str.slice(0,-2).astype(int), df["nombre_pieces_principales"])

df["adresse_numero"] = df["adresse_numero"].astype(str)
df["adresse_numero"] = np.where(df["adresse_numero"].str.slice(-2,) == ".0", df["adresse_numero"].str.slice(0,-2).astype(int), df["adresse_numero"])

# On remplace les Paris 8ème arrondiseement etc par Paris - sinon Tableau ne reconnait pas la ville
df['nom_commune'] = np.where(df['nom_commune'].str.slice(0,5) == "Paris", "Paris", df['nom_commune'])

#on ajoute un nouveau champ calculé - prix au m2
df["prix_au_m2"] = df["valeur_fonciere"]/df["surface_reelle_bati"]

#on ajoute un nouveau champ calculé - code de la section cadastrale
df["section_cadastrale"] = df["code_postal"].astype(str) + "_" + df["id_parcelle"].str.slice(8,10)

#On retire les valeurs abberrantes
#On commence par les stats
stat = {}
for code_postal in list(set(df["code_postal"])) :
    stat[code_postal] = []
    q1 = round(df[df["code_postal"] == code_postal]["prix_au_m2"].quantile(0.25),2)
    q3 = round(df[df["code_postal"] == code_postal]["prix_au_m2"].quantile(0.75),2)
    iqr = q3 - q1
    stat[code_postal].append(q1 - 1.5 * iqr)
    stat[code_postal].append(q3 + 1.5 * iqr)

#On crée une fonction pour identifer les outliers à partir des stats
def is_outlier(row):
    code_postal = row["code_postal"]
    lower_limit = stat[code_postal][0]
    upper_limit = stat[code_postal][1]
    if row["prix_au_m2"] < lower_limit or row["prix_au_m2"] > upper_limit :
        return True
    else:
        return False

#apply the function to the original df:
df.loc[:, 'outlier'] = df.apply(is_outlier, axis = 1)
#filter to only non-outliers:
df_no_outliers = df[~(df["outlier"])]


# On exporte notre nouvelle table
df_no_outliers.to_csv("short-2020.csv", index=False, encoding='utf8')
df_no_outliers.to_excel("short-2020.xlsx", index=False, encoding='utf8')



