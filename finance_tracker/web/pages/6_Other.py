import streamlit as st
from web.helpers import get_session

st.title('⚙️ Other Tools')

username = get_session()
if not username:
    st.warning('Please login first on the Login page')
else:
    st.write('Here you can add more tools or future features!')
