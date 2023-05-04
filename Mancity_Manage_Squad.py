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

st.set_page_config(page_title="Manchester City Decision Support System", layout = 'wide')

url = "https://fbref.com/en/squads/b8fd03ef/Manchester-City-Stats"
url_transfer = "https://fbref.com/en/comps/Big5/stats/players/Big-5-European-Leagues-Stats"
@st.cache_data(experimental_allow_widgets=True)
def load_data(url):
    html = pd.read_html(url, header = 1)
    playerstats = html[0]
    shoot = html[4]
    passing = html[5]
    df = html[8]
    playerstats.drop(playerstats.tail(2).index, inplace = True)
    playerstats["Nation"] = playerstats["Nation"].str.replace('[a-z]', '')
    playerstats["Age"] = playerstats["Age"].str.replace(r'(-\d\d\d)', '')

    return playerstats, shoot, passing, df, html

def Analysis(url):
    #Forward
    data = load_data(url)[4]

    #Shoot
    shoot =  data[4]
    shoot.drop(shoot.tail(2).index, inplace = True)
    shoot["Nation"] = shoot["Nation"].str.replace('[a-z]', '')
    shoot = shoot.drop(['SoT%', 'Sh/90', 'SoT/90', 'G/SoT', 'Dist', 'xG', 'npxG', 'npxG/Sh', 'G-xG', 'np:G-xG', 'Matches'], axis=1)
    shoot.rename(columns = {'Gls':'Goals', 'Sh':'Shots total', 'SoT':'Shots on Target', 'G/Sh':'Goal per Shot', 'FK':'Freekick','PK':'Penalty Kick','PKatt':'Pentallty Attemp'}, inplace = True)
    shoot = shoot.reset_index(drop = True) 

    #Pass
    passing =  data[5]
    passing.drop(passing.tail(2).index, inplace = True)
    passing["Nation"] = passing["Nation"].str.replace('[a-z]', '')
#     passing = passing.drop(['xAG','xA', 'A-xAG', 'KP', '1/3', 'PPA', 'CrsPA', 'Prog','Matches'], axis=1)
    passing.rename(columns = {'Cmp':'Passed Completed', 'Att':'Passes Attempted', 'Cmp%':'%Completed'}, inplace = True)
    passing = passing.reset_index(drop = True)



    #Defend
    df =  data[8]
    df.drop(df.tail(2).index, inplace = True)
    df["Nation"] = df["Nation"].str.replace('[a-z]', '')
    df = df.drop(['Def 3rd', 'Att 3rd','Att','Lost','Sh','Pass','Tkl+Int','Clr','Matches'], axis=1)
    df.rename(columns = {'Tkl':'Number of Players Tackles', 'Tkl.1':'Number of Tackled by Competitors','Int':'Intercept', 'Err':'Mistakes lead to goals'}, inplace = True)

    df = df.reset_index(drop = True)

    #Possesion
    possesion = data[9]
    possesion.drop(possesion.tail(2).index, inplace = True)
    possesion["Nation"] = possesion["Nation"].str.replace('[a-z]', '')
    possesion_1 = pd.DataFrame()
    possesion_1 = possesion[['Player','Nation','Pos','Age','90s','Touches','Def Pen','Att Pen','Live', 'Rec', 'Mid 3rd']]
    possesion_1.rename(columns = {'Def Pen':'Touches in defensive area of team', 'Att Pen':'Touches in attacking area of team', 'Live':'Live-ball touches', 'Rec':'Number of successfully recieved the pass'}, inplace = True)
    possesion_1 = possesion_1.reset_index(drop = True)

    return shoot, passing, df, possesion_1

def Analysis_Forward(url):
    st.header('Statistics of Forward')

    shoot = Analysis(url)[0]
    shoot = shoot.loc[shoot["Pos"].str.contains("FW")]
    shoot = shoot.reset_index(drop = True)
    st.write('Stats of Shooting')
    st.dataframe(shoot)

    passing = Analysis(url)[1]
    passing = passing.loc[passing["Pos"].str.contains("FW")]
    passing = passing.reset_index(drop = True)
    st.write('Stats of Passing')
    st.dataframe(passing) 
    st.write('*Note\n Cmp.1: Passes Completed in Short Distance - Att.1 Passes Attempted in Short Distance - Cmp%.1: % Passes Completed in Short Distance - .2: Medium Distance - .3:Long Distance')

    df = Analysis(url)[2]
    df = df.loc[df["Pos"].str.contains("FW")]
    df = df.reset_index(drop = True)
    st.write('Stats of Defensive')
    st.dataframe(df)

    possesion = Analysis(url)[3]
    possesion = possesion.loc[possesion["Pos"].str.contains("FW")]
    possesion = possesion.reset_index(drop = True)
    st.write('Stats of Possesion')
    st.dataframe(possesion)
