import streamlit as st
import requests
import pandas as pd

st.title("Project Managment App")

st.header("Add a Developer")
dev_name=st.text_input("Developer Name")
dev_experience=st.number_input("Developer Experience (years)",min_value=0,max_value=50,step=1)

if st.button("Create Developer"):
    dev_data={"name":dev_name,"experience":dev_experience}
    response=requests.post("http://loclalhost:800/developers/",json=dev_data)
    st.json(response.json)

st.header("Add a Project")
proj_title=st.text_input("Project Title")
proj_description=st.text_area("Project Description")
proj_languages=st.text_input("Programing Languages")
lead_dev_name=st.text_input("Lead Developer Name")
lead_dev_experience=st.number_input("Lead Developer Experience",min_value=0,max_value=50,step=1)


if st.button("Create Project"):
    lead_dev_data={"name":lead_dev_name,"experience":lead_dev_experience}
    proj_Data={
        "title":proj_title,
        "description":proj_description,
        "languages":proj_languages.split(","),
        "lead_developer":lead_dev_data
    }
    response=requests.post("http://localhost:800/projects/",json=proj_Data)
    st.json(response.json())

st.header("Project Dashboard")

if st.button("Get Projects"):
    response=requests.get("http://localhost:8000/projects/")
    projects_data=response.json()['projects']
    
    if projects_data:
        projects_df=pd.DataFrame(projects_data)

