import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('Manchester City Football Club\n Management Decision Support System')

st.markdown("""
This app is project of Decision Support System course\n
by\n
Ly Minh Trung\n
Kieu Chi Huy\n
Truong Quoc An
""")

st.sidebar.header('Squad Selection')
# Sidebar - Position selection
unique_pos = ['GK','DF','MF','FW']
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


df_selected_position= playerstats[(playerstats.Pos.isin(selected_pos))]

st.header("Information of Manchester City's Players")
st.write('Data Dimension: ' + str(playerstats.shape[0]) + ' rows and ' + str(playerstats.shape[1]) + ' columns.')
st.dataframe(playerstats)


# Heatmap
if st.button('View Players by Position'):
    st.header('Players by Position')
    st.write('Data Dimension: ' + str(df_selected_position.shape[0]) + ' rows and ' + str(df_selected_position.shape[1]) + ' columns.')

    st.dataframe(df_selected_position)
