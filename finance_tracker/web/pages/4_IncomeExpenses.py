import streamlit as st
from web.helpers import get_session
from analysis.finance_utils import add_transaction, get_transactions
from datetime import datetime
import pandas as pd

st.title('💳 Income & Expenses')

username = get_session()
if not username:
    st.warning('Please login first on the Login page')
else:
    t_type = st.selectbox('Transaction Type', ['income','expense'])
    category = st.text_input('Category')
    amount = st.number_input('Amount', min_value=0.0, format='%f')
    date = st.date_input('Date', datetime.today())

    if st.button('Add Transaction'):
        add_transaction(username, t_type, category, amount, date.strftime('%Y-%m-%d'))
        st.success('Transaction added!')

    st.subheader('Your Transactions')
    df = get_transactions(username)
    if df is None or df.empty:
        st.info('No transactions yet.')
    else:
        st.dataframe(df)
