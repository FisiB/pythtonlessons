import streamlit as st
import requests
import pandas as pd

st.title("Project Managment App")

st.header("Add Developer")
dev_name=st.text_input("Developer Name")
dev_exp=st.number_input("Experience (Years)",min_value=0,max_value=50,value=0)

if st.button("Create Developer"):
    dev_data={"name":dev_name,"experience":dev_exp}
    response=requests.post("http://localhost:8000/developers/",json=dev_data)
    st.json(response.json())