import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('Manchester City Football Club Management Decision Support System')

st.markdown("""
Project of Decision Support System course\n
by\n
Ly Minh Trung\n
Kieu Chi Huy\n
Truong Quoc An
""")

st.sidebar.header('Squad Selection')
# Sidebar - Position selection
unique_pos = playerstats["Pos"].tolist()
selected_pos = st.sidebar.multiselect('Posision', unique_pos, unique_pos)


@st.cache
def load_data():
    url = "https://fbref.com/en/squads/b8fd03ef/Manchester-City-Stats"
    html = pd.read_html(url, header = 1)
    playerstats = html[0]
   
    playerstats.drop(playerstats.tail(2).index, inplace = True)
    playerstats["Nation"] = playerstats["Nation"].str.replace('[a-z]', '')
    return playerstats
playerstats = load_data()

unique_nation = playerstats["Nation"].tolist()
selected_nation = st.sidebar.multiselect('Nation', unique_nation, unique_nation)

df_selected_position = playerstats[(playerstats.Pos.isin(selected_pos))] 

df_selected_nation = playerstats[(playerstats.Pos.isin(selected_pos)) & (playerstats.Nation.isin(selected_nation))]


st.header("Information of Manchester City's Players")
st.write('Data Dimension: ' + str(playerstats.shape[0]) + ' rows and ' + str(playerstats.shape[1]) + ' columns.')
st.dataframe(playerstats)


# button
if st.button('View Players by Position'):
    st.header('Players by Position')
    st.write('Data Dimension: ' + str(df_selected_position.shape[0]) + ' rows and ' + str(df_selected_position.shape[1]) + ' columns.')

    st.dataframe(df_selected_position) 
    
if st.button('View Players by Nation'):
    st.header('Players by Nation')
    st.write('Data Dimension: ' + str(df_selected_nation.shape[0]) + ' rows and ' + str(df_selected_nation.shape[1]) + ' columns.')

    st.dataframe(df_selected_nation) 
