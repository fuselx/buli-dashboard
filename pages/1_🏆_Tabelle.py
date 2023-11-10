# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
st.set_page_config(layout="centered")
# Session State für Smartphone-Version
st.session_state.mobile_on = st.session_state.mobile_on

# Höhe der Sidebar-Liste anpassen
st.sidebar.markdown("""
                    <style> [data-testid='stSidebarNav'] > ul { min-height: 60vh; } </style> 
                    """, unsafe_allow_html=True)

# Toggle für Smartphone-Version (wird durch Session State für alle Seiten übernommen)
mobile_on = st.sidebar.toggle("Smartphone-Version", key = "mobile_on")

#%% Tabellen einlesen
@st.cache_data(ttl=3600*12)
def load_data():
# Daten von der Website einlesen
    all_tables = pd.read_html("https://fbref.com/en/comps/33/2-Bundesliga-Stats")
    # Erstmal die Tabelle ausgeben lassen
    df = all_tables[0]
    

    # Vereinsnamen anpassen
    new_names = {"Wehen":"Wiesbaden",
                 "Karlsruher":"Karlsruhe",
                 "Paderborn 07":"Paderborn"
        }
    df['Squad'] = df['Squad'].replace(new_names)

    return df
#%% Tabelle bearbeiten
# Team-Stastistiken und Tabelle
df = load_data()
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
if mobile_on:  
    st.table(Tabelle_slim.style.set_table_styles(Tabelle_style))
else:
    st.table(Tabelle.style.set_table_styles(Tabelle_style))
