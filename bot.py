import telebot
from flask import Flask, request
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
    try:
        # Determine the file type and get relevant attributes
        if message.content_type == 'document':
            file_name = message.document.file_name
            file_size = message.document.file_size
        elif message.content_type == 'video':
            file_name = message.video.file_name if hasattr(message.video, 'file_name') else 'video.mp4'
            file_size = message.video.file_size
        elif message.content_type == 'audio':
            file_name = message.audio.file_name if hasattr(message.audio, 'file_name') else 'audio.mp3'
            file_size = message.audio.file_size
        else:
            bot.reply_to(message, "Unsupported file type")
            return

        # Generate links (replace with your actual link generation logic)
        download_link = f"https://technoranch.com/download/{file_name}"
        streamable_link = f"https://technoranch.com/stream/{file_name}"
        
        response = f"File Name: {file_name}\n"
        response += f"📦File Size: {file_size} bytes\n"
        response += f"💌Download link: {download_link}\n"
        response += f"💻Watch online: {streamable_link}\n"
        
        # Create buttons for download and watch
        markup = telebot.types.InlineKeyboardMarkup()
        download_button = telebot.types.InlineKeyboardButton(text="⚡DOWNLOAD⚡", url=download_link)
        watch_button = telebot.types.InlineKeyboardButton(text="⚡WATCH⚡", url=streamable_link)
        markup.add(download_button, watch_button)
        
        bot.send_message(message.chat.id, response, reply_markup=markup)
    
    except Exception as e:
        bot.reply_to(message, f"Error processing file: {str(e)}")

# Define the route for receiving updates via webhook
@app.route(WEBHOOK_PATH, methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

@app.route('/')
def index():
    return 'Bot is running!'

if __name__ == '__main__':
    # For development only
    app.run(host='0.0.0.0', 
            port=int(os.environ.get('PORT', 5000)),
            ssl_context='adhoc')