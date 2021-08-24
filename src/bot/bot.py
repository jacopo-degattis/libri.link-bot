from config import TOKEN
from commands.commands import start, search
from telegram import InlineKeyboardButton, InlineKeyboardMarkup,Update, Bot, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, CallbackContext

def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("search", search))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    bot = Bot(TOKEN)
    main()
