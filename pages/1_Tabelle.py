# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Tabelle",
    page_icon="🥇"
)

st.sidebar.success("Wähle aus der Liste oben den Punkt aus, den Du Dir anschauen möchtest!")
#%% Tabellen einlesen
@st.cache_data(ttl=3600*12)
def load_data():
# Daten von der Website einlesen
    all_tables = pd.read_html("https://fbref.com/en/comps/33/2-Bundesliga-Stats")
    # Erstmal die Tabelle ausgeben lassen
    df = all_tables[0]
    
    
    shots = all_tables[8] # Tabelle laden
    shots.columns = shots.columns.get_level_values(1)
    new_columns = {col: 'shots.' + col for col in shots.iloc[:,3:]}
    shots.rename(columns=new_columns,inplace = True)
    df = pd.merge(df.drop('xG',axis = 1),shots,on = "Squad")
    
    shotsag = all_tables[9]
    shotsag.columns = shotsag.columns.get_level_values(1)
    new_columns = {col: 'shots.ag.' + col for col in shotsag.iloc[:,3:]}
    shotsag.rename(columns=new_columns,inplace = True)
    shotsag['Squad'] = shotsag['Squad'].str.replace("vs ","")
    df = pd.merge(df,(shotsag.drop(['# Pl','90s'],axis = 1)),on = "Squad")
    
    passing = all_tables[10]
    passing.columns = passing.columns.map('.'.join)
    target = 17
    while any(str(target) in col for col in passing.columns):
        passing.columns = passing.columns.str.replace(str(target),"")
        target += 1
    passing.columns = passing.columns.str.replace("Unnamed: _level_0.","").str.replace("Unnamed: 0_level_0.","")
    new_columns = {col: 'passing.' + col for col in passing.iloc[:,3:]}
    passing.rename(columns=new_columns,inplace = True)
    df = pd.merge(df,(passing.drop(['Unnamed: 1_level_0.# Pl','Unnamed: 2_level_0.90s'],axis = 1)))
    
    passingag = all_tables[11]
    passingag.columns = passingag.columns.map('.'.join)
    target = 17
    while any(str(target) in col for col in passingag.columns):
        passingag.columns = passingag.columns.str.replace(str(target),"")
        target += 1
    passingag.columns = passingag.columns.str.replace("Unnamed: _level_0.","").str.replace("Unnamed: 0_level_0.","")
    new_columns = {col: 'passing.ag.' + col for col in passingag.iloc[:,3:]}
    passingag.rename(columns=new_columns,inplace = True)
    passingag['Squad'] = passingag['Squad'].str.replace("vs ","")
    df = pd.merge(df,(passingag.drop(['Unnamed: 1_level_0.# Pl','Unnamed: 2_level_0.90s'],axis = 1)))
    
    passtypes = all_tables[12]
    passtypes.columns = passtypes.columns.map('.'.join)
    passtypes.columns = passtypes.columns.str.replace("Unnamed: 0_level_0.","").str.replace("Unnamed: 1_level_0.","").str.replace("Unnamed: 2_level_0.","").str.replace("Unnamed: 3_level_0.","")
    new_columns = {col: 'pt.' + col for col in passtypes.iloc[:,4:]}
    passtypes.rename(columns=new_columns,inplace = True)
    df = pd.merge(df,(passtypes.drop(['# Pl',"90s","Att"],axis = 1)))
    
    passtypesag = all_tables[13]
    passtypesag.columns = passtypesag.columns.map('.'.join)
    passtypesag.columns = passtypesag.columns.str.replace("Unnamed: 0_level_0.","").str.replace("Unnamed: 1_level_0.","").str.replace("Unnamed: 2_level_0.","").str.replace("Unnamed: 3_level_0.","")
    new_columns = {col: 'pt.ag.' + col for col in passtypesag.iloc[:,4:]}
    passtypesag.rename(columns=new_columns,inplace = True)
    passtypesag['Squad'] = passtypesag['Squad'].str.replace("vs ","")
    df = pd.merge(df,(passtypesag.drop(['# Pl',"90s","Att"],axis = 1)))
    
    creation = all_tables[14]
    creation.columns = creation.columns.map('.'.join)
    creation.columns = creation.columns.str.replace("Unnamed: 0_level_0.","").str.replace("Unnamed: 1_level_0.","").str.replace("Unnamed: 2_level_0.","")
    new_columns = {col: 'creation.' + col for col in creation.iloc[:,3:]}
    creation.rename(columns=new_columns,inplace = True)
    df = pd.merge(df,(creation.drop(['# Pl',"90s"],axis = 1)))
    
    creationag = all_tables[15]
    creationag.columns = creationag.columns.map('.'.join)
    creationag.columns = creationag.columns.str.replace("Unnamed: 0_level_0.","").str.replace("Unnamed: 1_level_0.","").str.replace("Unnamed: 2_level_0.","")
    new_columns = {col: 'creation.ag.' + col for col in creationag.iloc[:,3:]}
    creationag.rename(columns=new_columns,inplace = True)
    creationag['Squad'] = creationag['Squad'].str.replace("vs ","")
    df = pd.merge(df,(creationag.drop(['# Pl',"90s"],axis = 1)))
    
    defense = all_tables[16]
    defense.columns = defense.columns.map('.'.join)
    target = 15
    while any(str(target) in col for col in defense.columns):
        defense.columns = defense.columns.str.replace(str(target),"")
        target += 1
    defense.columns = defense.columns.str.replace("Unnamed: _level_0.","").str.replace("Unnamed: 0_level_0.","")
    new_columns = {col: 'defense.' + col for col in defense.iloc[:,3:]}
    defense.rename(columns=new_columns,inplace = True)
    df = pd.merge(df,(defense.drop(['Unnamed: 1_level_0.# Pl','Unnamed: 2_level_0.90s'],axis = 1)))
    
    defenseag = all_tables[17]
    defenseag.columns = defenseag.columns.map('.'.join)
    target = 15
    while any(str(target) in col for col in defenseag.columns):
        defenseag.columns = defenseag.columns.str.replace(str(target),"")
        target += 1
    defenseag.columns = defenseag.columns.str.replace("Unnamed: _level_0.","").str.replace("Unnamed: 0_level_0.","")
    new_columns = {col: 'defense.ag.' + col for col in defenseag.iloc[:,3:]}
    defenseag.rename(columns=new_columns,inplace = True)
    defenseag['Squad'] = defenseag['Squad'].str.replace("vs ","")
    df = pd.merge(df,(defenseag.drop(['Unnamed: 1_level_0.# Pl','Unnamed: 2_level_0.90s'],axis = 1)))
    
    poss = all_tables[18]
    poss.columns = poss.columns.map('.'.join)
    poss.columns = poss.columns.str.replace("Unnamed: 0_level_0.","").str.replace("Unnamed: 1_level_0.","").str.replace("Unnamed: 2_level_0.","").str.replace("Unnamed: 3_level_0.","")
    new_columns = {col: 'poss.' + col for col in poss.iloc[:,4:]}
    poss.rename(columns=new_columns,inplace = True)
    df = pd.merge(df,(poss.drop(['# Pl',"90s"],axis = 1)))
    
    possag = all_tables[19]
    possag.columns = possag.columns.map('.'.join)
    possag.columns = possag.columns.str.replace("Unnamed: 0_level_0.","").str.replace("Unnamed: 1_level_0.","").str.replace("Unnamed: 2_level_0.","").str.replace("Unnamed: 3_level_0.","")
    new_columns = {col: 'poss.ag.' + col for col in possag.iloc[:,2:]}
    possag.rename(columns=new_columns,inplace = True)
    possag['Squad'] = possag['Squad'].str.replace("vs ","")
    df = pd.merge(df,(possag.drop(['# Pl',"poss.ag.90s"],axis = 1)))
    
    # Vereinsnamen anpassen
    new_names = {"Wehen":"Wiesbaden",
                 "Karlsruher":"Karlsruhe",
                 "Paderborn 07":"Paderborn"
        }
    df['Squad'] = df['Squad'].replace(new_names)
    df['passing.LongPct'] = (100*df['passing.Long.Att'].div(df['passing.Total.Att'])).round(1)
    return df
