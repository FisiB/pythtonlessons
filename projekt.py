import streamlit as st
import pandas as pd
import plotly.express as px

players_df=pd.read_csv("players.csv")
# st.title("Football players 2025-2026")
# st.write("Players statistics this season!")
# st.subheader("The summery of statistics")
# totalplayers=players_df.shape[0]
# player_names=players_df["Player"].nunique()
# positions = players_df["Pos"].mode()[0]
# players_df["G+A"] = players_df["Gls"] + players_df["Ast"]
# goal_assists = players_df["G+A"].mean()

st.sidebar.header("Football")
st.sidebar.write("Look at football stats this season")
option =st.sidebar.radio("Chose an option",["Home","Players Nation and Club","Top players stats"])

if option == "Home":
 st.title("Football players 2025-2026")
 st.write("Players statistics this season!")
 st.subheader("The summery of statistics")
 totalplayers=players_df.shape[0]
 player_names=players_df["Player"].nunique()
 positions = players_df["Pos"].mode()[0]
 players_df["G+A"] = players_df["Gls"] + players_df["Ast"]
 goal_assists = players_df["G+A"].mean()

elif option == "Players Nation and Club":
 totalplayers = players_df.shape[0]
 player_names = players_df["Player"].nunique()
 total_nations = players_df["Nation"].nunique()
 most_common_nation = players_df["Nation"].mode()[0]
 total_clubs = players_df["Squad"].nunique()
 most_common_club = players_df["Squad"].mode()[0]
 col1, col2, col3, col4 = st.columns(4)
 col1.metric("Total Players", totalplayers)
 col2.metric("Unique Player Names", player_names) 
 col3.metric("Most Common Nation", most_common_nation)
 col4.metric("Most Common Club", most_common_club)


elif option == "Top players stats":
 st.title("Players stats")
 st.title("Check out this sesons top players")
 st.write("Look at the statistics for this season by our players")
 tab1,tab2,tab3=st.tabs(["Top player possitions","Top goalscorer","Top assister"])
 with tab1:
    st.subheader("Top positions played this season")
    fig=px.pie(players_df, names="Pos", title="Top played positions",color="Pos",
    color_discrete_sequence=px.colors.sequential.Plasma)
    st.plotly_chart(fig)

 with tab2:
    st.subheader("Top 10 most goals scored")
    top_goals=players_df["Player"].value_counts().head(10)
    st.bar_chart(top_goals)

 with tab3:

   st.subheader("Top 10 assisters")
   top_assisters=players_df["Player"].value_counts().head(10).reset_index()
   top_assisters.columns=["Player","Ast"]

   figg=px.bar(top_assisters,x="Ast",y="Player",orientation="h",
            title="Top 10 assisters",
            labels={"Ast":"Counts of Assists","Player":"Player"},
            color="Ast",color_continuous_scale=px.colors.sequential.Plasma)

   st.plotly_chart(figg)

# col1,col2,col3,col4=st.columns(4)
# col1.metric("Total Players",totalplayers)
# col2.metric("Player names",player_names)
# col3.metric("Most played position",positions)
# col4.metric("Goals and assists avarage",goal_assists)


# tab1,tab2,tab3=st.tabs(["Top player possitions","Top goalscorer","Top assister"])
# with tab1:
#     st.subheader("Top positions played this season")
#     fig=px.pie(players_df, names="Pos", title="Top played positions",color="Pos",
#     color_discrete_sequence=px.colors.sequential.Plasma)
#     st.plotly_chart(fig)

# with tab2:
#     st.subheader("Top 10 most goals scored")
#     top_goals=players_df["Player"].value_counts().head(10)
#     st.bar_chart(top_goals)

# with tab3:

#    st.subheader("Top 10 assisters")
#    top_assisters=players_df["Player"].value_counts().head(10).reset_index()
#    top_assisters.columns=["Player","Ast"]

#    figg=px.bar(top_assisters,x="Ast",y="Player",orientation="h",
#             title="Top 10 assisters",
#             labels={"Ast":"Counts of Assists","Player":"Player"},
#             color="Ast",color_continuous_scale=px.colors.sequential.Plasma)

#    st.plotly_chart(figg)