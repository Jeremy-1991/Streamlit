# -*- coding: utf-8 -*-
"""my_streamlit_app.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eRrUr_gdu44wpCQSr169B14fgyn5WZ4H
"""

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

link = "https://raw.githubusercontent.com/murpi/wilddata/master/quests/cars.csv"
df_cars = pd.read_csv(link)

st.title("Analyse dataset voitures")

st.write("Utilisation d'une base de données sur l'automobile comparant les véhicules des US, de l'Europe et du Japon.")
st.write("\n")

st.write("Veuillez sélectionner un ou plusieurs pays.")
option_US = st.checkbox("US")
option_EU = st.checkbox("Europe")
option_JA = st.checkbox("Japon")
st.write("\n")

df_cars_final = pd.DataFrame()
if option_US :
    df_cars_final = pd.concat([df_cars_final, df_cars.loc[df_cars["continent"] == " US."]])
if option_EU :
    df_cars_final = pd.concat([df_cars_final, df_cars.loc[df_cars["continent"] == " Europe."]])
if option_JA :
    df_cars_final = pd.concat([df_cars_final, df_cars.loc[df_cars["continent"] == " Japan."]])
if df_cars_final.empty :
    df_cars_final = df_cars

st.write("Dataframe obtenue.")
df_cars_final
st.write("\n")

def summarize(df) :

# 1) Calcul statistiques de base grâce à .describe()
    df_final = df.describe(include='all').T

# 2) Affichage des valeurs nulles sur une colonne.
    df_final['NAN'] = df.apply(lambda x: 'OUI' if pd.isna(x).any() else 'NON')

# 3) Calcul % de valeurs nulles : application d'un lambda pour calculer le pourcentage.
    df_final['% NAN'] = df.apply(lambda x : (x.isna().sum() / len(x))*100)

# 4) Affichage des valeurs en doublons sur une colonne.
    df_final['Duplicated'] = df.apply(lambda x: 'OUI' if x.duplicated().any() else 'NON')

# 5) Calcul % de valeurs en doublons : application d'un lambda pour calculer le pourcentage.
    df_final['% Duplicated'] = df.apply(lambda x : (x.duplicated().sum() / len(x))*100)

# 6) Calcul nombre de valeurs uniques : application d'un lambda pour calculer le nombre de valeurs uniques.
    df_final['Uniques'] = df.apply(lambda x : len(x.unique()))

# 7) Création de la heatmap.
    st.write("Heatmap de corrélation.")
    viz_correlation = sns.heatmap(df.select_dtypes(include=['number']).corr(), cmap="coolwarm", center=0)
    st.pyplot(viz_correlation.figure)
    st.write("\n")

# 8) Affichage des boxplots de toutes les valeurs numériques.
    # On commence par récupérer les colonnes avec des valeurs numériques (int, float)
    st.write("Boxplots pour chaque donnée.")
    col_num = df.select_dtypes(include=['int', 'float'])

    # On crée une boucle qui crée un graphique global contenant un sous-graphique de type boxplot pour chaque colonne numérique.
    plt.figure(figsize=(8, 10))

    for i, colonne in enumerate(col_num, 1):
        plt.subplot(len(df.columns), 1, i)
        viz_correlation3 = sns.boxplot(x=df[colonne])
        plt.title(colonne)

    plt.tight_layout()
    st.pyplot(viz_correlation3.figure)
    st.write("\n")

# 9) Affichage des cellules en rouge.
    df_final = df_final.style.apply(lambda column : ['background : red' if value > 0 else '' for value in column], subset=['% NAN', '% Duplicated'])
    st.write("Ensemble des statistiques pour chaque donnée.")
    df_final

    return df_final

summarize(df_cars_final)