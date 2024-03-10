# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import numpy as np
import requests
import io
from PIL import Image

directory = "https://raw.githubusercontent.com/fuselx/buli-dashboard/main/Logos%20Zweite%20Liga/"

#%% Spieltage einlesen
@st.cache_data(ttl=3600*12)
def matchdays():
    temp = pd.read_html("https://fbref.com/en/comps/33/schedule/2-Bundesliga-Scores-and-Fixtures")
    md = temp[0]
    md = md.dropna(subset=['Wk'])
    md.rename(columns = {
        'Wk':'Spieltag',
        'Day':'Tag',
        'Date':'Datum',
        'Time':'Anstoß',
        'Home':'Heim',
        'Score':'Ergebnis',
        'Away':'Auswärts',
        'Attendance':'Zuschauer',
        'Referee':'Schiedsrichter',
        'xG.1':'xG '},inplace = True)
    new_names = {"Wehen":"Wiesbaden",
                 "Karlsruher":"Karlsruhe",
                 "Paderborn 07":"Paderborn"
        }
    md.loc[:,['Heim','Auswärts']] = md.loc[:,['Heim','Auswärts']].replace(new_names)
    days = {'Fri':'Fr.',
            'Sat':'Sa.',
            'Sun':'So.',
            'Tue':'Di.',
            'Wed':'Mi.',
            'Thu':'Do.'}
    md.loc[:,'Tag'] = md.loc[:,'Tag'].replace(days)
    md['Datum'] = pd.to_datetime(md['Datum']).dt.strftime('%d.%m.%Y')
    md['Spieltag'] = md['Spieltag'].astype('int')
    md['Zuschauer'] = pd.to_numeric(md['Zuschauer'])
    md['Ergebnis'] = md['Ergebnis'].fillna("-:-")
    md['Anstoß'] = md['Anstoß'].fillna("tbd")
    md = md.replace(np.nan, 0)
    md['Schiedsrichter'] = md['Schiedsrichter'].replace(0,"")
    md = md.replace(0,np.nan)
    md['xG'] = md['xG'].replace(np.nan,0)
    md['xG '] = md['xG '].replace(np.nan,0)
    md = md.drop(['Venue','Match Report','Notes'],axis = 1)
    return md

# Spieltage
md = matchdays()
#mdSubset = md[md['Ergebnis'] != "-:-" ]

#%% Bilder laden
@st.cache_data
def images():
    images = {}
    mdImages = pd.DataFrame(md["Heim"].unique())
    for index, row in mdImages.iterrows():
        image_name = row[0] + ".png"  # gesuchter Name des Logos
        image_path = directory + image_name
        response = requests.get(image_path, stream=True)
        img = Image.open(io.BytesIO(response.content)).convert("RGBA")
        images[image_name] = img
    return images

# Bilder laden
images = images()
def table_images():
    # Bilder in die Tabelle laden
    md['Heimlogo'] = None
    md['Auswärtslogo'] = None
    for index, row in md.iterrows():
        imagename_home = row['Heim'] + ".png"
        imagename_away = row['Auswärts'] + ".png"
        md.loc[index,'Heimlogo'] = directory + imagename_home
        md.loc[index,'Auswärtslogo'] = directory + imagename_away   
    return md

#%% Selbstgemachte Tabelle nach Spieltagen
def Tabelle_md(df,md = 34):
    
    df_copy = df[df.loc[:,'Spieltag'] <= md]  
    all_teams = set(df_copy['Heim'].unique()).union(set(df_copy['Auswärts'].unique()))
    spiele = []
    for team in all_teams:
        mp = df_copy[(df_copy['Heim'] == team) | (df_copy['Auswärts'] == team)]['Ergebnis'].count()
        spiele.append(mp)
    
    
    # aus dem string 'Ergebnis' die Variablen ToreHeim und ToreAuswärts generieren
    df_copy.loc[:,'ToreHeim']=df_copy.loc[:,'Ergebnis'].str[0]
    df_copy.loc[:,'ToreHeim'] = pd.to_numeric(df_copy['ToreHeim'],errors="coerce")
    df_copy.loc[:,'ToreAuswärts']=df_copy.loc[:,'Ergebnis'].str[2]
    df_copy.loc[:,'ToreAuswärts'] = pd.to_numeric(df_copy['ToreAuswärts'],errors="coerce")
    
    # Auf der Basis PunkteHeim und PunkteAuswärts generieren
    df_copy['PunkteHeim'] = np.where(df_copy['ToreHeim'] == df_copy['ToreAuswärts'], 1, np.where(df_copy['ToreHeim'] > df_copy['ToreAuswärts'], 3, 0))
    df_copy['PunkteAuswärts'] = np.where(df_copy['ToreHeim'] == df_copy['ToreAuswärts'], 1, np.where(df_copy['ToreHeim'] < df_copy['ToreAuswärts'], 3, 0))
    
    # Und so eine Summe für jedes Team für Punkte und Tore berechnen 
    punkte = []
    for team in all_teams:
        points = sum(df_copy[df_copy['Heim'] == team]['PunkteHeim'])+sum(df_copy[df_copy['Auswärts'] == team]['PunkteAuswärts'])
        punkte.append(points)
        
    tordifferenz = []
    tore = []
    gegentore = []  
    
    for team in all_teams:
        Heimtore = df_copy[df_copy['Heim'] == team]['ToreHeim'].fillna(0).sum()
        Heimgegentore = df_copy[df_copy['Heim'] == team]['ToreAuswärts'].fillna(0).sum()
        
        Auswärtstore = df_copy[df_copy['Auswärts'] == team]['ToreAuswärts'].fillna(0).sum()
        Auswärtsgegentore = df_copy[df_copy['Auswärts'] == team]['ToreHeim'].fillna(0).sum()
        
        goals = Heimtore + Auswärtstore
        goals = goals.astype('int')
        tore.append(goals)
        goalsag = Heimgegentore + Auswärtsgegentore
        goalsag = goalsag.astype('int')
        gegentore.append(goalsag)
        goaldif = Heimtore + Auswärtstore - Heimgegentore - Auswärtsgegentore
        goaldif = goaldif.astype('int')
        tordifferenz.append(goaldif)
        
    
    # Jetzt die Teams aus df herausfinden. Dafür reichen einfach die unique values in df['Heim']
    # Dazu werden Punkte und Tordifferenz gegebeben und richtig sortiert.
    Tabelle_md = pd.DataFrame({'Team':list(all_teams),
                            'Spieltag':mp,
                            'Tore':tore,
                            'Gegentore':gegentore,
                            'Tordifferenz':tordifferenz,
                            'Punkte':punkte}).sort_values(by=['Punkte','Tordifferenz'],ascending=False)
    Tabelle_md.loc[:,"Platz"] = range(1,19)
    return Tabelle_md

