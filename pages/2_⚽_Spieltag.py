# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import requests
import io
from PIL import Image
st.set_page_config(layout="wide")


# Höhe der Sidebar-Liste anpassen
st.sidebar.markdown("""
                    <style> [data-testid='stSidebarNav'] > ul { min-height: 60vh; } </style> 
                    """, unsafe_allow_html=True)

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
col1,col2,col3 = st.columns((1,7,1))
with col2:
    st.subheader("Spieltage",divider = "rainbow")
    Start_index = len(mdSubset[(mdSubset["Heim"] == "Hannover 96")|(mdSubset["Auswärts"] == "Hannover 96")]) # aktuelle Anzahl von Spielen
    
    
    buttonDown,buttonUp,Space = st.columns((1,1,13))
    with buttonDown:
        if st.button("⏪"):
            st.session_state['select'] -= 1
    with buttonUp:
        if st.button("⏩"):
            st.session_state['select'] += 1
    Spieltag = st.selectbox("",options = range(1,35),index=Start_index-1,key="select",label_visibility="collapsed")
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
