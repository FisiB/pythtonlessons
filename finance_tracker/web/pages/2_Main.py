import streamlit as st
from web.helpers import get_session

st.title('🏠 Main Page')

username = get_session()
if not username:
    st.warning('Please login first on the Login page')
else:
    st.write(f'Welcome, **{username}**!')
    st.write('''
    This personal finance tracker allows you to:
    1. Convert currencies on the Currency page
    2. Add and view your Income and Expenses
    3. View Statistics and Charts
    4. Use other tools
    ''')
