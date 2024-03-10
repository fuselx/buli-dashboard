# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="centered")

from pages.prep import data_matchdays

# Höhe der Sidebar-Liste anpassen
st.sidebar.markdown("""
                    <style> [data-testid='stSidebarNav'] > ul { min-height: 60vh; } </style> 
                    """, unsafe_allow_html=True)



#%% Daten einlesen
# Liste, um Tabelle für Spieltage zu sammeln
list_Tabellen_md = []

# Einen DF pro Spieltag erstellen
# Aktuellen Spieltag ermitteln
md = data_matchdays.matchdays()
mdSubset = md[md['Ergebnis'] != "-:-" ]

bis = max(mdSubset["Spieltag"])+1
for matchday in range(1, bis):  
    Tabellen_md = data_matchdays.Tabelle_md(md, md = matchday)
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
