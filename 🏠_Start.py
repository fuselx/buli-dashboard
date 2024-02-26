# -*- coding: utf-8 -*-
import streamlit as st
st.set_page_config(layout="wide")

    
# Höhe der Sidebar-Liste anpassen
st.sidebar.markdown("""
                    <style> [data-testid='stSidebarNav'] > ul { min-height: 60vh; } </style> 
                    """, unsafe_allow_html=True)
#%% Tatsächliches Dashboard
col1,col2,col3 = st.columns((1,3.5,1))
with col2:
    st.write("# Willkommen auf Volkers zweitklassigem Fußball-Dashboard!")
    
    
    
    st.markdown(
        """
        In dieser App finden sich unterschiedlichste Informationen zur zweiten Fußball-Bundesliga. Zwischen diesen kannst du in der Leiste links auswählen.
        Neben der Tabelle und Spielplänen findest du aufbereitete Daten und Statistiken, mit denen die Leistungen und Spielweisen der Teams 
        analysiert werden können. 
        """
        )
    
    st.image("https://raw.githubusercontent.com/fuselwolga/buli-dashboard/main/Aufstieg_2002.jpg")
    st.caption("Symbolbild")
    with st.expander("Weitere Infos"):
        st.markdown(
            """
            Sämtliche genutzte Daten kommen von [fbref.com](https://fbref.com/en/comps/33/2-Bundesliga-Stats/) und sind mit einer Verzögerung von ca. einem Tag aktuell.\\
            Die App wurde mithilfe des Python-Pakets [*Streamlit*](https.streamlit.io) erstellt. Optimiert ist sie für die Nutzung im Browser.
            """)
