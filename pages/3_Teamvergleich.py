import streamlit as st
import pandas as pd
from PIL import Image
import requests
import io
import matplotlib.pyplot  as plt
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

st.set_page_config(
    page_title="Teamvergleich",
    page_icon="📊"
)
st.sidebar.success("Wähle aus der Liste oben den Punkt aus, den Du Dir anschauen möchtest!")
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
df = load_data()
df['passing.avgDist'] = df['passing.Total.TotDist'].div(df['passing.Total.Att'])
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
images = images()
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


#%% Dashboard
st.subheader("Teamrankings",divider = "rainbow")
st.markdown("""
            Hier kann aus unterschiedlichen Statistiken ausgewählt werden. Oben finden sich einfache Rankings, unten zweidimensionale Grafiken.
            """)
tab1,tab2,tab3,tab4 = st.tabs(["Offensiv","Defensiv","Passspiel","Sonstiges"])

with tab1:
    option = st.selectbox("",options=["Tore",
                                      "Schüsse",
                                      "Schüsse aufs Tor",
                                      "Expected Goals pro Spiel",
                                      "Expected Goals pro Spiel (ohne 11m)",
                                      "Abseits",
                                      "Dribblings",
                                      "Standardtore"])
    if option == "Tore":
           st.pyplot(hbar(df,"GF","Geschossene Tore"))
    elif option == "Expected Goals pro Spiel":
           st.pyplot(hbar(df,"shots.xG","Expected Goals pro Spiel",pergame = True))
    elif option == "Expected Goals pro Spiel (ohne 11m)":
           st.pyplot(hbar(df,"shots.npxG","Expected Goals pro Spiel (ohne 11m)",pergame = True))
    elif option == "Schüsse":
           st.pyplot(hbar(df,"shots.Sh","Schüsse pro Spiel",pergame = True))
    elif option == "Schüsse aufs Tor":
           st.pyplot(hbar(df,"shots.SoT","Schüsse aufs Tor pro Spiel",pergame = True))
    elif option == "Abseits":
           st.pyplot(hbar(df,'pt.Outcomes.Off',"Ins Abseits gelaufen (ganze Saison)",pergame = False))
    elif option == "Dribblings":
           st.pyplot(hbar(df,'poss.Take-Ons.Succ',"Erfolgreiche Dribblings pro Spiel",pergame = True))
           st.caption("Ein erfolgreiches Dribbling ist gleichbedeutend mit einem Gegenspieler, der ausgedribbelt wurde.")
    elif option == "Standardtore":
           st.pyplot(hbar(df,'creation.GCA Types.PassDead',"Tore nach Standardsituationen (ohne 11m)",pergame = False))
           
with tab2:
    option = st.selectbox("",options=["Gegentore",
                                      "Expected Goals against pro Spiel",
                                      "Fehler",
                                      "Abseits",
                                      "Standardtore"])
    if option == "Gegentore":
           st.pyplot(hbar(df,"GA","Gegentore"))
    elif option == "Expected Goals against pro Spiel":
           st.pyplot(hbar(df,"xGA","Expected Goals against pro Spiel",pergame = True))
    elif option == "Fehler":
           st.pyplot(hbar(df,"defense.Err","Fehler",pergame = False))    
           st.caption("Individuelle Fehler, die zu einer Torchance geführt haben")
    elif option == "Abseits":
           st.pyplot(hbar(df,'pt.ag.Outcomes.Off',"Gegner ins Abseits gestellt (ganze Saison)",pergame = False))
    elif option == "Standardtore":
           st.pyplot(hbar(df,'creation.ag.GCA Types.PassDead',"Gegentore nach Standardsituationen (ohne 11m)",pergame = False))    
with tab3:
    option = st.selectbox("",options=["Passgenauigkeit",
                                      "Pässe pro Spiel",
                                      "Ballbesitz",
                                      "Lange Bälle",
                                      "Flanken"])
    if option == "Passgenauigkeit":
           st.pyplot(hbar(df,"passing.Total.Cmp%","Angekommene Pässe (in %)"))
    elif option == "Ballbesitz":
           st.pyplot(hbar(df,"Poss","durchschnittlicher Ballbesitz (in %)",pergame = False))
    elif option == "Lange Bälle":
           st.pyplot(hbar(df,"passing.LongPct","Anteil langer Bälle an allen Pässen (in %)",pergame = False))
           st.caption("Pässe über eine Distanz von mehr als 32 Metern")
    elif option == "Flanken":
           st.pyplot(hbar(df,"pt.Pass Types.Crs","Flanken pro Spiel",pergame = True))
    elif option == "Pässe pro Spiel":
           st.pyplot(hbar(df,"passing.Total.Att","Pässe pro Spiel",pergame = True))
           st.caption("Gesamtzahl aller erfolgreichen und erfolglosen Pässe pro Spiel")
with tab4:
    option = st.selectbox("",options=["Zuschauer"])
    if option == "Zuschauer":
           st.pyplot(hbar(df,"Attendance","Zuschauerschnitt bei Heimspielen",pergame = False))

           
    
st.divider()
#   st.subheader("Zweidimensionale Statistiken",divider = "rainbow")
option = st.selectbox("", options = ['Schüsse',
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