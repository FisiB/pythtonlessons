import streamlit as st
import requests
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv

load_dotenv()

API_HOST = os.getenv("API_HOST", "http://127.0.0.1:8000")

st.set_page_config(page_title="Finance Tracker", layout="wide")

# --- Session Helpers ---
def set_token(token: str, username: str):
    st.session_state["token"] = token
    st.session_state["username"] = username

def get_token():
    return st.session_state.get("token")

def get_username():
    return st.session_state.get("username")

def clear_session():
    # Clean up all session state
    keys_to_delete = ["token", "username", "tx_tab"]
    for k in keys_to_delete:
        if k in st.session_state:
            del st.session_state[k]

def auth_headers():
    token = get_token()
    if not token:
        return {}
    return {"Authorization": f"Bearer {token}"}

# ==========================================
# LOGGED OUT SECTION
# ==========================================
if not get_token():
    st.title("💰 Finance Tracker Login")
    
    col1, col2 = st.columns(2)
    with col1:
        with st.form("login_form"):
            st.subheader("Login")
            lu = st.text_input("Username")
            lp = st.text_input("Password", type="password")
            submitted_login = st.form_submit_button("Login", use_container_width=True)
            
        if submitted_login:
            try:
                r = requests.post(f"{API_HOST}/auth/login", json={"username": lu, "password": lp}, timeout=8)
                if r.status_code == 200:
                    token = r.json().get("access_token")
                    if token:
                        set_token(token, lu)
                        st.success("Logged in successfully!")
                        st.rerun()
                    else:
                        st.error("Login failed: No token received.")
                else:
                    st.error(r.json().get("detail", "Invalid credentials"))
            except Exception as e:
                st.error(f"Connection Error: {e}")

    with col2:
        with st.form("signup_form"):
            st.subheader("Sign Up")
            su = st.text_input("Choose username", key="su")
            sp = st.text_input("Choose password", type="password", key="sp")
            submitted_signup = st.form_submit_button("Sign Up", use_container_width=True)
            
        if submitted_signup:
            try:
                r = requests.post(f"{API_HOST}/auth/register", json={"username": su, "password": sp}, timeout=8)
                if r.status_code in (200, 201):
                    st.success("Account created! Please log in.")
                else:
                    st.error(r.json().get("detail", "Sign up failed"))
            except Exception as e:
                st.error(f"Connection Error: {e}")
    st.stop() 

# ==========================================
# LOGGED IN SECTION
# ==========================================
username = get_username()

st.sidebar.title(f"👋 {username}")

# Persistent Menu
if "tx_tab" not in st.session_state:
    st.session_state["tx_tab"] = "Add New"

menu = st.sidebar.radio("Navigate", ["Home", "Transactions", "Budget Goals", "Currency Converter", "Logout"])

# Helper function to fetch transactions
@st.cache_data(ttl=60) 
def fetch_transactions(token):
    if not token:
        return None
    headers = {"Authorization": f"Bearer {token}"}
    try:
        r = requests.get(f"{API_HOST}/transactions/me", headers=headers, timeout=8)
        if r.status_code == 200:
            return r.json()
        else:
            return None
    except Exception as e:
        return None

# 1. HOME PAGE
if menu == "Home":
    st.title("🏠 Welcome Back!")
    st.markdown(f"Hello **{username}**, here is your financial overview.")
    
    txs = fetch_transactions(get_token())
    
    if txs:
        df = pd.DataFrame(txs)
        df["amount"] = df["amount"].astype(float)
        
        total_income = df[df["type"] == "income"]["amount"].sum()
        total_expense = df[df["type"] == "expense"]["amount"].sum()
        balance = total_income - total_expense
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Balance", f"${balance:,.2f}", delta=f"${balance:,.2f}")
        c2.metric("Total Income", f"${total_income:,.2f}", delta_color="normal")
        c3.metric("Total Expenses", f"${total_expense:,.2f}", delta_color="inverse")
        
        st.info("👉 Use the sidebar to navigate to **Transactions** to manage your money or **Budget Goals** to track targets.")
    else:
        st.warning("No transaction data found.")

