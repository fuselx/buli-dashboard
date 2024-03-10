import streamlit as st

st.set_page_config(layout="centered")

from pages.prep import data_stats
from pages.prep import plots


# Höhe der Sidebar-Liste anpassen
st.sidebar.markdown("""
                    <style> [data-testid='stSidebarNav'] > ul { min-height: 60vh; } </style> 
                    """, unsafe_allow_html=True)
                    

#%% Tabellen einlesen
df = data_stats.load_data()


#%% Dashboard
st.subheader("Teamvergleich",divider = "rainbow")
st.markdown("""
            Hier kann aus unterschiedlichen Statistiken ausgewählt werden. Oben finden sich eindimensionale Rankings, unten zweidimensionale Darstellungen.
            """)
tab1,tab2,tab3,tab4 = st.tabs(["Offensiv","Defensiv","Passspiel","Sonstiges"])

with tab1:
    option = st.selectbox("",options=["Tore",
                                      "Schüsse",
                                      "Schüsse aufs Tor",
                                      "Expected Goals pro Spiel",
                                      "Expected Goals pro Spiel (ohne 11m)",
                                      "Ballkontakte im letzten Drittel",
                                      "Abseits",
                                      "Dribblings",
                                      "Standardtore"])
    if option == "Tore":
           st.pyplot(plots.hbar(df,"GF","Geschossene Tore"))
    elif option == "Expected Goals pro Spiel":
           st.pyplot(plots.hbar(df,"shots.xG","Expected Goals pro Spiel",pergame = True))
    elif option == "Expected Goals pro Spiel (ohne 11m)":
           st.pyplot(plots.hbar(df,"shots.npxG","Expected Goals pro Spiel (ohne 11m)",pergame = True))
    elif option == "Schüsse":
           st.pyplot(plots.hbar(df,"shots.Sh","Schüsse pro Spiel",pergame = True))
    elif option == "Schüsse aufs Tor":
           st.pyplot(plots.hbar(df,"shots.SoT","Schüsse aufs Tor pro Spiel",pergame = True))
    elif option == "Ballkontakte im letzten Drittel":
           st.pyplot(plots.hbar(df,"poss.Touches.Att 3rd","Ballkontakte im offensiven Drittel pro Spiel", pergame = True))
    elif option == "Abseits":
           st.pyplot(plots.hbar(df,'pt.Outcomes.Off',"Ins Abseits gelaufen (ganze Saison)",pergame = False))
    elif option == "Dribblings":
           st.pyplot(plots.hbar(df,'poss.Take-Ons.Succ',"Erfolgreiche Dribblings pro Spiel",pergame = True))
           st.caption("Ein erfolgreiches Dribbling ist gleichbedeutend mit einem Gegenspieler, der ausgedribbelt wurde.")
    elif option == "Standardtore":
           st.pyplot(plots.hbar(df,'creation.GCA Types.PassDead',"Tore nach Standardsituationen (ohne 11m)",pergame = False))
           
with tab2:
    option = st.selectbox("",options=["Gegentore",
                                      "Expected Goals against pro Spiel",
                                      "Individuelle Fehler",
                                      "Fehler provoziert",
                                      "Abseits",
                                      "Standardtore"])
    if option == "Gegentore":
           st.pyplot(plots.hbar(df,"GA","Gegentore"))
    elif option == "Expected Goals against pro Spiel":
           st.pyplot(plots.hbar(df,"xGA","Expected Goals against pro Spiel",pergame = True))
    elif option == "Individuelle Fehler":
           st.pyplot(plots.hbar(df,"defense.Err","Individuelle Fehler",pergame = False))    
           st.caption("Individuelle Fehler, die zu einer Torchance geführt haben")
    elif option == "Fehler provoziert":
           st.pyplot(plots.hbar(df,"defense.ag.Err","Fehler provoziert",pergame = False)) 
           st.caption("Individuelle Fehler, die zu einer Torchance geführt haben")
    elif option == "Abseits":
           st.pyplot(plots.hbar(df,'pt.ag.Outcomes.Off',"Gegner ins Abseits gestellt (ganze Saison)",pergame = False))
    elif option == "Standardtore":
           st.pyplot(plots.hbar(df,'creation.ag.GCA Types.PassDead',"Gegentore nach Standardsituationen (ohne 11m)",pergame = False))    
with tab3:
    option = st.selectbox("",options=["Passgenauigkeit",
                                      "Pässe pro Spiel",
                                      "Ballbesitz",
                                      "Lange Bälle",
                                      "Flanken"])
    if option == "Passgenauigkeit":
           st.pyplot(plots.hbar(df,"passing.Total.Cmp%","Angekommene Pässe (in %)"))
    elif option == "Ballbesitz":
           st.pyplot(plots.hbar(df,"Poss","durchschnittlicher Ballbesitz (in %)",pergame = False))
    elif option == "Lange Bälle":
           st.pyplot(plots.hbar(df,"passing.LongPct","Anteil langer Bälle an allen Pässen (in %)",pergame = False))
           st.caption("Pässe über eine Distanz von mehr als 32 Metern")
    elif option == "Flanken":
           st.pyplot(plots.hbar(df,"pt.Pass Types.Crs","Flanken pro Spiel",pergame = True))
    elif option == "Pässe pro Spiel":
           st.pyplot(plots.hbar(df,"passing.Total.Att","Pässe pro Spiel",pergame = True))
           st.caption("Gesamtzahl aller erfolgreichen und erfolglosen Pässe pro Spiel")
