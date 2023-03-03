from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from uuid import UUID

app = FastAPI()

class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(title="Description of the book",
                             max_length = 100,
                             min_length= 1)
    rating: int = Field(gt=-1, lt=101)

    class Config:
        schema_extra = {
            "example": {
                "id": "ad92e12f-3bbf-4deb-b6f5-474574263482",
                "title": "Computer science book",
                "author": "Erind Mehmeti",
                "description": "awesome book",
                "rating": 100
            }

        }

BOOKS = []

@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):
    if len(BOOKS) < 1:
         create_books_no_api()

    if books_to_return and len(BOOKS) >= books_to_return > 0:
        i = 1
        new_books = []
        while i <= books_to_return:
            new_books.append(BOOKS[i-1])
            i += 1
        return new_books
    return BOOKS



@app.get("/book/{book_id}")
async def read_book(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found_exception()

@app.put("/{book_id}")
async def update_book(book_id, book:Book):
    counter = 0
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            BOOKS[counter -1] = book
            return BOOKS[counter - 1]
    raise raise_item_cannot_be_found_exception()


@app.delete("/{book_id}")
async def delete_book(book_id: UUID):


    counter = 0
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            del BOOKS[counter-1]
            return f'ID:{book_id} deleted'

    raise raise_item_cannot_be_found_exception()

@app.post("/")
async def create_book(book: Book):
    BOOKS.append(book)
    return book

def create_books_no_api():
    book_1 = Book(id="ad92e12f-3bbf-4deb-b6f5-474574263482",
                  title = "Title 1",
                  author = "Author 1",
                  description = "Description 1",
                  rating = 60)
    book_2 = Book(id="ad82e12f-3bbf-4deb-b6f5-474574263482",
                  title = "Title 2",
                  author = "Author 2",
                  description = "Description 1",
                  rating = 60)
    book_3 = Book(id="ad32e12f-3bbf-4deb-b6f5-474574263482",
                  title = "Title 3",
                  author = "Author 3",
                  description = "Description 3",
                  rating = 60)
    book_4 = Book(id="ad52e12f-3bbf-4deb-b6f5-474574263482",
                  title = "Title 1",
                  author = "Author 1",
                  description = "Description 4",
                  rating = 60)
    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)


def raise_item_cannot_be_found_exception():
    return HTTPException(status_code=404, detail="Book not found",
                        headers={"X-Header-Error":
                                 "Nothing to be seen at the UUID"})