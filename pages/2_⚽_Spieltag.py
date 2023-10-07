# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import requests
import io
from PIL import Image

st.set_page_config(
    page_title="Spieltage",
    page_icon="⌚",
    layout="wide"
)

st.sidebar.success("Wähle aus der Liste oben den Punkt aus, den Du Dir anschauen möchtest!")


directory = "https://raw.githubusercontent.com/fuselwolga/buli-dashboard/main/Logos%20Zweite%20Liga/"
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
  
#%% Dataframes formatieren
# Kleiner md-Datensatz für Handy-Version
md_small = md[["Spieltag","Tag","Anstoß","Heim","Ergebnis","Auswärts"]]
Abkürzungen = {"Paderborn":"SCP",
               "Schalke 04":"S04",
               "Hamburger SV":"HSV",
               "Düsseldorf":"F95",
               "Hansa Rostock":"FCH",
               "Braunschweig":"EBS",
               "Hannover 96":"H96",
               "Wiesbaden":"WIE",
               "Karlsruhe":"KSC",
               "Holstein Kiel":"KSV",
               "Hertha BSC":"BSC",
               "St. Pauli":"STP",
               "Elversberg":"ELV",
               "Greuther Fürth":"SGF",
               "Nürnberg":"FCN",
               "Magdeburg":"FCM",
               "Osnabrück":"OSN",
               "Kaiserslautern":"FCK"}
md_small.loc[:,'Heim'] = md_small.loc[:,'Heim'].replace(Abkürzungen)
md_small.loc[:,'Auswärts'] = md_small.loc[:,'Auswärts'].replace(Abkürzungen)
md_small_style = [{'selector':'tbody',
                   'props':[('font-size',"14px")]},
                  {'selector':'td:nth-child(6)',
                   'props':[('font-weight','bold'),("text-align","center")]},
                  {'selector':'td:nth-child(4)',
                   'props':[('background-color','#f7f7f7'),('border-right','2px solid #f7f7f7')]},
                  {'selector':'td:nth-child(3)',
                   'props':[('background-color','#f7f7f7'),('border-right','2px solid #f7f7f7')]},
                  {'selector':'tbody tr td',
                   'props':[('color','black'),('border-left','2px solid white'),('border-right','2px solid white')]},
                  {'selector':'th',
                  'props':[('display','none')]},
                  {'selector':'td:nth-child(2)',
                  'props':[('display','none')]},
                  {'selector':'td:nth-child(4)',
                  'props':[('border-right','2px solid black')]}]
md_spielplan_small = md[["Spieltag","Datum","Tag","Anstoß","Heim","Ergebnis","Auswärts"]]
md_spielplan_small['Heim'] = md_spielplan_small['Heim'].replace(Abkürzungen)
md_spielplan_small['Auswärts'] = md_spielplan_small['Auswärts'].replace(Abkürzungen)
md_spielplan_small['Datum'] =  pd.to_datetime(md_spielplan_small['Datum']).dt.strftime('%d.%m.%y')
md_spielplan_small_style = [{'selector':'tbody',
                   'props':[('font-size',"14px")]},
                  {'selector':'td:nth-child(7)',
                   'props':[('font-weight','bold'),("text-align","center")]},
                  {'selector':'td:nth-child(4)',
                   'props':[('font-style','italic')]},
                  {'selector':'td:nth-child(3)',
                   'props':[('font-style','italic')]},
                  {'selector':'td:nth-child(5)',
                   'props':[('font-style','italic')]},
                  {'selector':'tbody tr td',
                   'props':[('color','black'),('border-left','2px solid white'),('border-right','2px solid white')]},
                  {'selector':'th',
                  'props':[('display','none')]},
                  {'selector':'td:nth-child(5)',
                  'props':[('border-right','2px solid black')]}]
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

# Bilder in die Tabelle laden
md['Heimlogo'] = None
md['Auswärtslogo'] = None
for index, row in md.iterrows():
    imagename_home = row['Heim'] + ".png"
    imagename_away = row['Auswärts'] + ".png"
    md.loc[index,'Heimlogo'] = directory + imagename_home
    md.loc[index,'Auswärtslogo'] = directory + imagename_away 
#%% Dashboard
st.subheader("Spieltage",divider = "rainbow")
Start_index = len(mdSubset[(mdSubset["Heim"] == "Hannover 96")|(mdSubset["Auswärts"] == "Hannover 96")]) # aktuelle Anzahl von Spielen
on = st.toggle("Smartphone-Version",key = "md-toogle_mobile")
Spieltag = st.selectbox("",options = range(1,35),index=Start_index-1)
if on:
   st.write(f"__Spieltag {Spieltag}: {md[md['Spieltag'] == Spieltag].reset_index().loc[0,'Datum']} - {md[md['Spieltag'] == Spieltag].reset_index().loc[7,'Datum']}__")
   st.table(md_small[md_small["Spieltag"] == Spieltag].style.set_table_styles(md_small_style))        
else:
#    if Spieltag > Start_index:
#            st.dataframe(md[md["Spieltag"] == Spieltag],
#                         hide_index=True,height = 360,
#                         column_order=("Tag","Datum","Anstoß","Heimlogo","Ergebnis","Auswärtslogo"),
#                         column_config={'Heimlogo':st.column_config.ImageColumn('Heim',width = "small"),
#                                        'Auswärtslogo':st.column_config.ImageColumn('Auswärts',width = "small")})
#    else:
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
st.divider()
st.subheader("Spielpläne einzelner Teams")
if on:
    team = st.selectbox("Wähle das Team, dessen Spieplan du dir anschauen möchtest",options = md_spielplan_small["Heim"].unique(),index = 1)
    st.table(md_spielplan_small[(md_spielplan_small['Heim'] == team)|(md_spielplan_small["Auswärts"] == team)].style.set_table_styles(md_spielplan_small_style)) 
else:  
    team = st.selectbox("Wähle das Team, dessen Spieplan du dir anschauen möchtest",options = md["Heim"].unique(),index = 1)     
    st.dataframe(md[(md['Heim'] == team)|(md["Auswärts"] == team)],
                     hide_index=True,
                     height = 1240,
                     column_order=("Spieltag","Tag","Datum","Anstoß","xG","Heimlogo","Ergebnis","Auswärtslogo","xG ","Zuschauer","Schiedsrichter"),
                     column_config={'Heimlogo':st.column_config.ImageColumn('Heim',width = "small"),
                                    'Auswärtslogo':st.column_config.ImageColumn('Auswärts',width = "small"),
                                    'xG':st.column_config.ProgressColumn(
                                        min_value=0,
                                        max_value=3.5,
                                        format = "  %f",
                                        width = "small"),
                                    'xG ':st.column_config.ProgressColumn(
                                        min_value=0,
                                        max_value=3.5,
                                        format = "  %f",
                                        width = "small")                                            
                                 })
