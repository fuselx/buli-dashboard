# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

from pages.prep import data_matchdays




pd.options.mode.chained_assignment = None  # default='warn'


# Höhe der Sidebar-Liste anpassen
st.sidebar.markdown("""
                    <style> [data-testid='stSidebarNav'] > ul { min-height: 60vh; } </style> 
                    """, unsafe_allow_html=True)


md = data_matchdays.table_images()
#%% Dataframes formatieren


# Converting links to html tags
def path_to_image_html(path):
    return '<img src="' + path + '" width="25" >'

#convert df to html
def convert_df(input_df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return input_df.to_html(escape=False, formatters=dict(Heimlogo=path_to_image_html,Auswärtslogo=path_to_image_html))
 
#%%Dashboard  
col1,col2,col3 = st.columns((1,8,1))
with col2:
    st.subheader("Spielpläne einzelner Teams",divider = "rainbow")
     
    team = st.selectbox("Wähle das Team, dessen Spieplan du dir anschauen möchtest",options = md["Heim"].sort_values().unique(),index = 5)  
    if team == "Braunschweig":
        st.toast("😒")
    elif team == "Hannover 96":
        st.balloons()
    st.dataframe(md[(md['Heim'] == team)|(md["Auswärts"] == team)],
                        hide_index=True,
                        height = 1240,
                        column_order=("Spieltag","Tag","Datum","Anstoß","xG","Heimlogo","Ergebnis","Auswärtslogo","xG ","Zuschauer","Schiedsrichter"),
                        column_config={'Heimlogo':st.column_config.ImageColumn('Heim',width = "small"),
                                    'Auswärtslogo':st.column_config.ImageColumn('Auswärts',width = "small"),
                                    'xG':st.column_config.ProgressColumn(
                                        min_value=0,
                                        max_value=3.5,
                                        format = "  %f",
                                        width = "small"),
                                    'xG ':st.column_config.ProgressColumn(
                                        min_value=0,
                                        max_value=3.5,
                                        format = "  %f",
                                        width = "small")                                            
                                    })
