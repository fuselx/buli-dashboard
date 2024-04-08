# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="centered")

from pages.prep import data_stats


# Höhe der Sidebar-Liste anpassen
st.sidebar.markdown("""
                    <style> [data-testid='stSidebarNav'] > ul { min-height: 60vh; } </style> 
                    """, unsafe_allow_html=True)
#%% Tabellen einlesen
df = data_stats.load_data()

#%% Import der Bilder, als Objekt speichern
images = data_stats.images()

#%% Radar-Chart Offensive
@st.cache_data
def radar_off(df,team):
    """
    Funktion, um Radar-Charts für jede Mannschaft zu erstellen

    ----------
    df : Datensatz
    team : Der Verein, für den der Plot erstellt werden soll (needs "")

    """
    variables = ['shots.npxG/Sh',
                 'poss.Touches.Att 3rd.pergame',
                 'shots.Gls',
                 'shots.Sh/90',
                 'Poss',
                 'passing.PrgP/90',
                 'creation.SCA Types.PassDead',
                 'poss.Take-Ons.Succ']
    variables.append("Squad")
    df_subset = df[variables]

    # Variablen umbenennen
    df_subset.rename(columns = {
        "shots.npxG/Sh":"xGoals pro Schuss",
        "poss.Touches.Att 3rd.pergame":"Ballkontakte im letzten Drittel pro Spiel",
        "shots.Gls":"Tore",
        "shots.Sh/90":"Schüsse pro Spiel",
        "Poss":"Ballbesitz (%)",
        "passing.PrgP/90":"Progressive Pässe pro Spiel",
        "creation.SCA Types.PassDead":"Chancen nach Offensivstandards",
        "poss.Take-Ons.Succ":"Erfolgreiche Dribblings"
    },inplace = True)

    # Dieses subset ins long_format
    df_long = pd.melt(df_subset,id_vars=["Squad"])
    df_long["maxvalue"] = df_long.groupby(["variable"])['value'].transform("max")
    df_long["minvalue"] = df_long.groupby(["variable"])['value'].transform("min")
    df_long["average"] = df_long.groupby(["variable"])['value'].transform("mean")
    df_long["normal"] = (df_long['value'] - df_long['minvalue']) / (df_long['maxvalue'] - df_long['minvalue'])
    df_long["normalavg"] = df_long.groupby(["variable"])["normal"].transform("mean")
    df_long["value"] = df_long["value"].round(0).astype(int)
    df_long["Beschriftung"] = df_long["variable"].astype(str) + ": " + df_long["value"].astype(str)

    df_long = df_long[df_long["Squad"] == team]
    df_long.reset_index(drop = True,inplace = True)

    # Plot
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r = df_long["normal"],
        theta=df_long["Beschriftung"],
        fill = 'toself',
        name = df_long.loc[0,"Squad"],
        fillcolor= "green"
    ))
    fig.add_trace(go.Scatterpolar(
        r = df_long["normalavg"],
        theta=df_long["Beschriftung"],
        fill = 'toself',
        name = "Durchschnitt",
        fillcolor= "gray"
    ))
    fig.update_traces(opacity=0.4,  # Set fill opacity
                    line=dict(width=0),  # Set line opacity
                    mode = 'lines')    
    fig.update_polars(bgcolor='white',
                        gridshape = "linear",
                        hole = 0,
                        angularaxis = dict(
                            gridcolor= "gray",
                            griddash = "dot",
                            linecolor = "black",
                            linewidth = 0.5,
                            ticks = ""),
                        radialaxis = dict(
                            color = "white",
                            gridwidth = 0.1,
                            dtick = 0.25,
                            linecolor = "white",
                            showline = False,
                            ticks = ""
                            ))                 
    fig.update_layout(template = "none",
                        showlegend=False,
                        dragmode = False,
                        clickmode = "none",
                        font = dict(size = 12,color = "black",family = "arial"),
                        title = "",
                        title_font_size=35,
                        title_x=0,
                        title_font_color = "black",
                        polar = dict(radialaxis = dict(showticklabels = False,range=[-0.05,1.05])))

    return fig
