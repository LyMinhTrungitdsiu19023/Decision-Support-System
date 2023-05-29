import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import spatial
from ratelimit import limits
import requests
from PIL import Image
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import time 
from Squad import *
from Analysis import *
from Transfer import *

    
##################################################################################################################################################################################################3
###Build GUI / Interface of the Web App

st.set_page_config(page_title="Manchester City Decision Support System", layout = 'wide')

# image = Image.open('squad2223.jpg')
image = Image.open('stadium.jpg')

st.image(image, caption='The Citizen', width=1400)


st.title("Manchester City Football Club Management System")


st.markdown("""
_Project of Information System Management course_\n
_by_\n
**Ly Minh Trung - Kieu Chi Huy - Truong Thai Ngoc Toan - Nguyen Dao Trung Hieu - Nguyen Anh Tuan**
""")

with open('Authen.yaml') as file:
    config = yaml.load(file,Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )
name, authenticator_status, username = authenticator.login('Login', 'main')
if authenticator_status == False:
    warn_error = st.error('Username/password is incorrect')
    time.sleep(1)
    warn_error.empty()

if authenticator_status == None:
    warn_missing = st.warning('Please enter your username and password')
    time.sleep(3)
    warn_missing.empty()

if authenticator_status:
    authenticator.logout("Log out","sidebar")
    
    see_data = st.expander("Information of Manchester City's Players 👉")
    with see_data: 
        st.header("Information of Manchester City's Players")
#         st.write('Data Dimension: ' + str(load_data(url)[0].shape[0]) + ' rows and ' + str(load_data(url)[0].shape[1]) + ' columns.')
        st.dataframe(load_data(url)[0])


    see_nation = st.expander("Players by Nation 👉")
    with see_nation: 
        st.header('Players by Nation')
        unique_nation = load_data(url)[0]["Nation"].tolist()
        selected_nation = st.selectbox('Nation', (unique_nation))
        df_selected_nation = load_data(url)[0].loc[load_data(url)[0]["Nation"].str.contains(selected_nation)]  
        st.dataframe(df_selected_nation) 


    see_pos = st.expander("Players by Posision 👉") 
    with see_pos: 
        st.header('Players by Position')
        unique_pos = load_data(url)[0]["Pos"].drop_duplicates().tolist()
        selected_pos = st.selectbox('Posision',('GK', 'DF', 'MF', 'FW'))
        df_selected_position = load_data(url)[0].loc[load_data(url)[0]["Pos"].str.contains(selected_pos)]
        st.dataframe(df_selected_position) 

    fw = st.checkbox("Statistics of Forward")
    mf = st.checkbox("Statistics of Midfield")
    df = st.checkbox("Statistics of Defensive")
    if fw:   
        Analysis_Forward(url)
    if mf:
        Analysis_Mid(url) 
    if df:
        Analysis_defend(url) 

    st.header('Analysis Information')

    row_wordx, row_wordy = st.columns((3.4, 2.3))
    row_chartx, row_charty = st.columns((.2, 3))

    with row_wordy:
        st.markdown('Investigate a variety of stats for each player. Top 10 players who score the most goals, assist, pass, or mistakes? How does players compare with each others?')
        select_attr = st.selectbox('Which attribute do you want to analyze?', ('Goal','Assist','Playing time','Tackle Completed','Number of Tackled','Done Intercept','Number of Touches','Number of Touches in attacking area','Mistakes lead to goals','Goal per 90Mins','Passed per 90Mins', 'Total Yellow Cards', 'Total Red Cards', 'Total Penalty Goals'))

    with row_wordx:
        plot_chart(select_attr, url)

    st.header("Expected Information of the player")

    see_predict_table = st.expander("Show prediction table 👉")
    with see_predict_table: 
        st.dataframe(prediction(url), width=2500, height=400)


    see_predict_chart = st.expander("Show prediction Chart 👉")
    with see_predict_chart:
        st.markdown('Investigate a variety of prediction for each player. Top 10 players who predicted to score the most goals, assist, pass, or mistakes? How does players compare with each others?')
        select_pre = st.selectbox('Which attribute do you want to see prediction?', ('Expected Goals','Expected Assists'))
        prediction_chart(select_pre)




    menu = st.sidebar.selectbox("Menu", ("Squad", "Transfer"))

    if menu == "Squad":
        st.sidebar.header('PlayStyle') 
        st.sidebar.markdown('Coach choose the requirements here') 

        selected_squad = st.sidebar.selectbox('Squad',('4-4-2', '4-2-3-1', '4-3-3'))
        selected_speed = st.sidebar.select_slider('Speed', options = [1,2,3,4])
        selected_intercept = st.sidebar.select_slider('Intercept', options = [1,2,3,4])
        selected_style = st.sidebar.selectbox('Style',('Organizing', 'Liberal')) 
        selected_squad_distance = st.sidebar.selectbox('Squad distance',('Narrow', 'Wide')) 
        selected_match_approach = st.sidebar.selectbox('Match approach',('Defend', 'Attack', 'Possesion')) 
        selected_gk = st.sidebar.selectbox('Select GoalKkeeper',load_data(url)[0].loc[load_data(url)[0]["Pos"].str.contains('GK')]) 
        st.header("Squad Recommendation")
        st.markdown('Please, Select attributes in Squad sidebar')
        if st.sidebar.button('Recommendations squad for the next match'):
            st.dataframe(recommendation(url, selected_squad, selected_speed, selected_intercept, selected_style, selected_squad_distance, selected_match_approach, selected_gk))

    if menu == "Transfer":
        st.sidebar.markdown("Recommend the most similar with your selection player")
        radio = st.sidebar.radio('Player type', ['Outfield players', 'Goal Keepers']) 

        if radio == "Goal Keepers":
            player_name = st.sidebar.selectbox('Player',load_data(url)[0].loc[load_data(url)[0]["Pos"] == "GK"]["Player"])
        else:
            player_name = st.sidebar.selectbox('Player',load_data(url)[0][load_data(url)[0]["Pos"].str.contains("GK") == False]["Player"])

        league = st.sidebar.selectbox('League', ["All", "Premier League", "Bundesliga","La Liga", "Ligue 1", "Serie A"]) 



        st.header("Player Recommender")
        st.markdown('Please, Select attributes in Transfer sidebar')
        see_data = st.expander("Information of Players in Big 5 European Leagues 👉")
        with see_data: 
            st.header("Information of Players in Big 5 European Leagues")
            select_player = st.selectbox("Player's name",get_data(url_transfer)["Player"], help = "You can type the name to see the suggestion")

            df_select_player = get_data(url_transfer).loc[get_data(url_transfer)["Player"].str.contains(select_player)]
            st.dataframe(df_select_player)

        see_data = st.expander("Showing Recommended Players 👉")
        if st.sidebar.button('## Find players ##'):
            with see_data:
                if filter_player_by_sidebar(url, url_transfer, url_defend,url_gk, player_name, league, radio).empty:
                    st.markdown("_No recommended players for_ **{}**".format(player_name))
                else:
                    st.markdown("_Top recommended players for_ **{}**".format(player_name))
                    st.dataframe(filter_player_by_sidebar(url, url_transfer, url_defend,url_gk, player_name, league, radio))


