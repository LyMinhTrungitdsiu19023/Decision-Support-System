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

from Analysis import *
from Transfer import *

def recommendation(url, squad, speed, intercept, style, squad_dis, approach, gk):
    
#Squad 4-4-2
    if squad == "4-4-2" and approach == "Defend":

        squad_dis = squad_dis
        gk_df = load_data(url)[0].loc[load_data(url)[0]["Player"] == gk]
        gk = gk_df[['Player','Nation', 'Pos']]
        
        fw_df = defend_approach(url)[0]
        fw_df = fw_df.head(2)
        fw = fw_df[['Player','Nation', 'Pos']]
        
        mid_df = defend_approach(url)[1]
        mid_df = mid_df.head(4)
        mid = mid_df[['Player','Nation', 'Pos']]

        de_df = defend_approach(url)[2]
        de_df = de_df.head(4)
        de = de_df[['Player','Nation', 'Pos']]
        
        recommend_squad = pd.concat([gk, de, mid, fw], ignore_index=True)
        
    if squad == "4-4-2" and approach == "Possesion":

            
        squad_dis = squad_dis
        gk_df = load_data(url)[0].loc[load_data(url)[0]["Player"] == gk]
        gk = gk_df[['Player','Nation', 'Pos']]
        
        fw_df = possesion_approach(url)[0]
        fw_df = fw_df.head(2)
        fw = fw_df[['Player','Nation', 'Pos']]
        
        mid_df = possesion_approach(url)[1]
        mid_df = mid_df.head(4)
        mid = mid_df[['Player','Nation', 'Pos']]

        de_df = possesion_approach(url)[2]
        de_df = de_df.head(4)
        de = de_df[['Player','Nation', 'Pos']]
        
        recommend_squad = pd.concat([gk, de, mid, fw], ignore_index=True)
     
    if squad == "4-4-2" and approach == "Attack":
            
        squad_dis = squad_dis
        gk_df = load_data(url)[0].loc[load_data(url)[0]["Player"] == gk]
        gk = gk_df[['Player','Nation', 'Pos']]
        
        fw_df = attack_approach(url)[0]
        fw_df = fw_df.head(2)
        fw = fw_df[['Player','Nation', 'Pos']]
        
        mid_df = attack_approach(url)[1]
        mid_df = mid_df.head(4)
        mid = mid_df[['Player','Nation', 'Pos']]

        de_df = attack_approach(url)[2]
        de_df = de_df.head(4)
        de = de_df[['Player','Nation', 'Pos']]
        
        recommend_squad = pd.concat([gk,de, mid, fw], ignore_index=True) 

#Squad 4-2-3-1
    if squad == "4-2-3-1" and approach == "Defend":

        squad_dis = squad_dis
        gk_df = load_data(url)[0].loc[load_data(url)[0]["Player"] == gk]
        gk = gk_df[['Player','Nation', 'Pos']]
        
        fw_df = defend_approach(url)[0]
        fw_df = fw_df.head(1)
        fw = fw_df[['Player','Nation', 'Pos']]
        
        mid_df = defend_approach(url)[1]
        mid_df = mid_df.head(5)
        mid = mid_df[['Player','Nation', 'Pos']]

        de_df = defend_approach(url)[2]
        de_df = de_df.head(4)
        de = de_df[['Player','Nation', 'Pos']]
        
        recommend_squad = pd.concat([gk, de, mid, fw], ignore_index=True)
        
    if squad == "4-2-3-1" and approach == "Possesion":
            
        squad_dis = squad_dis
        gk_df = load_data(url)[0].loc[load_data(url)[0]["Player"] == gk]
        gk = gk_df[['Player','Nation', 'Pos']]
        
        fw_df = possesion_approach(url)[0]
        fw_df = fw_df.head(1)
        fw = fw_df[['Player','Nation', 'Pos']]
        
        mid_df = possesion_approach(url)[1]
        mid_df = mid_df.head(5)
        mid = mid_df[['Player','Nation', 'Pos']]

        de_df = possesion_approach(url)[2]
        de_df = de_df.head(4)
        de = de_df[['Player','Nation', 'Pos']]
        
        recommend_squad = pd.concat([gk, de, mid, fw], ignore_index=True)
     
    if squad == "4-2-3-1" and approach == "Attack":
            
        squad_dis = squad_dis
        gk_df = load_data(url)[0].loc[load_data(url)[0]["Player"] == gk]
        gk = gk_df[['Player','Nation', 'Pos']]
        
        fw_df = attack_approach(url)[0]
        fw_df = fw_df.head(1)
        fw = fw_df[['Player','Nation', 'Pos']]
        
        mid_df = attack_approach(url)[1]
        mid_df = mid_df.head(5)
        mid = mid_df[['Player','Nation', 'Pos']]

        de_df = attack_approach(url)[2]
        de_df = de_df.head(4)
        de = de_df[['Player','Nation', 'Pos']]
        
        recommend_squad = pd.concat([gk,de, mid, fw], ignore_index=True) 

#Squad 4-3-3        
    if squad == "4-3-3" and approach == "Defend":

        squad_dis = squad_dis
        gk_df = load_data(url)[0].loc[load_data(url)[0]["Player"] == gk]
        gk = gk_df[['Player','Nation', 'Pos']]
        
        fw_df = defend_approach(url)[0]
        fw_df = fw_df.head(3)
        fw = fw_df[['Player','Nation', 'Pos']]
        
        mid_df = defend_approach(url)[1]
        mid_df = mid_df.head(3)
        mid = mid_df[['Player','Nation', 'Pos']]

        de_df = defend_approach(url)[2]
        de_df = de_df.head(4)
        de = de_df[['Player','Nation', 'Pos']]
        
        recommend_squad = pd.concat([gk, de, mid, fw], ignore_index=True)
        
    if squad == "4-3-3" and approach == "Possesion":
         
        squad_dis = squad_dis
        gk_df = load_data(url)[0].loc[load_data(url)[0]["Player"] == gk]
        gk = gk_df[['Player','Nation', 'Pos']]
        
        fw_df = possesion_approach(url)[0]
        fw_df = fw_df.head(3)
        fw = fw_df[['Player','Nation', 'Pos']]
        
        mid_df = possesion_approach(url)[1]
        mid_df = mid_df.head(3)
        mid = mid_df[['Player','Nation', 'Pos']]

        de_df = possesion_approach(url)[2]
        de_df = de_df.head(4)
        de = de_df[['Player','Nation', 'Pos']]
        
        recommend_squad = pd.concat([gk, de, mid, fw], ignore_index=True)
     
    if squad == "4-3-3" and approach == "Attack":
            
        squad_dis = squad_dis
        gk_df = load_data(url)[0].loc[load_data(url)[0]["Player"] == gk]
        gk = gk_df[['Player','Nation', 'Pos']]
        
        fw_df = attack_approach(url)[0]
        fw_df = fw_df.head(3)
        fw = fw_df[['Player','Nation', 'Pos']]
        
        mid_df = attack_approach(url)[1]
        mid_df = mid_df.head(3)
        mid = mid_df[['Player','Nation', 'Pos']]

        de_df = attack_approach(url)[2]
        de_df = de_df.head(4)
        de = de_df[['Player','Nation', 'Pos']]
        
        recommend_squad = pd.concat([gk,de, mid, fw], ignore_index=True) 
        
    return recommend_squad