#%% Tabelle bearbeiten
# Team-Stastistiken und Tabelle
df = load_data()
df['passing.avgDist'] = df['passing.Total.TotDist'].div(df['passing.Total.Att'])
Tabelle = df[['Rk','Squad','MP','W','D','L','GF','GA','GD','Pts']]
Tabelle.rename(columns = {
    'Rk':'Platz',
    'Squad':'Team',
    'MP':'Spiele',
    'W':'S',
    'D':'U',
    'L':'N',
    'GF':'Tore',
    'GA':'Gegentore',
    'GD':'Tordifferenz',
    'Pts':'Punkte'
    },inplace = True)

Tabelle_slim = Tabelle[['Platz','Team','Spiele','Tordifferenz','Punkte']]
Tabelle_slim.rename(columns = {
    'Platz':'#',
    'Verein':'Team',
    'Spiele':'Sp',
    'Tordifferenz':'TD',
    'Punkte':'Pkt'},inplace = True)
Tabelle_slim.set_index('#', inplace=True)
Tabelle.set_index('Platz', inplace=True)

#%% Styles
Tabelle_style = [{'selector':'th',
                   'props':[("border","2px solid white"),('font-weight','bold')]},
                  {'selector':'tbody tr',
                   'props':[('color','black')]},
                  {'selector':'tbody tr:first-child th',
                   'props':[('background-color','#66e373')]},
                  {'selector':'tbody tr:nth-child(2) th',
                   'props':[('background-color','#66e373')]},
                  {'selector':'tbody tr:nth-child(3) th',
                   'props':[('background-color','#a3f0ab')]},
                  {'selector':'tbody tr:nth-child(16) th',
                   'props':[('background-color','#f5bd73')]},
                  {'selector':'tbody tr:nth-child(17) th',
                   'props':[('background-color','#fc8326')]},
                  {'selector':'tbody tr:nth-child(18) th',
                   'props':[('background-color','#fc8326')]},
                  {'selector':'tbody tr:nth-child(odd)',
                   'props':[('background-color','#f7f7f7')]},
                  {'selector':'tbody tr td',
                   'props':[('color','black'),('border','2px solid white')]}]

#%% Dashboard
st.subheader("Tabelle der 2. Bundesliga",divider = "rainbow")
on = st.toggle("Smartphone-Version")
if on:  
    st.table(Tabelle_slim.style.set_table_styles(Tabelle_style))
else:
    st.table(Tabelle.style.set_table_styles(Tabelle_style))
