# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import requests
import io
from PIL import Image
st.set_page_config(layout="wide")

pd.options.mode.chained_assignment = None  # default='warn'

# Höhe der Sidebar-Liste anpassen
st.sidebar.markdown("""
                    <style> [data-testid='stSidebarNav'] > ul { min-height: 60vh; } </style> 
                    """, unsafe_allow_html=True)


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
mdSubset = md[md['Ergebnis'] != "-:-" ]

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

md = table_images()


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
