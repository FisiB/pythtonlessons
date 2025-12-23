import streamlit as st
import pandas as pd
import requests
import plotly.express as px

API_URL = "http://localhost:8000"
st.set_page_config(layout="wide")

# ---------------- LOGIN ----------------
st.title("⚽ Football Analytics Login")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.admin = False

if not st.session_state.logged_in:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        res = requests.post(f"{API_URL}/login", json={"username": username, "password": password}).json()
        if "error" in res:
            st.error("Invalid username or password")
        else:
            st.session_state.logged_in = True
            st.session_state.username = res["username"]
            st.session_state.admin = res.get("admin", False)
            st.success(f"Welcome, {st.session_state.username}!")
            st.experimental_rerun()
else:
    # ---------------- SIDEBAR ----------------
    option = st.sidebar.radio(
        "Navigation",
        ["Home", "Search Players", "Favorite XI", "Favorite Players Stats", "Manage Articles"]
    )

    # ---------------- HOME ----------------
    if option == "Home":
        st.title("⚽ Welcome to Football Analytics Website")
        st.subheader(f"Hello {st.session_state.username}!")
        st.write("Scroll down to see the latest football articles:")

        articles = requests.get(f"{API_URL}/articles").json()
        for art in articles:
            with st.expander(f"{art['title']} (by {art['author']})"):
                st.write(art["content"])

    # ---------------- SEARCH PLAYERS ----------------
    elif option == "Search Players":
        st.subheader("🔍 Search Footballer")
        name = st.text_input("Enter footballer name")
        if st.button("Search"):
            res = requests.get(f"{API_URL}/player-info", params={"name": name}).json()
            if "error" in res:
                st.error("Player not found")
            else:
                st.success(res["name"])
                st.write(res["summary"])

    # ---------------- FAVORITE XI ----------------
    elif option == "Favorite XI":
        st.subheader("🏟️ Build Your Favorite XI")
        players = [p["Player"] for p in requests.get(f"{API_URL}/players").json()]
        selected_players = st.multiselect("Select 11 Players", players)

        if st.button("Save Favorite XI"):
            if len(selected_players) != 11:
                st.error("Select exactly 11 players!")
            else:
                requests.post(f"{API_URL}/favorite-xi",
                              json={"username": st.session_state.username, "player_list": selected_players})
                st.success("Favorite XI saved!")

        if st.button("View My XI"):
            res = requests.get(f"{API_URL}/favorite-xi/{st.session_state.username}").json()
            if "player_list" in res:
                st.write(res["player_list"])
            else:
                st.warning("No favorite XI found.")

        if st.button("Delete My XI"):
            requests.delete(f"{API_URL}/favorite-xi/{st.session_state.username}")
            st.warning("Favorite XI deleted.")

    # ---------------- FAVORITE PLAYERS STATS ----------------
    elif option == "Favorite Players Stats":
        st.subheader("📊 Favorite Players Stats")
        xi_res = requests.get(f"{API_URL}/favorite-xi/{st.session_state.username}").json()
        if "player_list" in xi_res:
            favorite_players = xi_res["player_list"]
            players_df = pd.DataFrame(requests.get(f"{API_URL}/players").json())
            fav_df = players_df[players_df["Player"].isin(favorite_players)]
            if not fav_df.empty:
                st.dataframe(fav_df[["Player", "Pos", "Gls", "Ast", "Squad", "Nation"]])
                fav_df["G+A"] = fav_df["Gls"] + fav_df["Ast"]
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Goals", fav_df["Gls"].sum())
                col2.metric("Total Assists", fav_df["Ast"].sum())
                col3.metric("Goals+Assists", fav_df["G+A"].sum())
            else:
                st.warning("No data found for your favorite players.")
        else:
            st.warning("You need to create your Favorite XI first.")

    # ---------------- MANAGE ARTICLES (ADMIN ONLY) ----------------
    elif option == "Manage Articles":
        if not st.session_state.admin:
            st.error("Only admins can manage articles")
        else:
            st.subheader("📝 Manage Articles (Admin Only)")

            # CREATE ARTICLE
            with st.expander("➕ Add New Article"):
                title = st.text_input("Title", key="create_title")
                content = st.text_area("Content", key="create_content")
                author = st.text_input("Author", key="create_author", value=st.session_state.username)
                if st.button("Publish Article"):
                    requests.post(f"{API_URL}/articles",
                                  json={"title": title, "content": content, "author": author},
                                  params={"admin": True})
                    st.success("Article published")

            # READ & UPDATE ARTICLES
            articles = requests.get(f"{API_URL}/articles").json()
            for art in articles:
                with st.expander(f"{art['title']} (by {art['author']})"):
                    st.write(art["content"])
                    with st.form(f"update_{art['id']}"):
                        new_title = st.text_input("New Title", value=art["title"], key=f"title_{art['id']}")
                        new_content = st.text_area("New Content", value=art["content"], key=f"content_{art['id']}")
                        new_author = st.text_input("New Author", value=art["author"], key=f"author_{art['id']}")
                        submitted = st.form_submit_button("Update Article")
                        if submitted:
                            requests.put(f"{API_URL}/articles/{art['id']}",
                                         json={"title": new_title, "content": new_content, "author": new_author},
                                         params={"admin": True})
                            st.success("Article updated")
                    if st.button(f"Delete Article", key=f"delete_{art['id']}"):
                        requests.delete(f"{API_URL}/articles/{art['id']}", params={"admin": True})
                        st.warning("Article deleted")
