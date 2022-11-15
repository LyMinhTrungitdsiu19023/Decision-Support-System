import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from PIL import Image
st.set_page_config(layout = 'wide')
image = Image.open('logo.jpg')

st.image(image, caption='The Citizen', width=1000)

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

 
def Analysis(url):
    #Forward
    data = pd.read_html(url, header = 1)
    

    
    #Shoot
    shoot = data[4]
    shoot.drop(shoot.tail(2).index, inplace = True)
    shoot["Nation"] = shoot["Nation"].str.replace('[a-z]', '')
    shoot = shoot.drop(['SoT%', 'Sh/90', 'SoT/90', 'G/SoT', 'Dist', 'xG', 'npxG', 'npxG/Sh', 'G-xG', 'np:G-xG', 'Matches'], axis=1)
    shoot.rename(columns = {'Gls':'Goals', 'Sh':'Shots total', 'SoT':'Shots on Target', 'G/Sh':'Goal per Shot', 'FK':'Freekick','PK':'Penalty Kick','PKatt':'Pentallty Attemp'}, inplace = True)
    shoot = shoot.reset_index(drop = True) 
    
    #Pass
    passing = data[5]
    passing.drop(passing.tail(2).index, inplace = True)
    passing["Nation"] = passing["Nation"].str.replace('[a-z]', '')
#     passing = passing.drop(['xA', 'A-xA', 'KP', '1/3', 'PPA', 'CrsPA', 'Prog','Matches', 'TotDist', 'PrgDist'], axis=1)
    passing.rename(columns = {'Cmp':'Passed Completed', 'Att':'Passes Attempted', 'Cmp%':'%Completed'}, inplace = True)
    passing = passing.reset_index(drop = True)
    

    
    #Defend
    df = data[5]
    df.drop(df.tail(2).index, inplace = True)
    df["Nation"] = df["Nation"].str.replace('[a-z]', '')
    df = df.drop(['Matches'], axis=1)
#     fw_df.rename(fw_df = {'Cmp':'Passed Completed', 'Att':'Passes Attempted', 'Cmp%':'%Completed'}, inplace = True)
    df = df.reset_index(drop = True)
 
    
    return shoot, passing, df
 
def Analysis_Forward(url):
    st.header('Analysis of Forward')
    


    shoot = Analysis(url)[0]
    shoot = shoot.loc[shoot["Pos"].str.contains("FW")]
    st.write('Stats of Shooting')
    st.dataframe(shoot)

    passing = Analysis(url)[1]
    passing = passing.loc[passing["Pos"].str.contains("FW")]
    st.write('Stats of Passing')
    st.dataframe(passing) 
    st.write('*Note\n Cmp.1: Passes Completed in Short Distance - Att.1 Passes Attempted in Short Distance - Cmp%.1: % Passes Completed in Short Distance - .2: Medium Distance - .3:Long Distance')

    df = Analysis(url)[2]
    df = df.loc[df["Pos"].str.contains("FW")]
    st.write('Stats of Defensive')
    st.dataframe(df)
    
def Analysis_Mid(url):
    st.header('Analysis of Midfield')


    shoot = Analysis(url)[0]
    shoot = shoot.loc[shoot["Pos"].str.contains("MF")]
    st.write('Stats of Shooting')
    st.dataframe(shoot)

    passing = Analysis(url)[1]
    passing = passing.loc[passing["Pos"].str.contains("MF")]
    st.write('Stats of Passing')
    st.dataframe(passing) 
    st.write('*Note\n Cmp.1: Passes Completed in Short Distance - Att.1 Passes Attempted in Short Distance - Cmp%.1: % Passes Completed in Short Distance - .2: Medium Distance - .3:Long Distance')

    df = Analysis(url)[2]
    df = df.loc[df["Pos"].str.contains("MF")]
    st.write('Stats of Defensive')
    st.dataframe(df)
    
    
def Analysis_defend(url):
    st.header('Analysis of Defensive')


    shoot = Analysis(url)[0]
    shoot = shoot.loc[shoot["Pos"].str.contains("DF")]
    st.write('Stats of Shooting')
    st.dataframe(shoot)

    passing = Analysis(url)[1]
    passing = passing.loc[passing["Pos"].str.contains("DF")]
    st.write('Stats of Passing')
    st.dataframe(passing) 
    st.write('*Note\n Cmp.1: Passes Completed in Short Distance - Att.1 Passes Attempted in Short Distance - Cmp%.1: % Passes Completed in Short Distance - .2: Medium Distance - .3:Long Distance')

    df = Analysis(url)[2]
    df = df.loc[df["Pos"].str.contains("DF")]
    st.write('Stats of Defensive')
    st.dataframe(df) 

# def chart_analysis_information_goal(attr, playerstats):
#     if attr == "Goal":
#         goal_df = playerstats.sort_values(by='Gls', ascending=False)
#         goal_df = goal_df.head(10)
        
#     return goal_df
def plot_chart(attr, url):
    playerstats = load_data(url)
    rc = {'figure.figsize':(8,4.5),
      'axes.facecolor':'#0e1117',
      'axes.edgecolor': '#0e1117',
      'axes.labelcolor': 'white',
      'figure.facecolor': '#0e1117',
      'patch.edgecolor': '#0e1117',
      'text.color': 'white',
      'xtick.color': 'white',
      'ytick.color': 'white',
      'grid.color': 'grey',
      'font.size' : 8,
      'axes.labelsize': 12,
      'xtick.labelsize': 8,
      'ytick.labelsize': 12}
    plt.rcParams.update(rc)
    fig, ax = plt.subplots()
    
    
    if attr == "Goal":

        goal_df = playerstats.sort_values(by='Gls', ascending=False)
        goal_df = goal_df.head(10)
        goal_df_1 = pd.DataFrame()
        goal_df_1 = goal_df[["Player", "Gls"]]
        ax = sns.barplot(x = goal_df_1["Player"], y = goal_df_1["Gls"], data=goal_df_1.reset_index(), color = "#b80606")
        ax.set(xlabel = "Player", ylabel = "Goal")
        plt.xticks(rotation=66,horizontalalignment="right")
        st.pyplot(fig)
#         return goal_df_1
    
#button 
# if st.button('Squad Analysis'):
fw = st.checkbox("Analysis of Forward")
mf = st.checkbox("Analysis of Midfield")
df = st.checkbox("Analysis of Defensive")
if fw:   
    Analysis_Forward(url)
if mf:
    Analysis_Mid(url) 
if df:
    Analysis_defend(url) 
    
# analysis_bar = st.expander("Analysis Information")
st.header('Analysis Information')

row_wordx, row_wordy = st.columns((3.4, 2.3))
row_chartx, row_charty = st.columns((.2, 3))
# with analysis_bar: 
with row_wordy:
    st.markdown('Investigate a variety of stats for each player. Which player scores the most goals, assist or pass? How does players compare with each others?')
    select_attr = st.selectbox('Which attribute do you want to analyze?', ('Goal','Assist','Goal per Shots','Passed Completed','Age'))
#     st.selectbox('Which measure do you want to analyze?', ('Mean','Median','Absolute','Maximum','Minimum'))
with row_charty:
#     st.dataframe(plot_chart(select_attr))
    plot_chart(select_attr, url)
