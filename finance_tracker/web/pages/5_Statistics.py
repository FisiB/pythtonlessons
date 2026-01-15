import streamlit as st
from web.helpers import get_session
from analysis.finance_utils import get_transactions
from analysis.visualization import monthly_expenses_figure, category_pie_figure
import pandas as pd

st.title('📊 Statistics & Charts')

username = get_session()
if not username:
    st.warning('Please login first on the Login page')
else:
    df = get_transactions(username)
    if df is None or df.empty:
        st.info('No transactions to show statistics for.')
    else:
        st.subheader('Raw transactions')
        st.dataframe(df)

        fig = monthly_expenses_figure(df)
        if fig:
            st.subheader('Monthly Expenses')
            st.pyplot(fig)

        fig2 = category_pie_figure(df)
        if fig2:
            st.subheader('Expenses by Category')
            st.pyplot(fig2)