# 2. TRANSACTIONS
elif menu == "Transactions":
    st.title("💳 Manage Transactions")
    
    txs = fetch_transactions(get_token())
    df = pd.DataFrame(txs) if txs else pd.DataFrame()
    
    # Use Radio Button for Tabs to persist state
    tx_tab = st.radio("Select Action", ["Add New", "Charts", "History & Edit"], horizontal=True, label_visibility="collapsed")

    if tx_tab == "Add New":
        with st.form("tx_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            with col_a:
                ttype = st.selectbox("Type", ["income", "expense"])
                amount = st.number_input("Amount", min_value=0.0, format="%.2f")
            with col_b:
                category = st.text_input("Category", placeholder="e.g. Food, Salary")
                date = st.date_input("Date")
            
            submitted = st.form_submit_button("Add Transaction", use_container_width=True, type="primary")
            
            if submitted:
                headers = auth_headers()
                try:
                    r = requests.post(
                        f"{API_HOST}/transactions", 
                        json={
                            "type": ttype, 
                            "category": category or "Misc", 
                            "amount": float(amount), 
                            "date": date.strftime("%Y-%m-%d")
                        }, 
                        headers=headers, 
                        timeout=8
                    )
                    if r.status_code == 200:
                        st.success("Transaction added successfully!")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        err = r.json().get("detail", r.text)
                        st.error(f"Failed to add: {err}")
                except Exception as e:
                    st.error(f"API Error: {e}")

    elif tx_tab == "Charts":
        if not df.empty:
            st.subheader("Financial Breakdown")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Income vs Expense**")
                inc_exp = df.groupby("type")["amount"].sum().reset_index()
                fig_pie = px.pie(inc_exp, values="amount", names="type", hole=0.5, 
                                 color_discrete_map={"income": "#00cc96", "expense": "#ef553b"})
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                st.write("**Expenses by Category**")
                expenses = df[df["type"] == "expense"]
                if not expenses.empty:
                    cat_data = expenses.groupby("category")["amount"].sum().reset_index().sort_values("amount", ascending=False)
                    fig_bar = px.bar(cat_data, x="category", y="amount", color="amount", 
                                     color_continuous_scale="Reds")
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.info("No expenses recorded yet.")
        else:
            st.info("Add transactions to see charts here.")

    elif tx_tab == "History & Edit":
        if not df.empty:
            st.dataframe(df.sort_values(by="date", ascending=False), use_container_width=True)
            
            st.markdown("---")
            col_edit, col_del = st.columns(2)
            
            with col_edit:
                st.subheader("✏️ Update Transaction")
                ids = df["id"].tolist()
                options = [f"{row['id']} | {row['date']} | ${row['amount']}" for _, row in df.iterrows()]
                
                sel_edit = st.selectbox("Select transaction to edit", options=[None] + options, key="edit_select")
                
                if sel_edit:
                    tx_id = int(sel_edit.split("|")[0].strip())
                    tx_data = df[df["id"] == tx_id].iloc[0]
                    
                    with st.form("edit_form", clear_on_submit=False):
                        edit_type = st.selectbox("Type", ["income", "expense"], 
                                                index=0 if tx_data["type"] == "income" else 1)
                        edit_amount = st.number_input("Amount", value=float(tx_data["amount"]), min_value=0.0, format="%.2f")
                        edit_category = st.text_input("Category", value=tx_data["category"])
                        from datetime import datetime
                        edit_date = st.date_input("Date", value=datetime.strptime(tx_data["date"], "%Y-%m-%d").date())
                        
                        if st.form_submit_button("Update Transaction", type="primary"):
                            payload = {
                                "type": edit_type,
                                "category": edit_category or "Misc",
                                "amount": float(edit_amount),
                                "date": edit_date.strftime("%Y-%m-%d")
                            }
                            try:
                                r = requests.put(f"{API_HOST}/transactions/{tx_id}", json=payload, headers=auth_headers(), timeout=8)
                                if r.status_code == 200:
                                    st.success("Transaction updated!")
                                    st.cache_data.clear()
                                    st.rerun()
                                else:
                                    st.error(f"Update failed: {r.json().get('detail', 'Unknown error')}")
                            except Exception as e:
                                st.error(f"API Error: {e}")

            with col_del:
                st.subheader("🗑️ Remove Transaction")
                sel_del = st.selectbox("Select ID to delete", options=[None] + ids, key="delete_select")
                if st.button("Delete Selected", type="secondary"):
                    if sel_del:
                        try:
                            r = requests.delete(f"{API_HOST}/transactions/{sel_del}", headers=auth_headers(), timeout=8)
                            if r.status_code == 200:
                                st.success("Transaction deleted!")
                                st.cache_data.clear()
                                st.rerun()
                            else:
                                st.error("Failed to delete.")
                        except Exception as e:
                            st.error(f"API Error: {e}")
        else:
            st.info("No transactions found.")

# 3. BUDGET GOALS (UPDATED TO SAVE TO DB)
elif menu == "Budget Goals":
    st.title("🎯 Budget Goals & Progress")
    
    # 1. Fetch the existing goal from the Database
    try:
        r = requests.get(f"{API_HOST}/me/goal", headers=auth_headers(), timeout=8)
        if r.status_code == 200:
            current_goal_value = r.json().get("goal", 1000.0)
        else:
            current_goal_value = 1000.0
    except:
        current_goal_value = 1000.0

    # 2. Display the input field pre-filled with the DB value
    with st.expander("Set your Savings Goal", expanded=True):
        new_goal = st.number_input("Monthly Savings Target ($)", min_value=0.0, value=current_goal_value)
        
        # 3. When clicked, send the NEW value to the Database
        if st.button("Update Goal"):
            try:
                r = requests.put(f"{API_HOST}/me/goal", json={"amount": float(new_goal)}, headers=auth_headers(), timeout=8)
                if r.status_code == 200:
                    st.success("Goal saved to database!")
                    st.rerun() # Refresh to show the new saved value
                else:
                    st.error("Failed to save goal.")
            except Exception as e:
                st.error(f"Error: {e}")

    # Fetch Data for Charts
    txs = fetch_transactions(get_token())
    
    # Use the value we just fetched from DB for the chart
    goal = current_goal_value

    if txs:
        df = pd.DataFrame(txs)
        df["date"] = pd.to_datetime(df["date"])
        df["amount"] = df["amount"].astype(float)
        
        now = pd.Timestamp.now()
        current_month_data = df[(df["date"].dt.month == now.month) & (df["date"].dt.year == now.year)]
        
        if current_month_data.empty:
            st.warning("No transactions for **this month** yet. Showing all-time progress.")
            data_source = df
            period_label = "(All Time)"
        else:
            data_source = current_month_data
            period_label = "(This Month)"

        income = data_source[data_source["type"] == "income"]["amount"].sum()
        expenses = data_source[data_source["type"] == "expense"]["amount"].sum()
        current_savings = income - expenses
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Income", f"${income:,.2f}")
        m2.metric("Expenses", f"${expenses:,.2f}")
        m3.metric("Net Savings", f"${current_savings:,.2f}", delta=f"${current_savings:,.2f}")

        if goal > 0:
            percentage = (current_savings / goal) * 100
        else:
            percentage = 0

        st.subheader(f"Progress to Goal: ${goal:,.2f} {period_label}")
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = current_savings,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': f"Saved (${current_savings:,.2f})"},
            delta = {'reference': goal},
            gauge = {
                'axis': {'range': [None, goal * 1.2]}, 
                'bar': {'color': "#00cc96"},
                'steps': [
                    {'range': [0, goal], 'color': "lightgray"},
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': goal 
                }
            }
        ))
        
        st.plotly_chart(fig, use_container_width=True)

        if current_savings >= goal:
            st.success("🎉 Amazing! You have reached your savings goal!")
        elif current_savings < 0:
            st.error("⚠️ You are in a deficit. Review your expenses.")
        else:
            amount_left = goal - current_savings
            st.info(f"💡 You need to save **${amount_left:,.2f}** more to reach your goal.")

    else:
        st.info("No data available. Add transactions to track your budget.")