#%%
@st.cache_data
def radar_pass(df,team):
    """
    Funktion, um Radar-Charts für jede Mannschaft zu erstellen

    ----------
    df : Datensatz
    team : Der Verein, für den der Plot erstellt werden soll (needs "")

    """
    variables = ['passing.Total.pergame',
                'passing.Total.Cmp%',
                'passing.PrgP.pergame',
                'passing.LongPct',
                'pt.Pass Types.TB',
                'Poss',
                'pt.Pass Types.Sw.pergame',
                'pt.Pass Types.Crs.pergame']
    variables.append("Squad")
    df_subset = df[variables]

    # Variablen umbenennen
    df_subset.rename(columns = {
        "passing.Total.pergame":"Pässe pro Spiel",
        "passing.Total.Cmp%":"Passquote",
        "passing.PrgP.pergame":"Progressive Pässe pro Spiel",
        "passing.LongPct":"Prozent Lange Bälle",
        "Poss":"Ballbesitz (%)",
        "pt.Pass Types.TB":"Through Balls",
        "pt.Pass Types.Sw.pergame":"Flankenwechsel pro Spiel",
        "pt.Pass Types.Crs.pergame":"Flanken pro Spiel"
    },inplace = True)

    # Dieses subset ins long_format
    df_long = pd.melt(df_subset,id_vars=["Squad"])
    df_long["maxvalue"] = df_long.groupby(["variable"])['value'].transform("max")
    df_long["minvalue"] = df_long.groupby(["variable"])['value'].transform("min")
    df_long["average"] = df_long.groupby(["variable"])['value'].transform("mean")
    df_long["normal"] = (df_long['value'] - df_long['minvalue']) / (df_long['maxvalue'] - df_long['minvalue'])
    df_long["normalavg"] = df_long.groupby(["variable"])["normal"].transform("mean")
    df_long["value"] = df_long["value"].round(0).astype(int)
    df_long["Beschriftung"] = df_long["variable"].astype(str) + ": " + df_long["value"].astype(str)

    df_long = df_long[df_long["Squad"] == team]
    df_long.reset_index(drop = True,inplace = True)

    # Plot
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r = df_long["normal"],
        theta=df_long["Beschriftung"],
        fill = 'toself',
        name = df_long.loc[0,"Squad"],
        fillcolor= "green"
    ))
    fig.add_trace(go.Scatterpolar(
        r = df_long["normalavg"],
        theta=df_long["Beschriftung"],
        fill = 'toself',
        name = "Durchschnitt",
        fillcolor= "gray"
    ))
    fig.update_traces(opacity=0.4,  # Set fill opacity
                    line=dict(width=0),  # Set line opacity
                    mode = 'lines')    
    fig.update_polars(bgcolor='white',
                        gridshape = "linear",
                        hole = 0,
                        angularaxis = dict(
                            gridcolor= "gray",
                            griddash = "dot",
                            linecolor = "black",
                            linewidth = 0.5,
                            ticks = ""),
                        radialaxis = dict(
                            color = "white",
                            gridwidth = 0.1,
                            dtick = 0.25,
                            linecolor = "white",
                            showline = False,
                            ticks = ""
                            ))                 
    fig.update_layout(template = "none",
                        showlegend=False,
                        dragmode = False,
                        clickmode = "none",
                        font = dict(size = 12,color = "black",family = "arial"),
                        title = "",
                        title_font_size=35,
                        title_x=0,
                        title_font_color = "black",
                        polar = dict(radialaxis = dict(showticklabels = False,range=[-0.05,1.05])))

    return fig

