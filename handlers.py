from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Command handler for the /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your bot. How can I assist you today?')

# Command handler for the /help command
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Here are the commands you can use:\n/start - Start the bot\n/help - Get help')

# Handler for text messages
def handle_message(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('You said: {}'.format(update.message.text))

def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater("YOUR_TOKEN")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    # Register message handler
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start polling for updates
    updater.start_polling()

    # Run the bot until you send a signal to stop
    updater.idle()

if __name__ == '__main__':
    main()