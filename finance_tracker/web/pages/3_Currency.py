import streamlit as st
from web.helpers import get_session
from analysis.finance_utils import convert_currency

st.title('💱 Currency Converter')

username = get_session()
if not username:
    st.warning('Please login first on the Login page')
else:
    amount = st.number_input('Amount', min_value=0.0, format='%f')
    rate = st.number_input('Exchange Rate', min_value=0.0, format='%f')
    if st.button('Convert'):
        result = convert_currency(amount, rate)
        st.success(f'Converted amount: {result:.2f}')