#%%
@st.cache_data
def radar_def(df,team):
    """
    Funktion, um Radar-Charts für jede Mannschaft zu erstellen

    ----------
    df : Datensatz
    team : Der Verein, für den der Plot erstellt werden soll (needs "")

    """
    variables = ['GA',
                'shots.ag.Sh/90',
                'creation.ag.SCA Types.PassDead',
                'poss.ag.Take-Ons.Succ',
                'poss.ag.Touches.Att Pen',
                'defense.Err',
                'misc.Performance.Fls',
                'misc.Aerial Duels.Won%']
    variables.append("Squad")
    df_subset = df[variables]

    # Variablen umbenennen
    df_subset.rename(columns = {
        "GA":"Gegentore",
        "shots.ag.Sh/90":"Gegn. Schüsse pro Spiel",
        "creation.ag.SCA Types.PassDead":"Gegn. Chancen<br>nach Standards",
        "poss.ag.Take-Ons.Succ":"Gegn. erfolgreiche Dribblings",
        "poss.ag.Touches.Att Pen":"Gegn. Ballkontakte im<br>Strafraum pro Spiel",
        "defense.Err":"Individuelle Fehler<br>vor gegn. Chance",
        "misc.Performance.Fls":"Fouls",
        "misc.Aerial Duels.Won%":"Gewonnene<br>Kopfballduelle (%)"
    },inplace = True)

    # Dieses subset ins long_format
    df_long = pd.melt(df_subset,id_vars=["Squad"])
    df_long["maxvalue"] = df_long.groupby(["variable"])['value'].transform("max")
    df_long["minvalue"] = df_long.groupby(["variable"])['value'].transform("min")
    df_long["average"] = df_long.groupby(["variable"])['value'].transform("mean")
    df_long["normal"] = (df_long['value'] - df_long['minvalue']) / (df_long['maxvalue'] - df_long['minvalue'])
    df_long["normalavg"] = df_long.groupby(["variable"])["normal"].transform("mean")
    df_long["value"] = df_long["value"].round(0).astype(int)
    df_long["Beschriftung"] = df_long["variable"].astype(str) + ": " + df_long["value"].astype(str)

    df_long = df_long[df_long["Squad"] == team]
    df_long.reset_index(drop = True,inplace = True)

    # Plot
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r = df_long["normal"],
        theta=df_long["Beschriftung"],
        fill = 'toself',
        name = df_long.loc[0,"Squad"],
        fillcolor= "green"
    ))
    fig.add_trace(go.Scatterpolar(
        r = df_long["normalavg"],
        theta=df_long["Beschriftung"],
        fill = 'toself',
        name = "Durchschnitt",
        fillcolor= "gray"
    ))
    fig.update_traces(opacity=0.4,  # Set fill opacity
                    line=dict(width=0),  # Set line opacity
                    mode = 'lines')    
    fig.update_polars(bgcolor='white',
                        gridshape = "linear",
                        hole = 0,
                        angularaxis = dict(
                            gridcolor= "gray",
                            griddash = "dot",
                            linecolor = "black",
                            linewidth = 0.5,
                            ticks = ""),
                        radialaxis = dict(
                            color = "white",
                            gridwidth = 0.1,
                            dtick = 0.25,
                            linecolor = "white",
                            showline = False,
                            ticks = ""
                            ))                 
    fig.update_layout(template = "none",
                        showlegend=False,
                        dragmode = False,
                        clickmode = "none",
                        font = dict(size = 12,color = "black",family = "arial"),
                        title = "",
                        title_font_size=35,
                        title_x=0,
                        title_font_color = "black",
                        polar = dict(radialaxis = dict(showticklabels = False,range=[-0.05,1.05])))

    return fig
#%% Dashboard
st.subheader("Teamprofile",divider = "rainbow")
option = st.selectbox("Wähle das Team, dessen Statistiken dargestellt werden sollen",options = df["Squad"].sort_values(),index = 5)
index = df[df["Squad"] == option].index[0]
image_name = df.loc[index,"Squad"]+".png"
col1,col2 = st.columns((1,7),gap= "small")
if option == df.loc[index,"Squad"]:
    with col1:
        st.image(images[image_name])
    with col2:
        auswahl = st.radio("",options = ["Offensiv","Passprofil","Defensiv","Gesamt","Hypothetisch"],horizontal = True)
if auswahl == "Offensiv":
    st.plotly_chart(radar_off(df,df.loc[index,'Squad']),use_container_width=True)
if auswahl == "Passprofil":
    st.plotly_chart(radar_pass(df,df.loc[index,'Squad']),use_container_width=True)
if auswahl == "Defensiv":
    st.plotly_chart(radar_def(df,df.loc[index,'Squad']),use_container_width=True)
if auswahl == "Gesamt":
    st.write("---- in Arbeit ----")
if auswahl == "Hypothetisch":
    st.write("---- in Arbeit ----")
with st.expander("Erklärung"):
    st.markdown("""
                Die grüne Fläche stellt das Profil der ausgewählten Mannschaft dar, die graue Fläche den Ligadurchschnitt.
                Die Daten sind ligaweit normalisiert. Das heißt:
                Beim Team mit den meisten Toren in der Liga wird der Graph bis an den Rand reichen, beim Team mit den 
                wenigsten Toren ist der Graph auf der Achse fast nicht zu sehen. Je größer also die farbige Fläche, desto 
                besser in den meisten Fällen die Leistung. Allerdings gibt es auch Statistiken, in denen mehr nicht automatisch
                besser ist. Viele lange Bälle oder Flanken sind beispielsweise nicht zwangsweise ein gutes Zeichen für das Spiel 
                einer Mannschaft.
                """)
