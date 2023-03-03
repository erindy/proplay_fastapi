from typing import Optional

from fastapi import FastAPI
from enum import Enum
app = FastAPI()

BOOKS = {
    'book_1': {'title': 'Title One', 'author': 'Author One'},
'book_2': {'title': 'Title One', 'author': 'Author One'},
'book_3': {'title': 'Title One', 'author': 'Author One'},
'book_4': {'title': 'Title One', 'author': 'Author One'}
}


class DirectionName(str, Enum):
    north = "North"
    south = "South"
    east = "East"
    west = "West"

@app.get("/")
async def read_all_books(skip_book: Optional[str]=None):
    if skip_book:
        new_books = BOOKS.copy()
        del new_books[skip_book]
        return new_books
    return BOOKS

@app.get("/directions/{direction_name}")
async def get_direction(direction_name: DirectionName):
    return {"Direction": direction_name.north}


@app.get("/books/{book_id}")
async def read_book(book_id: int):
    return {"book_title": book_id}

@app.get("/{book_name}")
async def read_book(bookname: str):
    return BOOKS[bookname]

@app.post("/")
async def create_book(book_title, book_author):
    current_book_id = 0
    if len(BOOKS) > 0:
        for book in BOOKS:
            x = int(book.split('_')[-1])
            if x > current_book_id:
                current_book_id = x
    BOOKS[f'book_{current_book_id + 1}'] = {'title': book_title, 'author': book_author}
    return BOOKS[f'book_{current_book_id + 1}']

@app.put("/{book_name}")
async def update_book(book_name: str, book_title: str, book_author: str):
    book_information = {'title': book_title, 'author': book_author}
    BOOKS[book_name] = book_information
    return book_information 