with tab4:
    option = st.selectbox("",options=["Zuschauer",
                                      "Gelbe Karten",
                                      "Rote Karten"])
    if option == "Zuschauer":
           st.pyplot(plots.hbar(df,"Attendance","Zuschauerschnitt bei Heimspielen",pergame = False))
    elif option == "Gelbe Karten":
           st.pyplot(plots.hbar(df,"misc.Performance.CrdY","Gelbe Karten",pergame = False))
    elif option == "Rote Karten":
           st.pyplot(plots.hbar(df,"misc.Performance.CrdR","Rote Karten",pergame = False))
           
    
st.divider()
#   st.subheader("Zweidimensionale Statistiken",divider = "rainbow")
tab10,tab20,tab30,tab40,tab50 = st.tabs(["Offensiv","Defensiv","Passspiel","xG","Sonstiges"])
with tab10:
    option = st.selectbox("", options = ['Schüsse',
                                         'Ballbesitz vs. Kontakte im Strafraum',
                                         "Offensivstandards"])
    if option == "Schüsse":
           st.pyplot(plots.scatter(df,"shots.Sh/90","shots.SoT/90",
                             title = "Schüsse (aufs Tor)",xlab = "Schüsse pro Spiel",ylab = "Schüsse aufs Tor pro Spiel"))
    if option == "Ballbesitz vs. Kontakte im Strafraum":
           st.pyplot(plots.scatter(df,"Poss","poss.Touches.Att Pen",pergame = "y",
                             title = "Ballbesitz",xlab = "Ballbesitz insgesamt",ylab = "Ballkontakte im Strafraum (pro Spiel)"))
    if option == "Offensivstandards":
           st.pyplot(plots.scatter(df,"creation.SCA Types.PassDead","creation.GCA Types.PassDead",
                             title = "Offensivstandards",xlab = "Chancen nach Standardsituationen",ylab = "Tore nach Standardsituationen"))
           
with tab20:
    option = st.selectbox("", options = ["Pressing offensiv",
                                         "Pressing defensiv"])
    if option == "Pressing offensiv":
           st.pyplot(plots.scatter(df,"defense.Tackles.Mid 3rd.Pct","defense.Tackles.Att 3rd.Pct",
                             title = "Tacklings in Mittelfeld und Sturm (% aller Tacklings)",xlab = "Tacklings Mittelfeld",ylab = "Tacklings Angriffsdrittel"))           
    if option == "Pressing defensiv":
           st.pyplot(plots.scatter(df,"defense.Tackles.Mid 3rd.Pct","defense.Tackles.Def 3rd.Pct",
                             title = "Tacklings in Mittelfeld Abwehr (% aller Tacklings)",xlab = "Tacklings Mittelfeld",ylab = "Tacklings Abwehrdrittel"))       
with tab30:
    option = st.selectbox("", options = ["Pässe", 
                                            "Kurzpässe",
                                            "Mittellange Pässe",
                                            "Lange Bälle",
                                            "Lange Bälle und Flanken"])
    if option == "Pässe":
           st.pyplot(plots.scatter(df,"passing.Total.Att","passing.Total.Cmp%", pergame = "x",
                             title = "Passgenauigkeit",xlab = "Gespielte Pässe pro Spiel",ylab = "Angekommene Pässe (in %)"))
    if option == "Kurzpässe":
            st.pyplot(plots.scatter(df,"passing.Short.Att","passing.Short.Cmp%", pergame = "x",
                                 title = "Passgenauigkeit Kurzpässe",xlab = "Gespielte Pässe pro Spiel",ylab = "Angekommene Pässe (in %)"))
            st.caption("Kurzpässe: Pässe zwischen 5 und 16 Metern (5/15 Yards)")
    if option == "Mittellange Pässe":
           st.pyplot(plots.scatter(df,"passing.Medium.Att","passing.Medium.Cmp%", pergame = "x",
                             title = "Passgenauigkeit mittellange Pässe",xlab = "Gespielte Pässe pro Spiel",ylab = "Angekommene Pässe (in %)"))
           st.caption("Mittellange Pässe: Pässe zwischen 16 und 32 Metern (15/30 Yards)")
    if option == "Lange Bälle":
           st.pyplot(plots.scatter(df,"passing.Long.Att","passing.Long.Cmp%", pergame = "x",
                             title = "Passgenauigkeit lange Bälle",xlab = "Gespielte Bälle pro Spiel",ylab = "Angekommene Bälle (in %)"))
           st.caption("Lange Bälle: Pässe über eine Strecke von mindesten 32 Metern (30 Yards)")
    if option == "Lange Bälle und Flanken":
           st.pyplot(plots.scatter(df,"passing.Long.Att","pt.Pass Types.Crs", pergame = "xy",
                             title = "Lange Bälle und Flanken (pro Spiel)",xlab = "Lange Bälle",ylab = "Flanken"))
with tab40:
    option = st.selectbox("", options= ['Expected Goals',
                                        'Tordifferenz vs. xG'])
    if option == "Expected Goals":
           st.pyplot(plots.scatter(df,"shots.xG","shots.ag.xG",pergame = "xy",
                             title = "Expected Goals (pro Spiel)",xlab = "Expected Goals",ylab = "Expected Goals against"))
    if option == "Tordifferenz vs. xG":
           st.pyplot(plots.scatter(df,"xGD","GD",
                             title = "Tordifferenz erwartet vs. tatsächlich",xlab = "Tordifferenz erwartet",ylab = "Tordifferenz tatsächlich"))

with tab50:
    option = st.selectbox("", options= ["Fouls"])
    if option == "Fouls":
        st.pyplot(plots.scatter(df,"misc.Performance.Fls","misc.Performance.Fld", pergame = "xy",
                          title = "Fouls pro Spiel",xlab = "begangene Fouls",ylab = "vom Gegner begangene Fouls"))
