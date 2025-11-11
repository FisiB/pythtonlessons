from fastapi import FastAPI
from challange.models1 import BookCreate, Writer

app = FastAPI()

# ---- Writers ----
@app.post("/writers/")
def create_writer(writer: Writer):
    return {"message": "Writer was created successfully", "writer": writer}


# ---- Books ----
@app.post("/books/")
def create_book(book: BookCreate):
    return {"message": "Book was created successfully", "book": book}


@app.get("/books/")
def get_books():
    sample_book = BookCreate(
        title="Sample Project",
        description="Sample description",
        lead_writer=Writer(name="John Doe")
    )
    # Return consistent JSON structure
    return {"books": [sample_book]}
