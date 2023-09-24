import pandas as pd
import matplotlib.pyplot  as plt
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import streamlit as st
import plotly.express as px
from PIL import Image
import requests
import io

directory = "https://raw.githubusercontent.com/fuselwolga/buli-dashboard/main/Logos%20Zweite%20Liga/"
# layout 
st.set_page_config(layout="wide")
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
    return df
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

#%% Import der Bilder, als Objekt speichern
@st.cache_data
def images():
    directory = "https://raw.githubusercontent.com/fuselwolga/buli-dashboard/main/Logos%20Zweite%20Liga/"
    images = {}
    for index, row in df.iterrows():
        image_name = row["Squad"] + ".png"  # gesuchter Name des Logos
        image_path = directory + image_name
        response = requests.get(image_path, stream=True)
        img = Image.open(io.BytesIO(response.content)).convert("RGBA")
        images[image_name] = img
    return images
#%% Funktion für Scatter Plots
@st.cache_data
def scatter(df,var1,var2,title = None ,xlab = None, ylab = None,pergame = None):
    """
    Einfache Funktion, um  Scatter-Plots für zwei Variablen mit den richtigen Logos auszugeben.
    Funktioniert nur für meinen Datensatz.

    ----------
    df    : Datensatz
    var1  : Variable auf der x-Achse (needs "")
    var2  : Variable auf der y-Achse (needs "")
    title : Diagrammtitel
    xlabel: X-Achsenbeschriftung
    ylabel: Y-Achsenbeschriftung

    """
    df_copy = df.copy()
    if pergame == "x":
        df_copy[var1] = df_copy[var1].div(df_copy['MP']).round(2)
    if pergame == "y":
        df_copy[var2] = df_copy[var2].div(df_copy['MP']).round(2)
    if pergame == "xy":
        df_copy[var1] = df_copy[var1].div(df_copy['MP']).round(2)
        df_copy[var2] = df_copy[var2].div(df_copy['MP']).round(2)
    fig = plt.figure()
    plt.scatter(df_copy[var1],df_copy[var2])
    for index, row in df_copy.iterrows():
        image_name = row["Squad"] + ".png"  # gesuchter Name des Logos
        imagebox = OffsetImage(images[image_name], zoom=0.3)
        ab = AnnotationBbox(imagebox, (row[var1], row[var2]), frameon=False)
        plt.gca().add_artist(ab)

    plt.axvline(x=np.mean(df_copy[var1]),linewidth = 0.5, linestyle = "--",color = "0.5")        
    plt.axhline(y=np.mean(df_copy[var2]),linewidth = 0.5, linestyle = "--",color = "0.5")
    if title == None:
        plt.title(var1 + " x " + var2,fontsize=13)
    else:
        plt.title(title,fontsize=13)
    if xlab == None:
        plt.xlabel(var1)
    else:
        plt.xlabel(xlab)
    if xlab == None:
        plt.ylabel(var2)
    else:
        plt.ylabel(ylab)
    return fig


