import streamlit as st
from analysis.finance_utils import login_user, register_user
from web.helpers import set_session

st.title('🔐 Login / Sign Up')

choice = st.radio('Choose action:', ['Login', 'Sign Up'])

username = st.text_input('Username')
password = st.text_input('Password', type='password')

if st.button('Submit'):
    if not username or not password:
        st.error('Username and password are required')
    elif choice == 'Sign Up':
        success = register_user(username, password)
        if success:
            st.success('User registered! You can login now.')
        else:
            st.error('Username already exists')
    else:
        success = login_user(username, password)
        if success:
            set_session(username)
            st.success('Login successful! Go to Main page.')
        else:
            st.error('Invalid credentials')
