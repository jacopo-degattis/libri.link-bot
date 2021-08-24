from commands.api.core import *
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
    
    book_info = get_book_info(query)
    book_cover = get_book_media_from_id(book_info["featured_media"])

    # TODO: creare una funzione per ottenere tutti i dati necessari
    # da inviare nel messaggio -> serializzare i dati se necessario. es: titolo

    book_message = f"""\n📚 *Book Infos*\n\n*Title*: {serialize_title(html.unescape(book_info["title"]["rendered"]))}"""
    update.callback_query.message.reply_photo(photo=book_cover, caption=book_message, parse_mode='Markdown')
