import streamlit as st
import pandas as pd
import plotly.express as px

# df=pd.DataFrame({
#     "Name":["Dion","Darsej","Jon"],
#     "Age":[17,19,21],
#     "City":["Prishtina","Prizren","Gjakova"]
# })

# st.write(df)

books_df=pd.read_csv("file.csv")
st.title("Best selling books")
st.write("The best selling books from 2009-2022")
st.subheader("The summery of statistics")
totalbooks=books_df.shape[0]
unique_titels=books_df["Name"].nunique()
avarage_rating=books_df["User Rating"].mean()
avarage_price=books_df["Price"].mean()

col1,col2,col3,col4=st.columns(4)
col1.metric("Total books",totalbooks)
col2.metric("Unqiue names",unique_titels)
col3.metric("Ratings",avarage_rating)
col4.metric("Price",avarage_price)

st.subheader("Stats")
st.write(books_df.head())

col1,col2=st.columns(2)

with col1:
    st.subheader("Top 10 most sold books")
    top_titles=books_df["Name"].value_counts().head(10)
    st.bar_chart(top_titles)

with col2:
    st.subheader("Top 10 Authors")
    top_authors=books_df["Author"].value_counts().head(10)
    st.bar_chart(top_authors)