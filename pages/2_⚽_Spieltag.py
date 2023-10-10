# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import requests
import io
from PIL import Image
st.set_page_config(layout="wide")
# Session State für Smartphone-Version
st.session_state.mobile_on = st.session_state.mobile_on
# Sidebar-Notiz
st.sidebar.success("Wähle aus der Liste oben den Punkt aus, den Du Dir anschauen möchtest!")
# Toggle für Smartphone-Version (wird durch Session State für alle Seiten übernommen)
mobile_on = st.sidebar.toggle("Smartphone-Version", key = "mobile_on")



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
#%% Dataframes formatieren
# Kleiner md-Datensatz für Handy-Version
md_small = md[["Spieltag","Tag","Datum","Anstoß","Heimlogo","Ergebnis","Auswärtslogo"]]
md_small['Datum'] =  pd.to_datetime(md_small['Datum']).dt.strftime('%d.%m.%y')
md_small_style = [{'selector':'tbody',
                   'props':[('font-size',"13px"),('color','black')]},
                  {'selector':'td:nth-child(7)',
                   'props':[('font-weight','bold'),("text-align","center")]},
                  {'selector':'td:nth-child(2)',
                   'props':[('display','none')]},
                  {'selector':'td:nth-child(2)',
                   'props':[('border-left','1px solid white')]},
                  {'selector':'td:nth-child(3)',
                   'props':[('border-right','1px solid white'),('border-left','1px solid white')]},
                  {'selector':'td:nth-child(4)',
                   'props':[('border-right','1px solid white')]},
                  {'selector':'td:nth-child(6)',
                   'props':[('border-right','1px solid white')]},
                  {'selector':'td:nth-child(7)',
                   'props':[('border-right','1px solid white')]},
                  {'selector':'td:nth-child(8)',
                   'props':[('border-right','1px solid white')]},
                  {'selector':'tr:nth-child(1)',
                   'props':[('border-top','2px solid white')]},
                  {'selector':'tr:last-child',
                   'props':[('border-bottom','2px solid white')]},
                  {'selector':'tr:nth-child(2)',
                   'props':[('border-bottom','2px solid gray')]},
                  {'selector':'tr:nth-child(6)',
                   'props':[('border-bottom','2px solid gray')]},
                  {'selector':'th',
                  'props':[('display','none')]},
                  {'selector':'td:nth-child(9)',
                  'props':[('display','none')]},
                  {'selector':'td:nth-child(10)',
                  'props':[('display','none')]},
                  {'selector':'tr:nth-child(odd)',
                   'props':[('background-color','#e7f7e1')]},
                  {'selector':'tr:nth-child(odd) td',
                   'props':[('border-right','1px solid #e7f7e1')]},
                  {'selector':'tr:nth-child(even) td',
                   'props':[('border-right','1px solid white')]},]
md_spielplan_small = md[["Spieltag","Tag","Datum","Anstoß","Heimlogo","Ergebnis","Auswärtslogo","Heim","Auswärts"]]
md_spielplan_small['Datum'] =  pd.to_datetime(md_spielplan_small['Datum']).dt.strftime('%d.%m.%y')

# Converting links to html tags
def path_to_image_html(path):
    return '<img src="' + path + '" width="30" >'

#convert df to html

def convert_df(input_df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return input_df.to_html(escape=False, formatters=dict(Heimlogo=path_to_image_html,Auswärtslogo=path_to_image_html))

#%% Dashboard
col1,col2,col3 = st.columns((1,3,1))
with col2:
    st.subheader("Spieltage",divider = "rainbow")
    Start_index = len(mdSubset[(mdSubset["Heim"] == "Hannover 96")|(mdSubset["Auswärts"] == "Hannover 96")]) # aktuelle Anzahl von Spielen
    if mobile_on:
       Spieltag = st.slider("",min_value=1,max_value=34,value=Start_index)
       md_small_html =  convert_df(md_small[md_small["Spieltag"] == Spieltag]) 
       css_string = ''
       for rule in md_small_style:
           selector = rule['selector']
           props = '; '.join([f'{prop[0]}: {prop[1]}' for prop in rule['props']])
           css_string += f'{selector} {{{props}}}\n'
       md_small_html_styled =  f'<style>{css_string}</style>{md_small_html}'  
       st.markdown(
           md_small_html_styled,
           unsafe_allow_html=True
       )         
    else:
                Spieltag = st.selectbox("",options = range(1,35),index=Start_index-1)
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
