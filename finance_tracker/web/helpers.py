import streamlit as st

def set_session(username: str) -> None:
    st.session_state['username'] = username

def get_session() -> str:
    return st.session_state.get('username', None)

def clear_session() -> None:
    if 'username' in st.session_state:
        del st.session_state['username']
