# -*- coding: utf-8 -*-
import streamlit as st
st.set_page_config(layout="centered")
#%% Tatsächliches Dashboard
st.write("# Willkommen auf Volkers zweitklassigem Fußball-Dashboard!")

st.sidebar.success("Wähle aus der Liste oben den Punkt aus, den Du Dir anschauen möchtest!")
mobile_on = st.sidebar.toggle("Smartphone-Version", key = "mobile_on")
if "mobile_on" not in st.session_state:
    st.session_state.mobile_on = False

st.markdown(
    """
    In dieser App finden sich unterschiedlichste Statistiken zur zweiten Fußball-Bundesliga. Das Ganze ist ein großes Übungs- und Spaßprojekt. 
    Sämtliche genutzte Daten kommen von [fbref.com](https://fbref.com/en/comps/33/2-Bundesliga-Stats/) und sind mit einer Verzögerung von ca. einem Tag aktuell.
    In der Liste links kannst du zwischen verschiedenen Punkten auswählen - von einfachen Übersichten bis
    zu interaktiven Darstellungen.\\
    Die App wurde mithilfe des Python-Pakets [*Streamlit*](https.streamlit.io) erstellt. Optimiert ist sie für die Nutzung im Browser an einem Computer.
    Sie funktioniert auch auf dem Smartphone, manche Darstellungen sind jedoch unter Umständen nicht optimal. 
    An einigen Stellen kann über einen Regler die Smartphone-Version aktiviert werden.
    """
    )

st.image("https://raw.githubusercontent.com/fuselwolga/buli-dashboard/main/Aufstieg_2002.jpg")
st.caption("Symbolbild")
