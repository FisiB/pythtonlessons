import streamlit as st
from analysis.finance_utils import init_db

# Initialize DB when the app starts
init_db()

st.set_page_config(page_title='Personal Finance Tracker', layout='wide')
st.title('💰 Personal Finance Tracker')
st.write('Use the left sidebar to navigate between pages.')

st.sidebar.title('Navigation')
st.sidebar.info('Open the pages from the sidebar: Login, Main, Currency, Income/Expenses, Statistics, Other')
