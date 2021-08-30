import json
from commands.api.core import search as search_book, get_book_info, get_book_media_from_id
from helper import *
from telegram import InlineKeyboardMarkup

def start(update, context) -> None:
    update.message.reply_text("Welcome")

def search(update, context) -> None:
    search_query = " ".join(update.message.text.split(" ")[1:])
    
    loading = update.message.reply_text("Fetcing books...")
    query_results = search_book(search_query)
    
    if len(query_results) > 0:
        inline_keyboard_message = InlineKeyboardMarkup(
            get_inline_keboard_books(query_results)
        )
        loading.delete()
        update.message.reply_text("Search results", reply_markup=inline_keyboard_message)
    else:
        update.message.reply_text("No books found !")

def inline_button(update, context) -> None:
    query = update.callback_query.data
    print(query)
    
    if "download" in query:
        # Dowload book
        current_book_id = query.split("=")[1]
        book_title = get_book_info(current_book_id)["title"]["rendered"]
        extension = current_book_format = [fmt for fmt in ["epub", "mobi", "pdf"] if fmt in book_title]
        book_title = serialize_title(html.unescape(book_title))
        book_title = book_title.replace(f"–  ({extension[0]})", "")
        book_title = book_title.replace("–", "-")
        doc = get_buffer_book_download(current_book_id)
        update.callback_query.message.reply_document(doc, filename=f"{book_title}.{extension[0]}")
    else:
        # get book info
        # book_info = get_book_info(query)
        # book_cover = get_book_media_from_id(book_info["featured_media"])
        book_data = get_book_info(query)
        i = book_infos = get_complete_book_data(book_data)
    
        # TODO: creare una funzione per ottenere tutti i dati necessari
        # da inviare nel messaggio -> serializzare i dati se necessario. es: titolo
        book_message = f"""\n📚 *Book Infos*\n\n*Title*: {serialize_title(html.unescape(book_infos["title"]["rendered"]))}\n*Author*: {book_infos['author']}\n*Release Date*: {book_infos['year']}\n*Publisher*: {book_infos['publisher']}"""
        update.callback_query.message.reply_photo(photo=book_infos["cover"], caption=book_message, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"⬇️ Download", callback_data=f"download={i['id']}")]]))
