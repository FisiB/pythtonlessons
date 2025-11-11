import streamlit as st
import requests
import pandas as pd

st.title("📚 Book Creation App")

# ---- Add Writer ----
st.header("Add Writer")
writer_name = st.text_input("Writer Name")

if st.button("Create Writer"):
    writer_data = {"name": writer_name}
    response = requests.post("http://localhost:8000/writers/", json=writer_data)
    try:
        st.json(response.json())
    except Exception:
        st.error(f"Invalid response: {response.text}")


# ---- Add Book ----
st.header("Add Book")
book_title = st.text_input("Book Title")
book_desc = st.text_area("Book Description")
lead_writer = st.text_input("Lead Writer Name")

if st.button("Create Book"):
    book_data = {
        "title": book_title,
        "description": book_desc,
        "lead_writer": {"name": lead_writer}
    }
    response = requests.post("http://localhost:8000/books/", json=book_data)
    try:
        st.json(response.json())
    except Exception:
        st.error(f"Invalid response: {response.text}")


# ---- Book Dashboard ----
st.header("Book Dashboard")

if st.button("Get Books"):
    response = requests.get("http://localhost:8000/books/")
    try:
        data = response.json()
        books_data = data.get("books", [])
    except Exception as e:
        st.error(f"Error decoding JSON: {e}")
        st.write(response.text)
        books_data = []

    if books_data:
        book_df = pd.DataFrame(books_data)
        st.subheader("Books Overview")
        st.dataframe(book_df)

        st.subheader("Book Details")
        for project in books_data:
            st.markdown(f"**Title:** {project['title']}")
            st.markdown(f"**Description:** {project['description']}")
            st.markdown(f"**Lead Writer:** {project['lead_writer']['name']}")
            st.markdown("---")
    else:
        st.warning("No books found.")
