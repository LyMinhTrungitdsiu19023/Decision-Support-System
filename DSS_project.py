import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from PIL import Image

image = Image.open('logo.jpg')

st.image(image, caption='The Citizen')

st.title('Manchester City Football Club Management Decision Support System')

st.markdown("""
Project of Decision Support System course\n
by\n
Ly Minh Trung\n
Kieu Chi Huy\n
Truong Quoc An
""")

st.sidebar.header('Features')
# Sidebar - Position selection


url = "https://fbref.com/en/squads/b8fd03ef/Manchester-City-Stats"
@st.cache
def load_data(url):

    html = pd.read_html(url, header = 1)
    playerstats = html[0]
   
    playerstats.drop(playerstats.tail(2).index, inplace = True)
    playerstats["Nation"] = playerstats["Nation"].str.replace('[a-z]', '')
    return playerstats
playerstats = load_data(url)



see_data = st.expander("Information of Manchester City's Players 👉")
with see_data: 
    st.header("Information of Manchester City's Players")
    st.write('Data Dimension: ' + str(playerstats.shape[0]) + ' rows and ' + str(playerstats.shape[1]) + ' columns.')
    st.dataframe(playerstats)


see_nation = st.expander("Players by Nation 👉")
with see_nation: 
    st.header('Players by Nation')
    unique_nation = playerstats["Nation"].tolist()
    selected_nation = st.selectbox('Nation', (unique_nation))

    df_selected_nation = playerstats.loc[playerstats["Nation"].str.contains(selected_nation)]  
    st.dataframe(df_selected_nation) 



see_pos = st.expander("Players by Posision 👉") 
with see_pos: 

    st.header('Players by Position')

    unique_pos = playerstats["Pos"].drop_duplicates().tolist()
    selected_pos = st.selectbox('Posision',('GK', 'DF', 'MF', 'FW'))
    df_selected_position = playerstats.loc[playerstats["Pos"].str.contains(selected_pos)]
    st.dataframe(df_selected_position) 


selected_squad = st.sidebar.selectbox('Squad',('4-4-2', '4-2-3-1', '4-3-3'))

 
#button 
if st.button('Squad Suggestion'):
  
    st.header('Analysis of Forward')
    fw = pd.read_html(url, header = 1)
    fw_table = fw[4]
    fw_table.drop(fw_table.tail(2).index, inplace = True)
    fw_table = fw_table.loc[fw_table["Pos"].str.contains("FW")]
    fw_table["Nation"] = fw_table["Nation"].str.replace('[a-z]', '')
    fw_table = fw_table.reset_index(drop = True)
    st.write('Stats of strikers')
    st.dataframe(fw_table) 
    
    
 
