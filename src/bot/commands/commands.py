from commands.api.core import *
from commands.api.core import search as search_book

def start(update, context) -> None:
    update.message.reply_text("Welcome")

def search(update, context) -> None:
    search_query = " ".join(update.message.text.split(" ")[1:])
    query_results = search_book(search_query)
    if len(query_results) > 0:
        print(query_results)
    else:
        print("No results found ! ")