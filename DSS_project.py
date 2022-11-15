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
    passing = passing.drop(['xAG','xA', 'A-xAG', 'KP', '1/3', 'PPA', 'CrsPA', 'Prog','Matches'], axis=1)
    passing.rename(columns = {'Cmp':'Passed Completed', 'Att':'Passes Attempted', 'Cmp%':'%Completed'}, inplace = True)
    passing = passing.reset_index(drop = True)
    

    
    #Defend
    df = data[8]
    df.drop(df.tail(2).index, inplace = True)
    df["Nation"] = df["Nation"].str.replace('[a-z]', '')
    df = df.drop(['Def 3rd','Mid 3rd', 'Att 3rd','Att','Past','Sh','Pass','Int','Tkl+Int','Clr','Matches'], axis=1)
    df.rename(columns = {'Tkl':'Number of Players Tackles', 'Tkl.1':'Number of Tackled by Competitors', 'Err':'Mistakes lead to goals'}, inplace = True)

    df = df.reset_index(drop = True)
 
    
    return shoot, passing, df
 
def Analysis_Forward(url):
    st.header('Statistics of Forward')
    


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
    st.dataframe(df, width=2500, height=400)
    
def Analysis_Mid(url):
    st.header('Statistics of Midfield')


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
    st.dataframe(df, width=2500, height=400)
    
    
def Analysis_defend(url):
    st.header('Statistics of Defensive')


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
    st.dataframe(df, width=2500, height=400) 

# def chart_analysis_information_goal(attr, playerstats):
#     if attr == "Goal":
#         goal_df = playerstats.sort_values(by='Gls', ascending=False)
#         goal_df = goal_df.head(10)
        
#     return goal_df
def plot_chart(attr, url):
    playerstats = load_data(url)
    defend_data = pd.read_html(url, header = 1)

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

        goal_df = playerstats.sort_values(by='Gls', ascending=False)
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

        ast_df = playerstats.sort_values(by='Ast', ascending=False)
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

        Gls_df = playerstats.sort_values(by='Gls.1', ascending=False)
        Gls_df = Gls_df.head(10)
        Gls_df_1 = pd.DataFrame()
        Gls_df_1 = Gls_df[["Player", "Gls.1"]]
        ax = sns.barplot(x = Gls_df_1["Player"], y = Gls_df_1["Gls.1"], data=Gls_df_1.reset_index(), color = "#FFD700")
        ax.set(xlabel = "Player", ylabel = "Goal per Shots")
        plt.xticks(rotation=66,horizontalalignment="right")
        st.pyplot(fig)
        
    if attr == "Passed per 90Mins":

        astcom_df = playerstats.sort_values(by='Ast.1', ascending=False)
        astcom_df = astcom_df.head(10)
        astcom_df_1 = pd.DataFrame()
        astcom_df_1 = astcom_df[["Player", "Ast.1"]]
        ax = sns.barplot(x = astcom_df_1["Player"], y = astcom_df_1["Ast.1"], data=astcom_df_1.reset_index(), color = "#7FFF00")
        ax.set(xlabel = "Player", ylabel = "Passed Completed")
        plt.xticks(rotation=66,horizontalalignment="right")
        st.pyplot(fig)
        
    if attr == "Total Yellow Cards":

        CrdY_df = playerstats.sort_values(by='CrdY', ascending=False)
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

        CrdR_df = playerstats.sort_values(by='CrdR', ascending=False)
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

        PKatt_df = playerstats.sort_values(by='PKatt', ascending=False)
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
        tkl = defend_data[8]
        tkl.drop(tkl.tail(2).index, inplace = True)
        tkl_df = tkl.sort_values(by='Tkl.1', ascending=False)
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
        tkled = defend_data[8]
        tkled.drop(tkled.tail(2).index, inplace = True)
        tkled_df = tkled.sort_values(by='Tkl', ascending=False)
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
        err = defend_data[8]
        err.drop(err.tail(2).index, inplace = True)
        err_df = err.sort_values(by='Err', ascending=False)
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

        
        
def prediction(url):
    data = pd.read_html(url, header = 1)
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
    predic_df = prediction(url)
    if attr == "Expected Goals":
        xG = xG.sort_values(by='Expected Goals', ascending=False)
        xG = xG.head(10)
        xG_1 = pd.DataFrame()
        xG_1 = xG[["Player", "Expected Goals"]]
        ax = sns.barplot(x = xG_1["Player"], y = xG_1["Expected Goals"], data=xG_1.reset_index(), color = "#EEB422")
        ax.set(xlabel = "Players with Expected Goal", ylabel = "Expected Goals")
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
#button 
# if st.button('Squad Analysis'):
fw = st.checkbox("Statistics of Forward")
mf = st.checkbox("Statistics of Midfield")
df = st.checkbox("Statistics of Defensive")
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
    st.markdown('Investigate a variety of stats for each player. Top 10 players who score the most goals, assist, pass, or mistakes? How does players compare with each others?')
    select_attr = st.selectbox('Which attribute do you want to analyze?', ('Goal','Assist','Tackle Completed','Number of Tackled','Mistakes lead to goals','Goal per 90Mins','Passed per 90Mins', 'Total Yellow Cards', 'Total Red Cards', 'Total Penalty Goals'))
#     st.selectbox('Which measure do you want to analyze?', ('Mean','Median','Absolute','Maximum','Minimum'))
with row_wordx:
#     st.dataframe(plot_chart(select_attr))
    plot_chart(select_attr, url)

st.header("Prediction of the player's ability")
see_predict_table = st.expander("Show prediction table 👉")
with see_predict_table: 
    st.dataframe(prediction(url), width=2500, height=400)

    
# see_predict_chart = st.expander("Show prediction Chart 👉")
# with see_predict_chart:
st.markdown('Investigate a variety of prediction for each player. Top 10 players who predicted to score the most goals, assist, pass, or mistakes? How does players compare with each others?')
select_pre = st.selectbox('Which attribute do you want to see prediction?', ('Expected Goals','Expected Assists','NonPenalty Expected Goals','NonPenalty Expected Goals/shots','NonPen Goal compare with expected','Goals compare ExGoals','Expected Assist Goals'))
prediction_chart(select_pre)