def Analysis_Mid(url):
    st.header('Statistics of Midfield')


    shoot = Analysis(url)[0]
    shoot = shoot.loc[shoot["Pos"].str.contains("MF")]
    shoot = shoot.reset_index(drop = True)
    st.write('Stats of Shooting')
    st.dataframe(shoot)

    passing = Analysis(url)[1]
    passing = passing.loc[passing["Pos"].str.contains("MF")]
    passing = passing.reset_index(drop = True)
    st.write('Stats of Passing')
    st.dataframe(passing) 
    st.write('*Note\n Cmp.1: Passes Completed in Short Distance - Att.1 Passes Attempted in Short Distance - Cmp%.1: % Passes Completed in Short Distance - .2: Medium Distance - .3:Long Distance')

    df = Analysis(url)[2]
    df = df.loc[df["Pos"].str.contains("MF")]
    df = df.reset_index(drop = True)
    st.write('Stats of Defensive')
    st.dataframe(df)

    possesion = Analysis(url)[3]
    possesion = possesion.loc[possesion["Pos"].str.contains("FW")]
    possesion = possesion.reset_index(drop = True)
    st.write('Stats of Possesion')
    st.dataframe(possesion)
def Analysis_defend(url):
    st.header('Statistics of Defensive')


    shoot = Analysis(url)[0]
    shoot = shoot.loc[shoot["Pos"].str.contains("DF")]
    shoot = shoot.reset_index(drop = True)
    st.write('Stats of Shooting')
    st.dataframe(shoot)

    passing = Analysis(url)[1]
    passing = passing.loc[passing["Pos"].str.contains("DF")]
    passing = passing.reset_index(drop = True)
    st.write('Stats of Passing')
    st.dataframe(passing) 
    st.write('*Note\n Cmp.1: Passes Completed in Short Distance - Att.1 Passes Attempted in Short Distance - Cmp%.1: % Passes Completed in Short Distance - .2: Medium Distance - .3:Long Distance')

    df = Analysis(url)[2]
    df = df.loc[df["Pos"].str.contains("DF")]
    df = df.reset_index(drop = True)
    st.write('Stats of Defensive')
    st.dataframe(df) 

    possesion = Analysis(url)[3]
    possesion = possesion.loc[possesion["Pos"].str.contains("FW")]
    possesion = possesion.reset_index(drop = True)
    st.write('Stats of Possesion')
    st.dataframe(possesion)

def plot_chart(attr, url):
    playerstats = load_data(url)
    html = pd.read_html(url, header = 1)
    defend = html[8]
#     defend = load_data(url)[3]
    defend.drop(defend.tail(2).index, inplace = True)
