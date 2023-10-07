# -*- coding: utf-8 -*-
import streamlit as st
#%% TatsÃ¤chliches Dashboard
st.set_page_config(
    page_title="Start",
    page_icon="🏠"
)

st.write("# Willkommen auf Volkers zweitklassigem Fußball-Dashboard!")

st.sidebar.success("Wähle aus der Liste oben den Punkt aus, den Du Dir anschauen möchtest!")

st.markdown(
    """
    In dieser App finden sich unterschiedlichste Statistiken zur zweiten Fußball-Bundesliga. Das ganze ist ein großes Übungs- und Spaßprojekt. 
    Sämtliche genutzte Daten kommen von [fbref.com](https://fbref.com/en/comps/33/2-Bundesliga-Stats/).
    In der Liste links kannst du zwischen verschiedenen Punkten auswählen - von einfachen Übersichten bis
    zu interaktiven Darstellungen.\\
    Die App wurde mithilfe des Python-Pakets [*Streamlit*](https.streamlit.io) erstellt. Optimiert ist sie für die Nutzung im Browser an einem Computer.
    Sie funktioniert auch auf dem Smartphone, manche Darstellungen sind unter Umständen nicht optimal. 
    An einigen Stellen kann über einen Regler die Smartphone-Version aktiviert werden.
    """
    )
