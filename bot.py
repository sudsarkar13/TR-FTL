import os
import requests
import tempfile
from telegram import Update, Document
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

# Define your Vercel deployment URL
VERCEL_DEPLOYMENT_URL = 'https://tr-ftl.vercel.app/'

def convert_file(update: Update, context: CallbackContext) -> None:
    # Get the file from the message
    file = context.bot.get_file(update.message.document.file_id)
    
    # Download the file to a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, file.file_path)
        file.download(file_path)
        
        # Convert the file using your Vercel deployment
        response = requests.post(VERCEL_DEPLOYMENT_URL, files={'file': open(file_path, 'rb')})
        response.raise_for_status()
        
        # Send the user a message containing the download and streaming link
        link = response.json().get('link')
        update.message.reply_text(f"Here is your high-speed download and streaming link: {link}")

def main() -> None:
    # Set up the Telegram bot using your bot token
    updater = Updater("5431499256:AAH2Zo0zw_bWgLQr9z_cDa4G4U_masSDlco")
    dispatcher = updater.dispatcher
    
    # Set up a handler for file messages
    file_handler = MessageHandler(Filters.document.category('video'), convert_file)
    dispatcher.add_handler(file_handler)
    
    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
