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

@st.cache_data(experimental_allow_widgets=True)
def get_data(url):
    html = pd.read_html(url, header = 1)
    playerlist = html[0]
    playerlist = playerlist.drop(["Rk", "Matches", 'Gls.1', 'Ast.1', 'G+A', 'G-PK.1', 'G+A-PK', 'npxG', 'npxG+xAG', 'xG.1', 'xAG.1', 'xG+xAG', 'npxG.1', 'npxG+xAG.1'], axis = 1) 
    playerlist["Nation"] = playerlist["Nation"].str.replace('[a-z]', '')
    playerlist["Age"] = playerlist["Age"].str.replace(r'(-\d\d\d)', '')
    playerlist["Comp"] = playerlist["Comp"].str.replace(r'(eng)|(fr)|(it)|(de)|(es)', '')
    playerlist["Comp"] = playerlist["Comp"].str.replace(r'Bunsliga', 'Bundesliga')


    return playerlist


def filter_player_by_sidebar(url, url_transfer, url_defend, url_gk,player_name, league,radio):
    my_player = load_data(url)[0].loc[load_data(url)[0]["Player"] == player_name]
    my_player = my_player[['Player','Nation','Pos','Age','Gls','Ast','xG','xAG']]
    my_player = pd.concat([my_player, Analysis(url)[2].loc[Analysis(url)[2]["Player"] == player_name][['TklW','Intercept']]], axis = 1)
    playerlist = get_data(url_transfer)[['Player','Nation','Pos','Age','Squad','Comp','Gls','Ast','xG','xAG']] #All players
    playerlist = pd.concat([playerlist, get_player_defend_table(url_defend)], axis=1)

    playerlist = playerlist.loc[playerlist["Pos"].str.contains(str(my_player["Pos"].iloc[0]))]                 #Filter same possision with my player
    playerlist = playerlist[playerlist["Player"].str.contains(player_name)==False]
    playerlist = playerlist[playerlist["Squad"].str.contains("Manchester City")==False]


        
    if radio == "Outfield players":
        if league == "All":
            pass
        else:
            playerlist = playerlist.loc[playerlist["Comp"].str.contains(str(league))] 

        if "DF" in my_player["Pos"].iloc[0]:
#             playerlist_tkl = playerlist.sort_values(by='TklW', ascending=False)
            playerlist_tkl = playerlist.loc[playerlist["TklW"].astype(int) >= int(my_player["TklW"].iloc[0])]
            playerlist_int = playerlist.loc[playerlist["Int"].astype(int) >= int(my_player["Intercept"].iloc[0])]

            #playerlist_int = playerlist.sort_values(by='Int', ascending=False)
            playerlist = pd.concat([playerlist_tkl, playerlist_int], axis = 0)
        elif "MF" in my_player["Pos"].iloc[0]:
            playerlist = playerlist.loc[playerlist["xAG"].astype(float) >= float(my_player["xAG"].iloc[0])]
            playerlist = playerlist.head(10)

        elif "FW" in my_player["Pos"].iloc[0]:
            playerlist_fw = playerlist.loc[playerlist["xG"].astype(float) >= float(my_player["xG"].iloc[0])]
            if playerlist_fw.empty:
                playerlist = playerlist.sort_values(by='xG', ascending=False)
            else:
                playerlist = playerlist_fw
            playerlist = playerlist.head(10)


        playerlist = playerlist.drop_duplicates(subset="Player")
        playerlist = playerlist.reset_index(drop = True)
    
    else:
        playerlist = get_goalkeeper_table(url_gk)

        if league == "All":
            pass
        else:
            playerlist = playerlist.loc[playerlist["Comp"].str.contains(str(league))]

        playerlist = playerlist.sort_values(by='GA', ascending=False)
        playerlist = playerlist.head(10)
        playerlist = playerlist.reset_index(drop = True)

    return playerlist


    
url_defend = "https://fbref.com/en/comps/Big5/defense/players/Big-5-European-Leagues-Stats"
url_gk = "https://fbref.com/en/comps/Big5/keepersadv/players/Big-5-European-Leagues-Stats"
def get_goalkeeper_table(url_gk):
        
    html = pd.read_html(url_gk, header = 1)
    gk = html[0]
    gk["Nation"] = gk["Nation"].str.replace('[a-z]', '')
    gk["Age"] = gk["Age"].str.replace(r'(-\d\d\d)', '')
    gk["Comp"] = gk["Comp"].str.replace(r'(eng)|(fr)|(it)|(de)|(es)', '')
    gk["Comp"] = gk["Comp"].str.replace(r'Bunsliga', 'Bundesliga')
    gk = gk[['Player','Nation','Pos','Squad','Comp','Age','GA']]
    gk = gk[gk["Player"].str.contains("Player")==False]
    gk = gk[gk["GA"].str.contains(r'[A-Za-z]')==False]

    gk['GA'] = gk['GA'].astype(int)

    return gk

def get_player_defend_table(url_defend):
    
    html = pd.read_html(url_defend, header = 1)
    player_de = html[0]
    player_de = player_de[['TklW','Int']]

    return player_de
    
