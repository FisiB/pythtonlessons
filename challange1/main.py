from fastapi import FastAPI, HTTPException
from typing import List
import database
import models
from models import Books, BooksCreate

app = FastAPI()

@app.get('/')
def read_root():
    return {"message": "Welcome to the Books CRUD app"}

# CREATE -------------------------------------
@app.post('/books/', response_model=Books)
def create_book(book: BooksCreate):
    # Create the book in the database and return it
    connection = database.get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO books (title, director) VALUES (?, ?)", 
                   (book.title, book.director))
    connection.commit()
    book_id = cursor.lastrowid
    connection.close()
    return Books(id=book_id, **book.dict())

# READ ALL -----------------------------------
@app.get('/books/', response_model=List[Books])
def get_all_books():
    connection = database.get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    connection.close()
    books = [Books(id=row["id"], title=row["title"], director=row["director"]) for row in rows]
    return books

# READ ONE -----------------------------------
@app.get('/books/{book_id}', response_model=Books)
def get_book(book_id: int):
    connection = database.get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    row = cursor.fetchone()
    connection.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return Books(id=row["id"], title=row["title"], director=row["director"])

# UPDATE --------------------------------------
@app.put('/books/{book_id}', response_model=Books)
def update_book(book_id: int, book: BooksCreate):
    connection = database.get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE books SET title = ?, director = ? WHERE id = ?", 
                   (book.title, book.director, book_id))
    connection.commit()
    connection.close()
    return Books(id=book_id, **book.dict())

# DELETE --------------------------------------
@app.delete('/books/{book_id}', response_model=dict)
def delete_book(book_id: int):
    connection = database.get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    connection.commit()
    connection.close()
    return {"message": "Book deleted successfully"}