# 4. CURRENCY CONVERTER
elif menu == "Currency Converter":
    st.title("💱 Currency Converter")
    st.write("Convert between Fiat Currencies and Cryptocurrencies using live data.")
    
    currencies = {
        "USD": "US Dollar", "EUR": "Euro", "GBP": "British Pound", "JPY": "Japanese Yen",
        "CAD": "Canadian Dollar", "AUD": "Australian Dollar", "CHF": "Swiss Franc",
        "CNY": "Chinese Yuan", "INR": "Indian Rupee", "BTC": "Bitcoin", "ETH": "Ethereum",
        "SOL": "Solana", "DOGE": "Dogecoin", "XRP": "Ripple", "ADA": "Cardano", "DOT": "Polkadot",
    }
    
    col1, col2, col3 = st.columns(3)
    with col1:
        frm = st.selectbox("From", options=list(currencies.keys()), format_func=lambda x: currencies[x], index=0)
    with col2:
        to = st.selectbox("To", options=list(currencies.keys()), format_func=lambda x: currencies[x], index=1)
    with col3:
        amt = st.number_input("Amount", min_value=0.0, value=1.0)
    
    if st.button("Convert", use_container_width=True):
        try:
            r = requests.get(f"{API_HOST}/scrape-currency", params={"frm": frm, "to": to}, timeout=10)
            if r.status_code == 200:
                data = r.json()
                rate = float(data.get("rate"))
                res = amt * rate
                st.success(f"Exchange Rate (Source: {data.get('source')}): 1 {frm} = {rate} {to}")
                st.metric(f"{amt} {frm}", f"{res:,.4f} {to}")
                if "note" in data:
                    st.caption(f"Note: {data['note']}")
            else:
                st.error("Failed to fetch rate. The currency pair might not exist on Yahoo Finance.")
        except Exception as e:
            st.error(f"Error: {e}")

# 5. LOGOUT
elif menu == "Logout":
    clear_session()
    st.cache_data.clear()
    st.success("Logged out successfully.")
    st.rerun()