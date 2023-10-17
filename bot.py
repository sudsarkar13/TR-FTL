import telebot
from flask import Flask, request
import os

# Define your environment variables
YOUR_API_TOKEN = os.environ.get('YOUR_API_TOKEN')
HTML_PAGE_URL = os.environ.get('HTML_PAGE_URL')
WEBHOOK_PATH = os.environ.get('WEBHOOK_PATH')

# Initialize the Flask app
app = Flask(__name__)

# Initialize your bot with your API token
bot = telebot.TeleBot(YOUR_API_TOKEN)

# Define the main menu keyboard
main_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.row('Start')

# Configure the webhook URL for your bot
webhook_url = f'https://api.telegram.org/bot{YOUR_API_TOKEN}/setWebhook?url={HTML_PAGE_URL}{WEBHOOK_PATH}'

# Set up the webhook
bot.remove_webhook()  # Remove any existing webhook configuration
bot.set_webhook(url=webhook_url)  # Set the new webhook URL

# Print the webhook URL for reference (optional)
print(f'Webhook URL: {webhook_url}')

# Define a handler for /start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Welcome to your bot!", reply_markup=main_menu)

# Define a handler for receiving files
@bot.message_handler(content_types=['document', 'video', 'audio'])
def handle_files(message):
    # Process the received file and generate download and streamable links
    # For simplicity, let's assume you have the download and streamable links
    download_link = "https://technoranch.com/download"
    streamable_link = "https://technoranch.com/stream"
    
    response = f"File Name: {message.document.file_name}\n"
    response += f"📦File Size: {message.document.file_size} bytes\n"
    response += f"💌Download link: {download_link}\n"
    response += f"💻Watch online: {streamable_link}\n"
    
    # Create buttons for download and watch
    markup = telebot.types.InlineKeyboardMarkup()
    download_button = telebot.types.InlineKeyboardButton(text="⚡DOWNLOAD⚡", url=download_link)
    watch_button = telebot.types.InlineKeyboardButton(text="⚡WATCH⚡", url=streamable_link)
    markup.add(download_button, watch_button)
    
    bot.send_message(message.chat.id, response, reply_markup=markup)

# Define the route for receiving updates via webhook
@app.route(WEBHOOK_PATH, methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))