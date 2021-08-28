# Helper functions
import html
import requests
from io import BytesIO
from logging import currentframe
from telegram import InlineKeyboardButton
from commands.api.core import *

def serialize_title(title):
  book_formats = ["epub", "mobi", "pdf"]
  current_book_format = [fmt for fmt in book_formats if fmt in title]
  title = f'{title.replace(current_book_format[0], "")} ({current_book_format[0]})'
  return title

def get_raw_data_from_url(url):
  res = requests.get(url)
  raw_bytes_stream = BytesIO(res.content)
  return raw_bytes_stream

def __fetch_taxonomies(taxonomies):
  data = dict()
  taxonomies_black_list = ["category", "post_tag"]
  for tax in taxonomies:
    if tax["taxonomy"] not in taxonomies_black_list:
      res = requests.get(tax["href"]).json()
      data[tax["taxonomy"]] = res
  return data

def get_complete_book_data(book_data):
  # Function to get all necessary data for the book

  # Fetch author info
  taxonomies = book_data["_links"]["wp:term"]
  taxonomies_info = __fetch_taxonomies(taxonomies)
  
  # TODO: add support for more than one author, genre, publisher etc.
  # TODO: improve function, better algorithm
  book_data["year"] = taxonomies_info["anno"][0]["name"] if len(taxonomies_info["anno"]) > 0 else "Unknown"
  book_data["author"] = " ".join(taxonomies_info["autore"][0]["name"].split("-")).title() if len(taxonomies_info["autore"]) > 0 else "Unknown"
  print(taxonomies_info["genere"])
  book_data["genre"] = taxonomies_info["genere"][0]["name"] if len(taxonomies_info["genere"]) > 0 else None
  book_data["publisher"] = " ".join(taxonomies_info["editore"][0]["name"].split("-")).title() if len(taxonomies_info["editore"]) > 0 else "Unknown"
  book_data["cover"] = get_book_media_from_id(book_data["featured_media"])

  return book_data

def get_buffer_book_download(book_id):
  uri = get_book_download_uri(book_id)[0]
  document = get_raw_data_from_url(uri)
  return document

def get_inline_keboard_books(books, offset=5):
  # 5 books per page
  keyboard = list()
  for book in books[offset:offset+5]:
    keyboard.append(
      [InlineKeyboardButton(f"📔 {serialize_title(html.unescape(book['title']))}", callback_data=book['id'])]
    )
  keyboard.append([InlineKeyboardButton("<", callback_data="back"), InlineKeyboardButton(">", callback_data="forward")])
  return keyboard
