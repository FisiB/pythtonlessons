import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"  # Ensure this matches your FastAPI URL

st.title("📚 Book Creation App")

# ---- Create Book ----
st.header("Add Book")

book_title = st.text_input("Title")
book_director = st.text_input("Director")

if st.button("Create Book"):
    book_data = {
        "title": book_title,
        "director": book_director
    }

    try:
        response = requests.post(f"{API_URL}/books/", json=book_data)
        if response.status_code == 200:
            st.success("Book created successfully!")
            st.json(response.json())
        else:
            st.error("Failed to create book")
            st.write(response.text)
    except Exception as e:
        st.error(f"Connection error: {e}")


# ---- Dashboard ----
st.header("Book Dashboard")

if st.button("Get Books"):
    try:
        response = requests.get(f"{API_URL}/books/")
        if response.status_code == 200:
            books_data = response.json()

            if books_data:
                df = pd.DataFrame(books_data)
                st.subheader("Books Overview")
                st.dataframe(df)

                st.subheader("Delete a Book")
                book_ids = [book["id"] for book in books_data]
                select_id = st.selectbox("Select Book ID to Delete", book_ids)

                if st.button("Delete Selected Book"):
                    delete_response = requests.delete(f"{API_URL}/books/{select_id}")
                    if delete_response.status_code == 200:
                        st.success("Book deleted!")
                        st.json(delete_response.json())
                    else:
                        st.error("Error during deletion.")
                        st.write(delete_response.text)
            else:
                st.warning("No books found.")
        else:
            st.error("Failed to retrieve books.")
            st.write(response.text)

    except Exception as e:
        st.error(f"Connection error: {e}")
