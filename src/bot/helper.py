# Helper functions
import html
import requests
from io import BytesIO
from logging import currentframe
from telegram import InlineKeyboardButton

def serialize_title(title):
  book_formats = ["epub", "mobi", "pdf"]
  current_book_format = [fmt for fmt in book_formats if fmt in title]
  title = f'{title.replace(current_book_format[0], "")} ({current_book_format[0]})'
  return title

def get_raw_data_from_url(url):
  res = requests.get(url)
  raw_bytes_stream = BytesIO(res.content)
  return raw_bytes_stream

def get_inline_keboard_books(books, offset=5):
  # 5 books per page
  keyboard = list()
  for book in books[offset:offset+5]:
    keyboard.append(
      [InlineKeyboardButton(f"📔 {serialize_title(html.unescape(book['title']))}", callback_data=book['id'])]
    )
  keyboard.append([InlineKeyboardButton("<", callback_data="back"), InlineKeyboardButton(">", callback_data="forward")])
  return keyboard