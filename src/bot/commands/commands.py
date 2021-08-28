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
        update.message.reply_text("Ciao", reply_markup=inline_keyboard_message)
    else:
        print("No results found ! ")

def inline_button(update, context) -> None:
    query = update.callback_query.data
    
    if "download" in query:
        # Dowload book
        download_id = query.split("=")[1]
        doc = get_buffer_book_download(download_id)
        # TODO: fix filename part
        update.callback_query.message.reply_document(doc, filename="test.epub")
    else:
        # get book info
        # book_info = get_book_info(query)
        # book_cover = get_book_media_from_id(book_info["featured_media"])
        book_data = get_book_info(query)
        book_infos = get_complete_book_data(book_data)

        # TODO: creare una funzione per ottenere tutti i dati necessari
        # da inviare nel messaggio -> serializzare i dati se necessario. es: titolo

        book_message = f"""\n📚 *Book Infos*\n\n*Title*: {serialize_title(html.unescape(book_infos["title"]["rendered"]))}\n*Author*: {book_infos['author']}\n*Release Date*: {book_infos['year']}\n*Publisher*: {book_infos['publisher']}"""
        update.callback_query.message.reply_photo(photo=book_infos["cover"], caption=book_message, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"⬇️ Download", callback_data=f"download={book_infos['id']}")]]))
