from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
from traceback import print_exc

# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! This is my first telegram bot!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    c = update.message.text
    update.message.reply_text("You Said: " + c)


def convert_image(update, context):
    filename = "test.jpg"
    file_id = update.message.photo[-1].file_id
    newFile = context.bot.get_file(file_id)
    newFile.download(filename)
    update.message.reply_text("Image received!!!")

    # Simple image to string
    try:
        extracted_string = (pytesseract.image_to_string(Image.open(filename)))
        if extracted_string is not None:
            update.message.reply_text("Extracted text: " + extracted_string)
        else:
            update.message.reply_text("Could not detect text")
    except Exception:
        print_exc()




def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    key = os.environ.get("token","")
    updater = Updater(key, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    dispatcher.add_handler(MessageHandler(Filters.photo, convert_image))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