#     defend = Analysis(url)[2]
    rc = {'figure.figsize':(8,4),
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

        goal_df =  load_data(url)[0].sort_values(by='Gls', ascending=False)
        goal_df = goal_df.head(10)
        goal_df_1 = pd.DataFrame()
        goal_df_1 = goal_df[["Player", "Gls"]]
        ax = sns.barplot(x = goal_df_1["Player"], y = goal_df_1["Gls"], data=goal_df_1.reset_index(), color = "#00BFFF")
        ax.set(xlabel = "Player", ylabel = "Goals")
        plt.xticks(rotation=66,horizontalalignment="right")
        for p in ax.patches:
            ax.annotate(format(str(int(p.get_height()))), 
                  (p.get_x() + p.get_width() / 2, p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 10),
                   rotation = 0,
                   textcoords = 'offset points')
        st.pyplot(fig)

    if attr == "Assist":

        ast_df =  load_data(url)[0].sort_values(by='Ast', ascending=False)
        ast_df = ast_df.head(10)
        ast_df_1 = pd.DataFrame()
        ast_df_1 = ast_df[["Player", "Ast"]]
        ax = sns.barplot(x = ast_df_1["Player"], y = ast_df_1["Ast"], data=ast_df_1.reset_index(), color = "#FCE6C9")
        ax.set(xlabel = "Player", ylabel = "Assists")
        plt.xticks(rotation=66,horizontalalignment="right")
        for p in ax.patches:
            ax.annotate(format(str(int(p.get_height()))), 
                  (p.get_x() + p.get_width() / 2, p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 10),
                   rotation = 0,
                   textcoords = 'offset points')
        st.pyplot(fig)

    if attr == "Goal per 90Mins":

        Gls_df =  load_data(url)[0].sort_values(by='Gls.1', ascending=False)
        Gls_df = Gls_df.head(10)
        Gls_df_1 = pd.DataFrame()
        Gls_df_1 = Gls_df[["Player", "Gls.1"]]
        ax = sns.barplot(x = Gls_df_1["Player"], y = Gls_df_1["Gls.1"], data=Gls_df_1.reset_index(), color = "#FFD700")
        ax.set(xlabel = "Player", ylabel = "Goal per Shots")
        plt.xticks(rotation=66,horizontalalignment="right")
        for p in ax.patches:
            ax.annotate(format(p.get_height(), '.2f'), 
                  (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 10),
                   rotation = 0,
                   textcoords = 'offset points')
        st.pyplot(fig)

    if attr == "Passed per 90Mins":

        astcom_df =  load_data(url)[0].sort_values(by='Ast.1', ascending=False)
        astcom_df = astcom_df.head(10)
        astcom_df_1 = pd.DataFrame()
        astcom_df_1 = astcom_df[["Player", "Ast.1"]]
        ax = sns.barplot(x = astcom_df_1["Player"], y = astcom_df_1["Ast.1"], data=astcom_df_1.reset_index(), color = "#7FFF00")
        ax.set(xlabel = "Player", ylabel = "Passed Completed")
        plt.xticks(rotation=66,horizontalalignment="right")
        for p in ax.patches:
            ax.annotate(format(p.get_height(), '.2f'), 
                  (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 10),
                   rotation = 0,
                   textcoords = 'offset points')
        st.pyplot(fig)

    if attr == "Total Yellow Cards":

        CrdY_df =  load_data(url)[0].sort_values(by='CrdY', ascending=False)
        CrdY_df = CrdY_df.head(10)
        CrdY_df_1 = pd.DataFrame()
        CrdY_df_1 = CrdY_df[["Player", "CrdY"]]
        ax = sns.barplot(x = CrdY_df_1["Player"], y = CrdY_df_1["CrdY"], data=CrdY_df_1.reset_index(), color = "#CD5B45")
        ax.set(xlabel = "Player", ylabel = "Yellow Cards")
        plt.xticks(rotation=66,horizontalalignment="right")
        for p in ax.patches:
            ax.annotate(format(str(int(p.get_height()))), 
                  (p.get_x() + p.get_width() / 2, p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 10),
                   rotation = 0,
                   textcoords = 'offset points')
        st.pyplot(fig)

    if attr == "Total Red Cards":

        CrdR_df =  load_data(url)[0].sort_values(by='CrdR', ascending=False)
        CrdR_df = CrdR_df.head(10)
        CrdR_df_1 = pd.DataFrame()
        CrdR_df_1 = CrdR_df[["Player", "CrdR"]]
        ax = sns.barplot(x = CrdR_df_1["Player"], y = CrdR_df_1["CrdR"], data=CrdR_df_1.reset_index(), color = "#CD5B45")
        ax.set(xlabel = "Player", ylabel = "Red Cards")
        plt.xticks(rotation=66,horizontalalignment="right")
        for p in ax.patches:
            ax.annotate(format(str(int(p.get_height()))), 
                  (p.get_x() + p.get_width() / 2, p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 10),
                   rotation = 0,
                   textcoords = 'offset points')
        st.pyplot(fig)


    if attr == "Total Penalty Goals":

        PKatt_df =  load_data(url)[0].sort_values(by='PKatt', ascending=False)
        PKatt_df = PKatt_df.head(10)
        PKatt_df_1 = pd.DataFrame()
        PKatt_df_1 = PKatt_df[["Player", "PKatt"]]
        ax = sns.barplot(x = PKatt_df_1["Player"], y = PKatt_df_1["PKatt"], data=PKatt_df_1.reset_index(), color = "#53868B")
        ax.set(xlabel = "Player", ylabel = "Total Penalty Goals")
        plt.xticks(rotation=66,horizontalalignment="right")
        for p in ax.patches:
            ax.annotate(format(str(int(p.get_height()))), 
                  (p.get_x() + p.get_width() / 2, p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 10),
                   rotation = 0,
                   textcoords = 'offset points')
        st.pyplot(fig)

    if attr == "Tackle Completed":

        tkl_df = defend.sort_values(by='Tkl.1', ascending=False)
        tkl_df = tkl_df.head(10)
        tkl_df_1 = pd.DataFrame()
        tkl_df_1 = tkl_df[["Player", "Tkl.1"]]
        ax = sns.barplot(x = tkl_df_1["Player"], y = tkl_df_1["Tkl.1"], data=tkl_df_1.reset_index(), color = "#79CDCD")
        ax.set(xlabel = "Player", ylabel = "Successful Tackles ")
        plt.xticks(rotation=66,horizontalalignment="right")
        for p in ax.patches:
            ax.annotate(format(str(int(p.get_height()))), 
                  (p.get_x() + p.get_width() / 2, p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 10),
                   rotation = 0,
                   textcoords = 'offset points')
        st.pyplot(fig)


    if attr == "Number of Tackled":

        tkled_df = defend.sort_values(by='Tkl', ascending=False)
        tkled_df = tkled_df.head(10)
        tkled_df_1 = pd.DataFrame()
        tkled_df_1 = tkled_df[["Player", "Tkl"]]
        ax = sns.barplot(x = tkled_df_1["Player"], y = tkled_df_1["Tkl"], data=tkled_df_1.reset_index(), color = "#79CDCD")
        ax.set(xlabel = "Player", ylabel = "Tackled by Competitors")
        plt.xticks(rotation=66,horizontalalignment="right")
        for p in ax.patches:
            ax.annotate(format(str(int(p.get_height()))), 
                  (p.get_x() + p.get_width() / 2, p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 10),
                   rotation = 0,
                   textcoords = 'offset points')
        st.pyplot(fig)

    if attr == "Mistakes lead to goals":

        err_df = defend.sort_values(by='Err', ascending=False)
        err_df = err_df.head(10)
        err_df_1 = pd.DataFrame()
        err_df_1 = err_df[["Player", "Err"]]
        ax = sns.barplot(x = err_df_1["Player"], y = err_df_1["Err"], data=err_df_1.reset_index(), color = "#79CDCD")
        ax.set(xlabel = "Player", ylabel = "Mistakes lead to goals")
        plt.xticks(rotation=66,horizontalalignment="right")
        for p in ax.patches:
            ax.annotate(format(str(int(p.get_height()))), 
                  (p.get_x() + p.get_width() / 2, p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 10),
                   rotation = 0,
                   textcoords = 'offset points')
        st.pyplot(fig)

    if attr == "Done Intercept":

        int_df = defend.sort_values(by='Int', ascending=False)
        int_df = int_df.head(10)
        int_df_1 = pd.DataFrame()
        int_df_1 = int_df[["Player", "Int"]]
        ax = sns.barplot(x = int_df_1["Player"], y = int_df_1["Int"], data=int_df_1.reset_index(), color = "#EE3A8C")
        ax.set(xlabel = "Player", ylabel = "Done Intercept")
        plt.xticks(rotation=66,horizontalalignment="right")
        for p in ax.patches:
            ax.annotate(format(str(int(p.get_height()))), 
                  (p.get_x() + p.get_width() / 2, p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 10),
                   rotation = 0,
                   textcoords = 'offset points')
        st.pyplot(fig)

    if attr == "Number of Touches":
        possesion = Analysis(url)[3]
        possesion_df = possesion.sort_values(by='Touches', ascending=False)
        possesion_df = possesion_df.head(10)
        possesion_df_1 = pd.DataFrame()
        possesion_df_1 = possesion_df[["Player", "Touches"]]
        ax = sns.barplot(x = possesion_df_1["Player"], y = possesion_df_1["Touches"], data=possesion_df_1.reset_index(), color = "#FFFFFF")
        ax.set(xlabel = "Player", ylabel = "Number of Touches")
        plt.xticks(rotation=66,horizontalalignment="right")
        for p in ax.patches:
            ax.annotate(format(str(int(p.get_height()))), 
                  (p.get_x() + p.get_width() / 2, p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 10),
                   rotation = 0,
                   textcoords = 'offset points')
        st.pyplot(fig)

    if attr == "Number of Touches in attacking area":
        attTouches = Analysis(url)[3]
        attTouches_df = attTouches.sort_values(by='Touches in attacking area of team', ascending=False)
        attTouches_df = attTouches_df.head(10)
        attTouches_df_1 = pd.DataFrame()
        attTouches_df_1 = attTouches_df[["Player", "Touches in attacking area of team"]]
        ax = sns.barplot(x = attTouches_df_1["Player"], y = attTouches_df_1["Touches in attacking area of team"], data=attTouches_df_1.reset_index(), color = "#FFFFFF")
        ax.set(xlabel = "Player", ylabel = "Touches in attacking area of team")
        plt.xticks(rotation=66,horizontalalignment="right")
        for p in ax.patches:
            ax.annotate(format(str(int(p.get_height()))), 
                  (p.get_x() + p.get_width() / 2, p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 10),
                   rotation = 0,
                   textcoords = 'offset points')
        st.pyplot(fig)

    if attr == "Playing time":

        time_df =  load_data(url)[0].sort_values(by='90s', ascending=False)
        time_df = time_df.head(10)
        time_df_1 = pd.DataFrame()
        time_df_1 = time_df[["Player", "90s"]]
        ax = sns.barplot(x = time_df_1["Player"], y = time_df_1["90s"], data=time_df_1.reset_index(), color = "#7FFF00")
        ax.set(xlabel = "Player", ylabel = "Playing time divide by 90 second")
        plt.xticks(rotation=66,horizontalalignment="right")
        for p in ax.patches:
            ax.annotate(format(p.get_height(), '.2f'), 
                  (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 10),
                   rotation = 0,
                   textcoords = 'offset points')
        st.pyplot(fig)
def prediction(url):
    data = pd.read_html(url, header = 1)
#     data = load_data(url)
    shoot = data[4]
    shoot.drop(shoot.tail(2).index, inplace = True)
    shoot["Nation"] = shoot["Nation"].str.replace('[a-z]', '')
    exshoot = pd.DataFrame()
    exshoot = shoot[['Player','Nation','Age', 'Pos','xG', 'npxG', 'npxG/Sh', 'G-xG', 'np:G-xG']]
    exshoot = exshoot.reset_index(drop = True) 

    passing = data[5]
    passing.drop(passing.tail(2).index, inplace = True)
    passing["Nation"] = passing["Nation"].str.replace('[a-z]', '')
    expassing = pd.DataFrame()
    expassing = passing[['Player','xAG', 'xA']]


    predic_df = pd.merge(exshoot, expassing, on='Player', how='inner')
    predic_df.rename(columns = {'xG':'Expected Goals', 'npxG':'NonPenalty Expected Goals', 'npxG/Sh':'NonPenalty Expected Goals/shots', 'G-xG':'Goals compare ExGoals', 'np:G-xG':'NonPen Goal compare with expected', 'xAG':'Expected Assist Goals', 'xA':'Expected Assists'}, inplace = True)

    return predic_df 

def prediction_chart(attr):

    rc = {'figure.figsize':(8,4),
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

    predic_df = prediction(url)
    if attr == "Expected Goals":
        xG = predic_df.sort_values(by='Expected Goals', ascending=False)
        xG = xG.head(10)
        xG_1 = pd.DataFrame()
        xG_1 = xG[["Player", "Expected Goals"]]
        ax = sns.barplot(x = xG_1["Player"], y = xG_1["Expected Goals"], data=xG_1.reset_index(), color = "#CD5C5C")
        ax.set(xlabel = "Players with Expected Goal", ylabel = "Expected Goals")
        plt.xticks(rotation=66,horizontalalignment="right")
        for p in ax.patches:
            ax.annotate(format(p.get_height(), '.2f'), 
                  (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 10),
                   rotation = 0,
                   textcoords = 'offset points')
        st.pyplot(fig)

    if attr == "Expected Assists":
        xA = predic_df.sort_values(by='Expected Assists', ascending=False)
        xA = xA.head(10)
        xA_1 = pd.DataFrame()
        xA_1 = xA[["Player", "Expected Assists"]]
        ax = sns.barplot(x = xA_1["Player"], y = xA_1["Expected Assists"], data=xA_1.reset_index(), color = "#CD5C5C")
        ax.set(xlabel = "Players with Expected Assists", ylabel = "Expected Assists")
        plt.xticks(rotation=66,horizontalalignment="right")
        for p in ax.patches:
            ax.annotate(format(p.get_height(), '.2f'), 
                  (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha = 'center',
                   va = 'center', 
                   xytext = (0, 10),
                   rotation = 0,
                   textcoords = 'offset points')
        st.pyplot(fig)
        
        
def defend_approach(url):
    expected = load_data(url)[0]
    
    fw_df = expected.loc[expected["Pos"].str.contains("FW")]
    fw_df = fw_df[fw_df["Player"].str.contains("Bernardo Silva")==False]
    fw = pd.DataFrame()
    fw = fw_df[['Player','Nation','Pos', 'xG']]
    fw = fw.sort_values(by='xG', ascending=False)

    possesion = Analysis(url)[3]
    mid = pd.DataFrame()
    mid = possesion[['Player','Nation','Pos', 'Mid 3rd']]
    mid = possesion.loc[possesion["Pos"].str.contains("MF")]
    mid = mid.sort_values(by='Mid 3rd', ascending=False)

    df = Analysis(url)[2]
    df.drop(df.tail(2).index, inplace = True)
    df["Nation"] = df["Nation"].str.replace('[a-z]', '')
    de = pd.DataFrame()
    de = df[['Player','Nation','Pos','TklW']]
    de = de.loc[de["Pos"].str.contains("DF")]
    de = de[de["Player"].str.contains("Phil Foden")==False]
    de = de.sort_values(by='TklW', ascending=False)
    
    return fw, mid, de

def possesion_approach(url):

    possesion = Analysis(url)[3]
    fw_df = possesion.loc[possesion["Pos"].str.contains("FW")]
    fw_df = fw_df[fw_df["Player"].str.contains("Bernardo Silva")==False]
    fw = pd.DataFrame()
    fw = fw_df[['Player','Nation','Pos', 'Touches']]
    fw = fw.sort_values(by='Touches', ascending=False)

    mid_df = possesion.loc[possesion["Pos"].str.contains("MF")]
    mid = pd.DataFrame()
    mid = mid_df[['Player','Nation','Pos', 'Touches']]
    mid = mid.sort_values(by='Touches', ascending=False)
    
    de_df = possesion.loc[possesion["Pos"].str.contains("DF")]
    de_df = de_df[de_df["Player"].str.contains("Phil Foden")==False]
    de = pd.DataFrame()
    de = de_df[['Player','Nation','Pos', 'Touches']]
    de = de.sort_values(by='Touches', ascending=False)
    return fw, mid, de

def attack_approach(url):
    expected = load_data(url)[0]
    
    fw_df = expected.loc[expected["Pos"].str.contains("FW")]
    fw_df = fw_df[fw_df["Player"].str.contains("Bernardo Silva")==False]
    fw = pd.DataFrame()
    fw = fw_df[['Player','Nation','Pos', 'xG']]
    fw = fw.sort_values(by='xG', ascending=False)

    mid_df = expected.loc[expected["Pos"].str.contains("MF")]
    mid = pd.DataFrame()
    mid = mid_df[['Player','Nation','Pos', 'xAG']]
    mid = mid.sort_values(by='xAG', ascending=False)
    
    de_df = expected.loc[expected["Pos"].str.contains("DF")]
    de_df = de_df[de_df["Player"].str.contains("Phil Foden")==False]
    de = pd.DataFrame()
    de = de_df[['Player','Nation','Pos', 'xAG']]
    de = de.sort_values(by='xAG', ascending=False)  
    
    return fw, mid, de

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


###Implement Transfer Role

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
    
##################################################################################################################################################################################################3
###Build GUI / Interface of the Web App


image = Image.open('squad2223.jpg')

st.image(image, caption='The Citizen', width=1000)


st.title("Manchester City Football Club Management Decision Support System")


st.markdown("""
Project of Information System Management course\n
by\n
Ly Minh Trung - Kieu Chi Huy - Truong Thai Ngoc Toan - Nguyen Dao Trung Hieu - Nguyen Anh Tuan
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
    see_data = st.expander("Information of Manchester City's Players 👉")
    with see_data: 
        st.header("Information of Manchester City's Players")
        st.write('Data Dimension: ' + str(load_data(url)[0].shape[0]) + ' rows and ' + str(load_data(url)[0].shape[1]) + ' columns.')
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