#%% Bar Plot
@st.cache_data
def hbar(df,var,title = None,pergame = False):
    """
    Einfache Funktion, um horizontale Bar-Plots für eine Variable mit den richtigen Logos auszugeben.
    Funktioniert nur für meinen Datensatz.

    ----------
    df : Datensatz
    var : Variable, die dargestellt werden soll (needs "")
    title : Diagrammtitel

    """
    df_copy = df.copy()
    if pergame == True:
        df_copy[var] = df_copy[var].div(df_copy['MP']).round(2)
    if df_copy[var].dtype == 'float64':
        df_copy[var] = round(df_copy[var],2)
    if df_copy[var].mean() >= 10:
        df_copy[var] = round(df_copy[var],1)
    if df_copy[var].mean() >= 100:
        df_copy[var] = round(df_copy[var],0).astype("int")       
    sort_df = df_copy.sort_values(by=var,ascending=True)
    fig = plt.figure()
    plt.barh(sort_df['Squad'],sort_df[var],color = "#85BD86",edgecolor="0",linewidth = 0.3)
    for i,v in enumerate(sort_df[var]):
        plt.text(v-(max(sort_df[var])*0.05),i-0.08,str(v),ha='center',va='center',fontsize=9.1,color="0.1")
    for index, row in sort_df.iterrows():
        image_name = row["Squad"] + ".png"  # gesuchter Name des Logos
        imagebox = OffsetImage(images[image_name], zoom = 0.17)
        ab = AnnotationBbox(imagebox, (row[var]+max(sort_df[var])*0.035,row['Squad']),frameon=False)
        plt.gca().add_artist(ab)
    if title == None:
        plt.title(var,fontsize=12)
    else:
        plt.title(title,fontsize=12)
    plt.axvline(x=np.mean(sort_df[var]),linewidth = 0.5,color = "0.5",linestyle = "--")
    plt.xticks([])
    plt.yticks([])
    plt.axis(xmax = max(sort_df[var]) + max(sort_df[var])*0.2)
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
    KeyPass = (df_copy.at[i,"passing.KP"]-min(df_copy["passing.KP"]))/(max(df_copy["passing.KP"])-min(df_copy["passing.KP"]))
    OffStd = (df_copy.at[i,"creation.SCA Types.PassDead"]-min(df_copy["creation.SCA Types.PassDead"]))/(max(df_copy["creation.SCA Types.PassDead"])-min(df_copy["creation.SCA Types.PassDead"]))
    Dribb = (df_copy.at[i,"poss.Take-Ons.Succ"]-min(df_copy["poss.Take-Ons.Succ"]))/(max(df_copy["poss.Take-Ons.Succ"])-min(df_copy["poss.Take-Ons.Succ"]))
    
    df_copy['n_npxG'] = (df_copy['shots.npxG/Sh'] - df_copy['shots.npxG/Sh'].min()) / (df_copy['shots.npxG/Sh'].max() - df_copy['shots.npxG/Sh'].min())
    df_copy['n_Gls'] = (df_copy['shots.Gls'] - df_copy['shots.Gls'].min()) / (df_copy['shots.Gls'].max() - df_copy['shots.Gls'].min())
    df_copy['n_Sh'] = (df_copy['shots.Sh/90'] - df_copy['shots.Sh/90'].min()) / (df_copy['shots.Sh/90'].max() - df_copy['shots.Sh/90'].min())
    df_copy['n_OffKon'] = (df_copy['poss.Touches.Att 3rd'] - df_copy['poss.Touches.Att 3rd'].min()) / (df_copy['poss.Touches.Att 3rd'].max() - df_copy['poss.Touches.Att 3rd'].min())
    df_copy['n_Ballbesitz'] = (df_copy['Poss'] - df_copy['Poss'].min()) / (df_copy['Poss'].max() - df_copy['Poss'].min())
    df_copy['n_KeyPass'] = (df_copy['passing.KP'] - df_copy['passing.KP'].min()) / (df_copy['passing.KP'].max() - df_copy['passing.KP'].min())
    df_copy['n_OffStd'] = (df_copy['creation.SCA Types.PassDead'] - df_copy['creation.SCA Types.PassDead'].min()) / (df_copy['creation.SCA Types.PassDead'].max() - df_copy['creation.SCA Types.PassDead'].min())
    df_copy['n_Dribb'] = (df_copy['poss.Take-Ons.Succ'] - df_copy['poss.Take-Ons.Succ'].min()) / (df_copy['poss.Take-Ons.Succ'].max() - df_copy['poss.Take-Ons.Succ'].min())
    
    dnpxG = df_copy["n_npxG"].mean()
    dGls = df_copy["n_Gls"].mean()
    dSh = df_copy["n_Sh"].mean()
    dOffKon = df_copy["n_OffKon"].mean()
    dBallbesitz = df_copy["n_Ballbesitz"].mean()
    dKeyPass = df_copy["n_KeyPass"].mean()
    dOffStd = df_copy["n_OffStd"].mean()
    dDribb =  df_copy["n_Dribb"].mean()
    
    df1 = pd.DataFrame(dict( # Teamwert
        r = [Gls,Sh,npxG,OffKon,Ballbesitz,KeyPass,Dribb,OffStd,Gls],
        theta = [f"Tore: {df_copy.at[i,'shots.Gls']}",
                 f"Schüsse pro Spiel: {df_copy.at[i,'shots.Sh/90']}",
                 f"xGoals pro Schuss: {df_copy.at[i,'shots.npxG/Sh']}%",
                 f"Ballkontakte im letzten Drittel pro Spiel: {df_copy.at[i,'poss.Touches.Att 3rd']}",
                 f"Ballbesitz: {df_copy.at[i,'Poss']}%",
                 f"Key Passes: {df_copy.at[i,'passing.KP']}",
                 f"Erfolgreiche Dribblings: {df_copy.at[i,'poss.Take-Ons.Succ']}",
                 f"Chancen nach Offensivstandards: {df_copy.at[i,'creation.SCA Types.PassDead']}",
                 f"Tore: {df_copy.at[i,'shots.Gls']}"]))
    
    df2 = pd.DataFrame(dict( # Liga-Durchschnitt
        r = [dGls,dSh,dnpxG,dOffKon,dBallbesitz,dKeyPass,dDribb,dOffStd,dGls],
        theta = [f"Tore: {df_copy.at[i,'shots.Gls']}",
                 f"Schüsse pro Spiel: {df_copy.at[i,'shots.Sh/90']}",
                 f"xGoals pro Schuss: {df_copy.at[i,'shots.npxG/Sh']}%",
                 f"Ballkontakte im letzten Drittel pro Spiel: {df_copy.at[i,'poss.Touches.Att 3rd']}",
                 f"Ballbesitz: {df_copy.at[i,'Poss']}%",
                 f"Key Passes: {df_copy.at[i,'passing.KP']}",
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

#%%
@st.cache_data
def radar_ges(df,team):
    """
    Funktion, um Radar-Charts für jede Mannschaft zu erstellen

    ----------
    df : Datensatz
    team : Der Verein, für den der Plot erstellt werden soll (needs "")

    """
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
#%% Vorbereitung von Tabellen für das Dashboard
# Team-Stastistiken
df = load_data()
df['passing.avgDist'] = df['passing.Total.TotDist'].div(df['passing.Total.Att'])
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
# Spieltage
md = matchdays()



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




hidefullscreen =    '''
                    <style>
                    button[title="View fullscreen"]{
                       { visibility: hidden;}
                    </style>
                    '''
#%% Tabellen Styles

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


md_small = md[["Spieltag","Tag","Anstoß","Heim","Ergebnis","Auswärts"]]
md_small_style = [{'selector':'td:nth-child(6)',
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

                    
#%% Hier fängt das Dashboard an

st.title("Zweitliga-Dashboard")
        
col1,col2 = st.columns((3,2),gap= "medium")


with col1:
    st.subheader("Tabelle",divider = "rainbow")
    on = st.toggle("Zeige Details")
    if on:  
        st.table(Tabelle.style.set_table_styles(Tabelle_style))
    else:
        st.table(Tabelle_slim.style.set_table_styles(Tabelle_style))
    st.subheader("Spieltag",divider = "rainbow")
    on = st.toggle("Zeige Details",key = "md-toogle_mobile")
    Start_index = df['MP'].max()
    Spieltag = st.slider("Wähle den Spieltag",min_value=1,max_value=34,value=Start_index,key="original")
    st.markdown("""
                   <style>
                   .css-1dx1gwv{
                       display:none}
                   </style>
                   """, unsafe_allow_html=True)
    if on:        
        if Spieltag > df.loc[0,'MP']:
                st.dataframe(md[md["Spieltag"] == Spieltag],
                             hide_index=True,height = 360,
                             column_order=("Tag","Datum","Anstoß","Heimlogo","Ergebnis","Auswärtslogo"),
                             column_config={'Heimlogo':st.column_config.ImageColumn('Heim',width = "small"),
                                            'Auswärtslogo':st.column_config.ImageColumn('Auswärts',width = "small")})
        else:
                st.dataframe(md[md["Spieltag"] == Spieltag],
                             hide_index=True,
                             height = 360,
                             column_order=("Tag","Datum","Anstoß","xG","Heimlogo","Ergebnis","Auswärtslogo","xG ","Zuschauer","Schiedsrichter"),
                             column_config={'Spieltag':None,
                                            'Heimlogo':st.column_config.ImageColumn('Heim',width = "small"),
                                            'Auswärtslogo':st.column_config.ImageColumn('Auswärts',width = "small"),
                                            'xG':st.column_config.ProgressColumn(
                                                min_value=0,
                                                max_value=md[md["Spieltag"] == Spieltag][['xG','xG ']].max().max(),
                                                format = "  %f",
                                                width = "small"),
                                            'xG ':st.column_config.ProgressColumn(
                                                min_value=0,
                                                max_value=md[md["Spieltag"] == Spieltag][['xG','xG ']].max().max(),
                                                format = "  %f",
                                                width = "small")                                            
                                         })
    else:
        st.write(f"__Spieltag {Spieltag}: {md[md['Spieltag'] == Spieltag].reset_index().loc[0,'Datum']} - {md[md['Spieltag'] == Spieltag].reset_index().loc[7,'Datum']}__")
        st.table(md_small[md_small["Spieltag"] == Spieltag].style.set_table_styles(md_small_style))
     
    


with col2:
    st.subheader("Eindimensionale Statistiken",divider = "rainbow")
    option = st.selectbox("Wähle die Statistik, die als Balkendiagramm dargestellt werden soll",options=["Expected Goals pro Spiel",
                                                                                                         "Expected Goals pro Spiel (ohne 11m)",
                                                                                                         "Expected Goals against pro Spiel",
                                                                                                         "Tore",
                                                                                                         "Gegentore",
                                                                                                         "Passgenauigkeit",
                                                                                                         "Passlänge",
                                                                                                         "Lange Bälle"])
    if option == "Expected Goals pro Spiel":
        st.pyplot(hbar(df,"shots.xG","Expected Goals pro Spiel",pergame = True))
    elif option == "Expected Goals pro Spiel (ohne 11m)":
        st.pyplot(hbar(df,"shots.npxG","Expected Goals pro Spiel (ohne 11m)",pergame = True))
    elif option == "Expected Goals against pro Spiel":
        st.pyplot(hbar(df,"xGA","Expected Goals against pro Spiel",pergame = True))
    elif option == "Tore":
        st.pyplot(hbar(df,"GF","Geschossene Tore"))
    elif option == "Gegentore":
        st.pyplot(hbar(df,"GA","Gegentore"))
    elif option == "Passgenauigkeit":
        st.pyplot(hbar(df,"passing.Total.Cmp%","Angekommene Pässe (in %)"))
    elif option == "Passlänge":
        st.pyplot(hbar(df,"passing.avgDist","Gespielte Distanz pro Pass in Metern",pergame = False))
    elif option == "Lange Bälle":
        st.pyplot(hbar(df,"passing.LongPct","Anteil langer Bälle an allen Pässen (in %)",pergame = False))
        st.caption("Pässe über eine Distanz von mehr als 32 Metern")
    
    st.subheader("Zweidimensionale Statistiken",divider = "rainbow")
    option = st.selectbox("Wähle die Statistik, die als Streudiagramm dargestellt werden soll", options = ['Schüsse',
                                                                                                           'Expected Goals',
                                                                                                           'Tordifferenz vs. xG',
                                                                                                           'Ballbesitz vs. Kontakte im Strafraum',
                                                                                                           "Pässe",
                                                                                                           "Kurzpässe",
                                                                                                           "Mittellange Pässe",
                                                                                                           "Lange Bälle",
                                                                                                           "Offensivstandards"])
    if option == "Schüsse":
        st.pyplot(scatter(df,"shots.Sh/90","shots.SoT/90",
                          title = "Schüsse (aufs Tor)",xlab = "Schüsse pro Spiel",ylab = "Schüsse aufs Tor pro Spiel"))
    if option == "Expected Goals":
        st.pyplot(scatter(df,"shots.xG","shots.ag.xG",pergame = "xy",
                          title = "Expected Goals (pro Spiel)",xlab = "Expected Goals",ylab = "Expected Goals against"))
    if option == "Tordifferenz vs. xG":
        st.pyplot(scatter(df,"xGD","GD",
                          title = "Tordifferenz erwartet vs. tatsächlich",xlab = "Tordifferenz erwartet",ylab = "Tordifferenz tatsächlich"))
    if option == "Ballbesitz vs. Kontakte im Strafraum":
        st.pyplot(scatter(df,"Poss","poss.Touches.Att Pen",pergame = "y",
                          title = "Ballbesitz",xlab = "Ballbesitz insgesamt",ylab = "Ballkontakte im Strafraum (pro Spiel)"))
    if option == "Pässe":
        st.pyplot(scatter(df,"passing.Total.Att","passing.Total.Cmp%", pergame = "x",
                          title = "Passgenauigkeit",xlab = "Gespielte Pässe pro Spiel",ylab = "Angekommene Pässe (in %)"))
    if option == "Kurzpässe":
         st.pyplot(scatter(df,"passing.Short.Att","passing.Short.Cmp%", pergame = "x",
                              title = "Passgenauigkeit Kurzpässe",xlab = "Gespielte Pässe pro Spiel",ylab = "Angekommene Pässe (in %)"))
         st.caption("Kurzpässe: Pässe zwischen 5 und 16 Metern (5/15 Yards)")
    if option == "Mittellange Pässe":
        st.pyplot(scatter(df,"passing.Medium.Att","passing.Medium.Cmp%", pergame = "x",
                          title = "Passgenauigkeit mittellange Pässe",xlab = "Gespielte Pässe pro Spiel",ylab = "Angekommene Pässe (in %)"))
        st.caption("Mittellange Pässe: Pässe zwischen 16 und 32 Metern (15/30 Yards)")
    if option == "Lange Bälle":
        st.pyplot(scatter(df,"passing.Long.Att","passing.Long.Cmp%", pergame = "x",
                          title = "Passgenauigkeit lange Bälle",xlab = "Gespielte Bälle pro Spiel",ylab = "Angekommene Bälle (in %)"))
        st.caption("Lange Bälle: Pässe über eine Strecke von mindesten 32 Metern (30 Yards)")
    if option == "Offensivstandards":
        st.pyplot(scatter(df,"creation.SCA Types.PassDead","creation.GCA Types.PassDead",
                          title = "Offensivstandards",xlab = "Chancen nach Standardsituationen",ylab = "Tore nach Standardsituationen"))


st.header("Teamvergleich",divider = "rainbow") 
on = st.toggle("Mobil-Version",key = "vergleich")
tab1,tab2 = st.tabs(["Offensiv","Passprofil"])
if on:
    with tab1:
        st.subheader("Offensivstatistiken",divider = "gray")
        option = st.selectbox("Wähle das Team, dessen Offensivstatistiken dargestellt werden sollen",options = df["Squad"].sort_values(),index = 5)
        index = df[df["Squad"] == option].index[0]
        if option == df.loc[index,"Squad"]:
            st.plotly_chart(radar_off(df,df.loc[index,'Squad']),use_container_width=True)        
    with tab2:
        st.subheader("Passstatistiken",divider = "gray")
        option = st.selectbox("Wähle das Team, dessen Passstatistiken  dargestellt werden sollen",options = df["Squad"].sort_values(),index = 5)
        index = df[df["Squad"] == option].index[0]
        if option == df.loc[index,"Squad"]:
            st.plotly_chart(radar_pass(df,df.loc[index,'Squad']),use_container_width=True)
else:
    with tab1:

        st.subheader("Offensivstatistiken",divider = "gray")
        subcol1, subcol2 = st.columns(2,gap = "small")
        with subcol1:
            option = st.selectbox("Wähle das Team, dessen Offensivstatistiken links dargestellt werden sollen",options = df["Squad"].sort_values(),index = 5)
            index = df[df["Squad"] == option].index[0]
            if option == df.loc[index,"Squad"]:
                st.plotly_chart(radar_off(df,df.loc[index,'Squad']),use_container_width=True)
        with subcol2:
            option = st.selectbox("Wähle das Team, dessen Offensivstatistiken rechts dargestellt werden sollen",options = df["Squad"].sort_values(),index = 0)
            index = df[df["Squad"] == option].index[0]
            if option == df.loc[index,"Squad"]:
                st.plotly_chart(radar_off(df,df.loc[index,'Squad']),use_container_width=True)
    with tab2:
        st.subheader("Passstatistiken",divider = "gray")
        subcol1, subcol2 = st.columns(2,gap = "small")
        with subcol1:
            option = st.selectbox("Wähle das Team, dessen Passstatistiken links dargestellt werden sollen",options = df["Squad"].sort_values(),index = 5)
            index = df[df["Squad"] == option].index[0]
            if option == df.loc[index,"Squad"]:
                st.plotly_chart(radar_pass(df,df.loc[index,'Squad']),use_container_width=True)
        with subcol2:
            option = st.selectbox("Wähle das Team, dessen Passstatistiken rechts dargestellt werden sollen",options = df["Squad"].sort_values(),index = 0)
            index = df[df["Squad"] == option].index[0]
            if option == df.loc[index,"Squad"]:
                st.plotly_chart(radar_pass(df,df.loc[index,'Squad']),use_container_width=True)        
