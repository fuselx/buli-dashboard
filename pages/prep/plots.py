# -*- coding: utf-8 -*-
import streamlit as st
import matplotlib.pyplot  as plt
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

from pages.prep import data_stats
df = data_stats.load_data()
images = data_stats.images()

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