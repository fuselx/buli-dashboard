# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
#import numpy as np
import plotly.express as px
import requests
import io
from PIL import Image
st.set_page_config(layout="centered")


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
    target = 21
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
    target = 21
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
    df["passing.PrgP/90"] = df["passing.PrgP"].div(df["MP"]).round(1)
    return df
df = load_data()

#%% Import der Bilder, als Objekt speichern
@st.cache_data
def images():
    directory = "https://raw.githubusercontent.com/fuselx/buli-dashboard/main/Logos%20Zweite%20Liga/"
    images = {}
    for index, row in df.iterrows():
        image_name = row["Squad"] + ".png"  # gesuchter Name des Logos
        image_path = directory + image_name
        response = requests.get(image_path, stream=True)
        img = Image.open(io.BytesIO(response.content)).convert("RGBA")
        images[image_name] = img
    return images
images = images()
#%%
@st.cache_data
def radar_ges(df,team):
    """
    Funktion, um Radar-Charts für jede Mannschaft zu erstellen

    ----------
    df : Datensatz
    team : Der Verein, für den der Plot erstellt werden soll (needs "")

    """
    # Tore, xG, Gegentore, xAG,Ballbesitz,Ballkontakte letztes Drittel, erfolg. Dribblings, 
    df_copy = df.copy()
    i = df_copy[df_copy['Squad'] == team].index[0]
    Pässe = (df_copy.at[i,"passing.Total.pergame"]-min(df_copy["passing.Total.pergame"]))/(max(df_copy["passing.Total.pergame"])-min(df_copy["passing.Total.pergame"]))
    Passgenauigkeit = (df_copy.at[i,"passing.Total.Cmp%"]-min(df_copy["passing.Total.Cmp%"]))/(max(df_copy["passing.Total.Cmp%"])-min(df_copy["passing.Total.Cmp%"]))
    ProgP = (df_copy.at[i,"passing.PrgP"]-min(df_copy["passing.PrgP"]))/(max(df_copy["passing.PrgP"])-min(df_copy["passing.PrgP"]))
    TB = (df_copy.at[i,"pt.Pass Types.TB"]-min(df_copy["pt.Pass Types.TB"]))/(max(df_copy["pt.Pass Types.TB"])-min(df_copy["pt.Pass Types.TB"]))
    Ballbesitz = (df_copy.at[i,"Poss"]-min(df_copy["Poss"]))/(max(df_copy["Poss"])-min(df_copy["Poss"]))
    Flankenwechsel = (df_copy.at[i,"pt.Pass Types.Sw"]-min(df_copy["pt.Pass Types.Sw"]))/(max(df_copy["pt.Pass Types.Sw"])-min(df_copy["pt.Pass Types.Sw"]))
    Flanken = (df_copy.at[i,"pt.Pass Types.Crs"]-min(df_copy["pt.Pass Types.Crs"]))/(max(df_copy["pt.Pass Types.Crs"])-min(df_copy["pt.Pass Types.Crs"]))
    LangeB = (df_copy.at[i,"passing.LongPct"]-min(df_copy["passing.LongPct"]))/(max(df_copy["passing.LongPct"])-min(df_copy["passing.LongPct"]))
    
    df_copy['n_Pässe'] = (df_copy['passing.Total.pergame'] - df_copy['passing.Total.pergame'].min()) / (df_copy['passing.Total.pergame'].max() - df_copy['passing.Total.pergame'].min())
    df_copy['n_Passgenauigkeit'] = (df_copy['passing.Total.Cmp%'] - df_copy['passing.Total.Cmp%'].min()) / (df_copy['passing.Total.Cmp%'].max() - df_copy['passing.Total.Cmp%'].min())
    df_copy['n_ProgP'] = (df_copy['passing.PrgP'] - df_copy['passing.PrgP'].min()) / (df_copy['passing.PrgP'].max() - df_copy['passing.PrgP'].min())
    df_copy['n_TB'] = (df_copy['pt.Pass Types.TB'] - df_copy['pt.Pass Types.TB'].min()) / (df_copy['pt.Pass Types.TB'].max() - df_copy['pt.Pass Types.TB'].min())
    df_copy['n_Ballbesitz'] = (df_copy['Poss'] - df_copy['Poss'].min()) / (df_copy['Poss'].max() - df_copy['Poss'].min())
    df_copy['n_Flankenwechsel'] = (df_copy['pt.Pass Types.Sw'] - df_copy['pt.Pass Types.Sw'].min()) / (df_copy['pt.Pass Types.Sw'].max() - df_copy['pt.Pass Types.Sw'].min())
    df_copy['n_Flanken'] = (df_copy['pt.Pass Types.Crs'] - df_copy['pt.Pass Types.Crs'].min()) / (df_copy['pt.Pass Types.Crs'].max() - df_copy['pt.Pass Types.Crs'].min())
    df_copy['n_LangeB'] = (df_copy['passing.LongPct'] - df_copy['passing.LongPct'].min()) / (df_copy['passing.LongPct'].max() - df_copy['passing.LongPct'].min())
    
    dPässe = df_copy["n_Pässe"].mean()
    dPassgenauigkeit = df_copy["n_Passgenauigkeit"].mean()
    dProgP = df_copy["n_ProgP"].mean()
    dTB = df_copy["n_TB"].mean()
    dBallbesitz = df_copy["n_Ballbesitz"].mean()
    dFlankenwechsel = df_copy["n_Flankenwechsel"].mean()
    dFlanken = df_copy["n_Flanken"].mean()
    dLangeB =  df_copy["n_LangeB"].mean()
    
    df1 = pd.DataFrame(dict( # Teamwert
        r = [Pässe,Ballbesitz,Passgenauigkeit,ProgP,TB,LangeB,Flankenwechsel,Flanken,Pässe],
        theta = [f"Pässe pro Spiel: {df_copy.at[i,'passing.Total.pergame']}",
                 f"Ballbesitz: {df_copy.at[i,'Poss']}%",
                 f"Passquote: {df_copy.at[i,'passing.Total.Cmp%']}%",
                 f"Progressive Pässe pro Spiel: {df_copy.at[i,'passing.PrgP']}", 
                 f"Through Balls: {df_copy.at[i,'pt.Pass Types.TB']}",
                 f"Anteil langer Bälle: {df_copy.at[i,'passing.LongPct']}%",
                 f"Flankenwechsel pro Spiel: {df_copy.at[i,'pt.Pass Types.Sw']}",
                 f"Flanken pro Spiel: {df_copy.at[i,'pt.Pass Types.Crs']}",
                 f"Pässe pro Spiel: {df_copy.at[i,'passing.Total.pergame']}"]))
    
    df2 = pd.DataFrame(dict( # Liga-Durchschnitt
        r = [dPässe,dBallbesitz,dPassgenauigkeit,dProgP,dTB,dLangeB,dFlankenwechsel,dFlanken,dPässe],
        theta = [f"Pässe pro Spiel: {df_copy.at[i,'passing.Total.pergame']}",
                 f"Ballbesitz: {df_copy.at[i,'Poss']}%",
                 f"Passquote: {df_copy.at[i,'passing.Total.Cmp%']}%",
                 f"Progressive Pässe pro Spiel: {df_copy.at[i,'passing.PrgP']}", 
                 f"Through Balls: {df_copy.at[i,'pt.Pass Types.TB']}",
                 f"Anteil langer Bälle: {df_copy.at[i,'passing.LongPct']}%",
                 f"Flankenwechsel pro Spiel: {df_copy.at[i,'pt.Pass Types.Sw']}",
                 f"Flanken pro Spiel: {df_copy.at[i,'pt.Pass Types.Crs']}",
                 f"Pässe pro Spiel: {df_copy.at[i,'passing.Total.pergame']}"]))
    
    df1['Model'] = team
    df2['Model'] = 'Ligadurchschnitt'
    df = pd.concat([df1,df2], axis=0)
    color_discrete_map = {
    team: 'green',
    'Ligadurchschnitt': 'gray',
}

    fig = px.line_polar(df,r='r',color = 'Model',theta = 'theta',
                        color_discrete_map=color_discrete_map,line_shape = "linear")
    fig.update_traces(fill='toself',
                      opacity=0.6,  # Set fill opacity
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
#%% Radar-Chart Offensive
@st.cache_data
def radar_off(df,team):
    """
    Funktion, um Radar-Charts für jede Mannschaft zu erstellen

    ----------
    df : Datensatz
    team : Der Verein, für den der Plot erstellt werden soll (needs "")

    """
    df_copy = df.copy()
    df_copy['shots.npxG/Sh'] = (df_copy['shots.npxG/Sh']*100).astype('int')
    df_copy['poss.Touches.Att 3rd'] = df_copy['poss.Touches.Att 3rd'].div(df_copy['MP']).round(0).astype('int')
    i = df_copy[df_copy['Squad'] == team].index[0]
    npxG = (df_copy.at[i,"shots.npxG/Sh"]-min(df_copy["shots.npxG/Sh"]))/(max(df_copy["shots.npxG/Sh"])-min(df_copy["shots.npxG/Sh"]))
    Gls = (df_copy.at[i,"shots.Gls"]-min(df_copy["shots.Gls"]))/(max(df_copy["shots.Gls"])-min(df_copy["shots.Gls"]))
    Sh = (df_copy.at[i,"shots.Sh/90"]-min(df_copy["shots.Sh/90"]))/(max(df_copy["shots.Sh/90"])-min(df_copy["shots.Sh/90"]))
    OffKon = (df_copy.at[i,"poss.Touches.Att 3rd"]-min(df_copy["poss.Touches.Att 3rd"]))/(max(df_copy["poss.Touches.Att 3rd"])-min(df_copy["poss.Touches.Att 3rd"]))
    Ballbesitz = (df_copy.at[i,"Poss"]-min(df_copy["Poss"]))/(max(df_copy["Poss"])-min(df_copy["Poss"]))
    PgrPass = (df_copy.at[i,"passing.PrgP/90"]-min(df_copy["passing.PrgP/90"]))/(max(df_copy["passing.PrgP/90"])-min(df_copy["passing.PrgP/90"]))
    OffStd = (df_copy.at[i,"creation.SCA Types.PassDead"]-min(df_copy["creation.SCA Types.PassDead"]))/(max(df_copy["creation.SCA Types.PassDead"])-min(df_copy["creation.SCA Types.PassDead"]))
    Dribb = (df_copy.at[i,"poss.Take-Ons.Succ"]-min(df_copy["poss.Take-Ons.Succ"]))/(max(df_copy["poss.Take-Ons.Succ"])-min(df_copy["poss.Take-Ons.Succ"]))
    
    df_copy['n_npxG'] = (df_copy['shots.npxG/Sh'] - df_copy['shots.npxG/Sh'].min()) / (df_copy['shots.npxG/Sh'].max() - df_copy['shots.npxG/Sh'].min())
    df_copy['n_Gls'] = (df_copy['shots.Gls'] - df_copy['shots.Gls'].min()) / (df_copy['shots.Gls'].max() - df_copy['shots.Gls'].min())
    df_copy['n_Sh'] = (df_copy['shots.Sh/90'] - df_copy['shots.Sh/90'].min()) / (df_copy['shots.Sh/90'].max() - df_copy['shots.Sh/90'].min())
    df_copy['n_OffKon'] = (df_copy['poss.Touches.Att 3rd'] - df_copy['poss.Touches.Att 3rd'].min()) / (df_copy['poss.Touches.Att 3rd'].max() - df_copy['poss.Touches.Att 3rd'].min())
    df_copy['n_Ballbesitz'] = (df_copy['Poss'] - df_copy['Poss'].min()) / (df_copy['Poss'].max() - df_copy['Poss'].min())
    df_copy['n_PgrPass'] = (df_copy['passing.PrgP/90'] - df_copy['passing.PrgP/90'].min()) / (df_copy['passing.PrgP/90'].max() - df_copy['passing.PrgP/90'].min())
    df_copy['n_OffStd'] = (df_copy['creation.SCA Types.PassDead'] - df_copy['creation.SCA Types.PassDead'].min()) / (df_copy['creation.SCA Types.PassDead'].max() - df_copy['creation.SCA Types.PassDead'].min())
    df_copy['n_Dribb'] = (df_copy['poss.Take-Ons.Succ'] - df_copy['poss.Take-Ons.Succ'].min()) / (df_copy['poss.Take-Ons.Succ'].max() - df_copy['poss.Take-Ons.Succ'].min())
    
    dnpxG = df_copy["n_npxG"].mean()
    dGls = df_copy["n_Gls"].mean()
    dSh = df_copy["n_Sh"].mean()
    dOffKon = df_copy["n_OffKon"].mean()
    dBallbesitz = df_copy["n_Ballbesitz"].mean()
    dPgrPass = df_copy["n_PgrPass"].mean()
    dOffStd = df_copy["n_OffStd"].mean()
    dDribb =  df_copy["n_Dribb"].mean()
    
    df1 = pd.DataFrame(dict( # Teamwert
        r = [Gls,Sh,npxG,OffKon,Ballbesitz,PgrPass,Dribb,OffStd,Gls],
        theta = [f"Tore: {df_copy.at[i,'shots.Gls']}",
                 f"Schüsse pro Spiel: {df_copy.at[i,'shots.Sh/90']}",
                 f"xGoals pro Schuss: {df_copy.at[i,'shots.npxG/Sh']}%",
                 f"Ballkontakte im letzten Drittel pro Spiel: {df_copy.at[i,'poss.Touches.Att 3rd']}",
                 f"Ballbesitz: {df_copy.at[i,'Poss']}%",
                 f"Prog. Pässe pro Spiel: {df_copy.at[i,'passing.PrgP/90']}",
                 f"Erfolgreiche Dribblings: {df_copy.at[i,'poss.Take-Ons.Succ']}",
                 f"Chancen nach Offensivstandards: {df_copy.at[i,'creation.SCA Types.PassDead']}",
                 f"Tore: {df_copy.at[i,'shots.Gls']}"]))
    
    df2 = pd.DataFrame(dict( # Liga-Durchschnitt
        r = [dGls,dSh,dnpxG,dOffKon,dBallbesitz,dPgrPass,dDribb,dOffStd,dGls],
        theta = [f"Tore: {df_copy.at[i,'shots.Gls']}",
                 f"Schüsse pro Spiel: {df_copy.at[i,'shots.Sh/90']}",
                 f"xGoals pro Schuss: {df_copy.at[i,'shots.npxG/Sh']}%",
                 f"Ballkontakte im letzten Drittel pro Spiel: {df_copy.at[i,'poss.Touches.Att 3rd']}",
                 f"Ballbesitz: {df_copy.at[i,'Poss']}%",
                 f"Prog. Pässe pro Spiel: {df_copy.at[i,'passing.PrgP/90']}",
                 f"Erfolgreiche Dribblings: {df_copy.at[i,'poss.Take-Ons.Succ']}",
                 f"Chancen nach Offensivstandards: {df_copy.at[i,'creation.SCA Types.PassDead']}",
                 f"Tore: {df_copy.at[i,'shots.Gls']}"]))
    
    df1['Model'] = team
    df2['Model'] = 'Ligadurchschnitt'
    df = pd.concat([df1,df2], axis=0)
    color_discrete_map = {
    team: 'green',
    'Ligadurchschnitt': 'gray',
}

    fig = px.line_polar(df,r='r',color = 'Model',theta = 'theta',
                        color_discrete_map=color_discrete_map,line_shape = "linear")
    fig.update_traces(fill='toself',
                      opacity=0.6,  # Set fill opacity
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
    df_copy = df.copy()
    df_copy['passing.Total.pergame'] = df_copy["passing.Total.Att"].div(df_copy['MP']).astype('int') #pro Spiel
    df_copy['pt.Pass Types.Sw'] = df_copy['pt.Pass Types.Sw'].div(df_copy['MP']).round(1) #pro Spiel
    df_copy['pt.Pass Types.Crs'] = df_copy['pt.Pass Types.Crs'].div(df_copy['MP']).round(1) #pro Spiel
    df_copy['passing.PrgP'] = df_copy['passing.PrgP'].div(df_copy['MP']).round(1) #pro Spiel
    i = df_copy[df_copy['Squad'] == team].index[0]
    Pässe = (df_copy.at[i,"passing.Total.pergame"]-min(df_copy["passing.Total.pergame"]))/(max(df_copy["passing.Total.pergame"])-min(df_copy["passing.Total.pergame"]))
    Passgenauigkeit = (df_copy.at[i,"passing.Total.Cmp%"]-min(df_copy["passing.Total.Cmp%"]))/(max(df_copy["passing.Total.Cmp%"])-min(df_copy["passing.Total.Cmp%"]))
    ProgP = (df_copy.at[i,"passing.PrgP"]-min(df_copy["passing.PrgP"]))/(max(df_copy["passing.PrgP"])-min(df_copy["passing.PrgP"]))
    TB = (df_copy.at[i,"pt.Pass Types.TB"]-min(df_copy["pt.Pass Types.TB"]))/(max(df_copy["pt.Pass Types.TB"])-min(df_copy["pt.Pass Types.TB"]))
    Ballbesitz = (df_copy.at[i,"Poss"]-min(df_copy["Poss"]))/(max(df_copy["Poss"])-min(df_copy["Poss"]))
    Flankenwechsel = (df_copy.at[i,"pt.Pass Types.Sw"]-min(df_copy["pt.Pass Types.Sw"]))/(max(df_copy["pt.Pass Types.Sw"])-min(df_copy["pt.Pass Types.Sw"]))
    Flanken = (df_copy.at[i,"pt.Pass Types.Crs"]-min(df_copy["pt.Pass Types.Crs"]))/(max(df_copy["pt.Pass Types.Crs"])-min(df_copy["pt.Pass Types.Crs"]))
    LangeB = (df_copy.at[i,"passing.LongPct"]-min(df_copy["passing.LongPct"]))/(max(df_copy["passing.LongPct"])-min(df_copy["passing.LongPct"]))
    
    df_copy['n_Pässe'] = (df_copy['passing.Total.pergame'] - df_copy['passing.Total.pergame'].min()) / (df_copy['passing.Total.pergame'].max() - df_copy['passing.Total.pergame'].min())
    df_copy['n_Passgenauigkeit'] = (df_copy['passing.Total.Cmp%'] - df_copy['passing.Total.Cmp%'].min()) / (df_copy['passing.Total.Cmp%'].max() - df_copy['passing.Total.Cmp%'].min())
    df_copy['n_ProgP'] = (df_copy['passing.PrgP'] - df_copy['passing.PrgP'].min()) / (df_copy['passing.PrgP'].max() - df_copy['passing.PrgP'].min())
    df_copy['n_TB'] = (df_copy['pt.Pass Types.TB'] - df_copy['pt.Pass Types.TB'].min()) / (df_copy['pt.Pass Types.TB'].max() - df_copy['pt.Pass Types.TB'].min())
    df_copy['n_Ballbesitz'] = (df_copy['Poss'] - df_copy['Poss'].min()) / (df_copy['Poss'].max() - df_copy['Poss'].min())
    df_copy['n_Flankenwechsel'] = (df_copy['pt.Pass Types.Sw'] - df_copy['pt.Pass Types.Sw'].min()) / (df_copy['pt.Pass Types.Sw'].max() - df_copy['pt.Pass Types.Sw'].min())
    df_copy['n_Flanken'] = (df_copy['pt.Pass Types.Crs'] - df_copy['pt.Pass Types.Crs'].min()) / (df_copy['pt.Pass Types.Crs'].max() - df_copy['pt.Pass Types.Crs'].min())
    df_copy['n_LangeB'] = (df_copy['passing.LongPct'] - df_copy['passing.LongPct'].min()) / (df_copy['passing.LongPct'].max() - df_copy['passing.LongPct'].min())
    
    dPässe = df_copy["n_Pässe"].mean()
    dPassgenauigkeit = df_copy["n_Passgenauigkeit"].mean()
    dProgP = df_copy["n_ProgP"].mean()
    dTB = df_copy["n_TB"].mean()
    dBallbesitz = df_copy["n_Ballbesitz"].mean()
    dFlankenwechsel = df_copy["n_Flankenwechsel"].mean()
    dFlanken = df_copy["n_Flanken"].mean()
    dLangeB =  df_copy["n_LangeB"].mean()
    
    df1 = pd.DataFrame(dict( # Teamwert
        r = [Pässe,Ballbesitz,Passgenauigkeit,ProgP,TB,LangeB,Flankenwechsel,Flanken,Pässe],
        theta = [f"Pässe pro Spiel: {df_copy.at[i,'passing.Total.pergame']}",
                 f"Ballbesitz: {df_copy.at[i,'Poss']}%",
                 f"Passquote: {df_copy.at[i,'passing.Total.Cmp%']}%",
                 f"Progressive Pässe pro Spiel: {df_copy.at[i,'passing.PrgP']}", 
                 f"Through Balls: {df_copy.at[i,'pt.Pass Types.TB']}",
                 f"Anteil langer Bälle: {df_copy.at[i,'passing.LongPct']}%",
                 f"Flankenwechsel pro Spiel: {df_copy.at[i,'pt.Pass Types.Sw']}",
                 f"Flanken pro Spiel: {df_copy.at[i,'pt.Pass Types.Crs']}",
                 f"Pässe pro Spiel: {df_copy.at[i,'passing.Total.pergame']}"]))
    
    df2 = pd.DataFrame(dict( # Liga-Durchschnitt
        r = [dPässe,dBallbesitz,dPassgenauigkeit,dProgP,dTB,dLangeB,dFlankenwechsel,dFlanken,dPässe],
        theta = [f"Pässe pro Spiel: {df_copy.at[i,'passing.Total.pergame']}",
                 f"Ballbesitz: {df_copy.at[i,'Poss']}%",
                 f"Passquote: {df_copy.at[i,'passing.Total.Cmp%']}%",
                 f"Progressive Pässe pro Spiel: {df_copy.at[i,'passing.PrgP']}", 
                 f"Through Balls: {df_copy.at[i,'pt.Pass Types.TB']}",
                 f"Anteil langer Bälle: {df_copy.at[i,'passing.LongPct']}%",
                 f"Flankenwechsel pro Spiel: {df_copy.at[i,'pt.Pass Types.Sw']}",
                 f"Flanken pro Spiel: {df_copy.at[i,'pt.Pass Types.Crs']}",
                 f"Pässe pro Spiel: {df_copy.at[i,'passing.Total.pergame']}"]))
    
    df1['Model'] = team
    df2['Model'] = 'Ligadurchschnitt'
    df = pd.concat([df1,df2], axis=0)
    color_discrete_map = {
    team: 'green',
    'Ligadurchschnitt': 'gray',
}

    fig = px.line_polar(df,r='r',color = 'Model',theta = 'theta',
                        color_discrete_map=color_discrete_map,line_shape = "linear")
    fig.update_traces(fill='toself',
                      opacity=0.6,  # Set fill opacity
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
    st.write("---- in Arbeit ----")
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
