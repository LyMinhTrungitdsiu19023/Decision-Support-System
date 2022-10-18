import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from PIL import Image

image = Image.open('logo.jpg')

st.image(image, caption='The Citizen', width=None)

st.title('Manchester City Football Club Management Decision Support System')

st.markdown("""
Project of Decision Support System course\n
by\n
Ly Minh Trung - Kieu Chi Huy - Truong Quoc An
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

 
def Analysis_Forward(url):
    #Forward
    st.header('Analysis of Forward')
    fw = pd.read_html(url, header = 1)
    

    
    #Shoot
    fw_shoot = fw[4]
    fw_shoot.drop(fw_shoot.tail(2).index, inplace = True)
    fw_shoot = fw_shoot.loc[fw_shoot["Pos"].str.contains("FW")]
    fw_shoot["Nation"] = fw_shoot["Nation"].str.replace('[a-z]', '')
    fw_shoot = fw_shoot.drop(['SoT%', 'Sh/90', 'SoT/90', 'G/SoT', 'Dist', 'xG', 'npxG', 'npxG/Sh', 'G-xG', 'np:G-xG', 'Matches'], axis=1)
    fw_shoot.rename(columns = {'Gls':'Goals', 'Sh':'Shots total', 'SoT':'Shots on Target', 'G/Sh':'Goal per Shot', 'FK':'Freekick','PK':'Penalty Kick','PKatt':'Pentallty Attemp'}, inplace = True)
    fw_shoot = fw_shoot.reset_index(drop = True)
    st.write('Stats of Shooting')
    st.dataframe(fw_shoot) 
    
    #Pass
    fw_pass = fw[5]
    fw_pass.drop(fw_pass.tail(2).index, inplace = True)
    fw_pass = fw_pass.loc[fw_pass["Pos"].str.contains("FW")]
    fw_pass["Nation"] = fw_pass["Nation"].str.replace('[a-z]', '')
    fw_pass = fw_pass.drop(['xA', 'A-xA', 'KP', '1/3', 'PPA', 'CrsPA', 'Prog','Matches', 'TotDist', 'PrgDist'], axis=1)
    fw_pass.rename(columns = {'Cmp':'Passed Completed', 'Att':'Passes Attempted', 'Cmp%':'%Completed'}, inplace = True)
    fw_pass = fw_pass.reset_index(drop = True)
    st.write('Stats of Passing')
    st.dataframe(fw_pass) 
    st.write('*Note\n Cmp.1: Passes Completed in Short Distance - Att.1 Passes Attempted in Short Distance - Cmp%.1: % Passes Completed in Short Distance - .2: Medium Distance - .3:Long Distance')

    
    #Defend
    fw_df = fw[5]
    fw_df.drop(fw_df.tail(2).index, inplace = True)
    fw_df = fw_df.loc[fw_df["Pos"].str.contains("FW")]
    fw_df["Nation"] = fw_df["Nation"].str.replace('[a-z]', '')
    fw_df = fw_df.drop(['Matches'], axis=1)
#     fw_df.rename(fw_df = {'Cmp':'Passed Completed', 'Att':'Passes Attempted', 'Cmp%':'%Completed'}, inplace = True)
    fw_df = fw_df.reset_index(drop = True)
    st.write('Stats of Defensive')
    st.dataframe(fw_df) 
    
#button 
if st.button('Squad Suggestion'):
  Analysis_Forward(url)

