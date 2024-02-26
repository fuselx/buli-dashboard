# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
st.set_page_config(layout="centered")


# Höhe der Sidebar-Liste anpassen
st.sidebar.markdown("""
                    <style> [data-testid='stSidebarNav'] > ul { min-height: 60vh; } </style> 
                    """, unsafe_allow_html=True)


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
    md['Zuschauer'] = md['Zuschauer'].astype('int')
    md = md.replace(0, "")
    md = md.drop(['Venue','Match Report','Notes'],axis = 1)
    return md

# Spieltage
md = matchdays()

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


#%%
# Liste, um Tabelle für Spieltage zu sammeln
list_Tabellen_md = []
# Einen DF pro Spieltag erstellen
# Aktuellen Spieltag ermitteln
mdSubset = md[md['Ergebnis'] != "-:-" ]

bis = max(mdSubset["Spieltag"])+1
for matchday in range(1, bis):  
    Tabellen_md = Tabelle_md(md, md = matchday)
    list_Tabellen_md.append(Tabellen_md)

# Alle zu einem df vereinen, was späteres Handling erleichtert
Tabellen_md = pd.concat(list_Tabellen_md,ignore_index=True).sort_values(by=['Team','Spieltag'])

#%% Graph für Saisonverlauf erstellen erstellen (Platzierung, fixe y-Range)
def season_rank():
    Vereinsfarben = ["#FBC910","#e30511", "black","#009d3b","#1e5cb3","#149c33","#006eb8","#014e9f","#00579c","#e30511","#004c94",
                     "#0169b9","#aa1025","#562b86","#1962b9","#014b9d","#614837","#b88748"] #alphabetische Reihenfole der Teams
    fig = px.line(Tabellen_md,
                  x = "Spieltag",
                  y="Platz",
                  color="Team",
                  markers = True,
                  range_y=(18.5,0.5),
                  range_x=(0.5,34.5),
                  line_shape="linear",
                  color_discrete_sequence=Vereinsfarben,
                  height=500)
    fig.update_layout(plot_bgcolor = "white")
    fig.update_yaxes(gridcolor = "#cdd1cf",tick0=18,dtick=1)
    fig.update_xaxes(minor=dict(ticklen=4, tickcolor="#cdd1cf", showgrid=False),title_text='')
    return fig

#%% Graph für Saisonverlauf erstellen (allgemein) 
def season(var):
    Vereinsfarben = ["#FBC910","#e30511", "black","#009d3b","#1e5cb3","#149c33","#006eb8","#014e9f","#00579c","#e30511","#004c94",
                     "#0169b9","#aa1025","#562b86","#1962b9","#014b9d","#614837","#b88748"] #alphabetische Reihenfole der Teams
    fig = px.line(Tabellen_md,
                  x = "Spieltag",
                  y=var,
                  color="Team",
                  markers = True,
                  range_y=(1.2*min(Tabellen_md[var])-0.2,1.2*max(Tabellen_md[var])),
                  range_x=(0.5,34.5),
                  line_shape="linear",
                  color_discrete_sequence=Vereinsfarben,
                  height=500)
    fig.update_layout(plot_bgcolor = "white")
    fig.update_yaxes(gridcolor = "#cdd1cf",tick0=0,dtick=1)
    fig.update_xaxes(minor=dict(ticklen=4, tickcolor="#cdd1cf", showgrid=False),title_text='')
    return fig
#%% Dashboard Seite
st.subheader("Saisonverlauf",divider = "rainbow")
st.markdown("""
            Wähle aus den Statistiken. Doppelklick auf ein Team zeigt nur den Saisonverlauf des angewählten Teams. Durch einzelne Klicks
            kannst du Teams an- oder abwählen. Durch Auswählen eines Bereiches kannst du in den Graph reinzoomen.
            """)
option = st.selectbox("",options=["Platzierung",
                                  "Punkte",
                                  "Tordifferenz",
                                  "Tore",
                                  "Gegentore"
                                  ])
if option == "Platzierung":
    st.plotly_chart(season_rank(),use_container_width = True)
elif option == "Punkte":
    st.plotly_chart(season("Punkte"),use_container_width = True)
elif option == "Tore":
    st.plotly_chart(season("Tore"),use_container_width = True)
elif option == "Gegentore":
    st.plotly_chart(season("Gegentore"),use_container_width = True)
elif option == "Tordifferenz":
    st.plotly_chart(season("Tordifferenz"),use_container_width = True)
