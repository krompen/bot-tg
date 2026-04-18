import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Start command handler
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your Telegram bot. How can I assist you today?')

# Help command handler
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('You can use the following commands to interact with me:
/start - Start the bot
/help - Get help')

# Echo message handler
def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)

# Error handler
def error(update: Update, context: CallbackContext) -> None:
    logger.error('Update %s caused error %s', update, context.error)

# Main function to start the bot
if __name__ == '__main__':
    # Set up the Updater with your bot token
    updater = Updater('YOUR_TOKEN_HERE')

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()  

    # Run the bot until you send a signal to stop
    updater.idle()