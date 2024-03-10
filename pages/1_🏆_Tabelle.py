# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

from pages.prep import data_matchdays
from pages.prep import data_table


pd.options.mode.chained_assignment = None  # default='warn'

# Höhe der Sidebar-Liste anpassen
st.sidebar.markdown("""
                    <style> [data-testid='stSidebarNav'] > ul { min-height: 60vh; } </style> 
                    """, unsafe_allow_html=True)



#%% Tabelle einlesen und bearbeiten
# Team-Stastistiken und Tabelle
df = data_table.load_data()
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


#%% Styles
Tabelle_style = [{'selector':'table tr th:nth-child(1)',
                   'props':[("display","none")]},
                 {'selector':'th',
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

#### Spieltage
md = data_matchdays.table_images()
mdSubset = md[md['Ergebnis'] != "-:-" ]

# Converting links to html tags
def path_to_image_html(path):
    return '<img src="' + path + '" width="32" >'

#convert df to html

def convert_df(input_df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return input_df.to_html(escape=False, formatters=dict(Heimlogo=path_to_image_html,Auswärtslogo=path_to_image_html))







#%% Dashboard
st.subheader("Spieltag und Tabelle")
col1,col2 = st.columns((6,5))
with col1:

    Start_index = len(mdSubset[(mdSubset["Heim"] == "Hannover 96")|(mdSubset["Auswärts"] == "Hannover 96")]) # aktuelle Anzahl von Spielen
    Spieltag = st.selectbox(label = "leer",options = range(1,35),index=Start_index-1,key="select",label_visibility="collapsed")
    st.dataframe(md[md["Spieltag"] == Spieltag],
                    hide_index=True,
                    height = 360,
                    column_order=("Tag","Datum","Anstoß","xG","Heimlogo","Ergebnis","Auswärtslogo","xG ","Zuschauer","Schiedsrichter"),
                    column_config={'Spieltag':None,
                                'Heimlogo':st.column_config.ImageColumn('Heim',width = "small"),
                                'Auswärtslogo':st.column_config.ImageColumn('Auswärts',width = "small"),
                                'xG':st.column_config.ProgressColumn(
                                    min_value=0,
                                    max_value=3.5,#md[md["Spieltag"] == Spieltag][['xG','xG ']].max().max(),
                                    format = "  %f",
                                    width = "small"),
                                'xG ':st.column_config.ProgressColumn(
                                        min_value=0,
                                        max_value=3.5,#md[md["Spieltag"] == Spieltag][['xG','xG ']].max().max(),
                                        format = "  %f",
                                        width = "small")                                            
                                })
with col2: 
    st.table(Tabelle.style.set_table_styles(Tabelle_style))
