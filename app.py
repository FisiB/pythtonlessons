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

st.header("Add Project")
proj_title=st.text_input("Project title")
proj_desc=st.text_area("Project description")
proj_lang=st.text_input("Languages used")
lead_dev=st.text_input("Lead developer name")
lead_dev_exp=st.number_input("Lead developer experience",min_value=0,max_value=50,value=0)

if st.button("Create project"):
    lead_dev_data={"name":lead_dev,"experience":lead_dev_exp}
    proj_data={
        "title":proj_title,
        "description":proj_desc,
        "languages":proj_lang.split(","),
        "lead devs":lead_dev_data
    }
    response=requests.post("http://localhost:8000/projects/",json=proj_data)
    st.json(response.json())


st.header("Project Dashboard")

if st.button("Get Projects"):
    response=requests.get("http://localhost:8000/projects/")
    project_data=response.json()['projects']

    if project_data:
        project_df=pd.DataFrame(project_data)

        st.subheader("Project Overview")
        st.dataframe(project_df)

        st.subheader("Project Details")
        for project in project_data:
            st.markdown(f"Title {project['title']}")
            st.markdown(f"Description {project['description']}")
            st.markdown(f"Languages {project['languages']}")
            st.markdown(f"Lead developer {project['lead_developer']['name']} with {project['lead_developer']['experience']} years of experience")
            st.markdown("---------")
        else:
            st.warning("No Projects Found")