import os
import requests
import json
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from flask import Flask, request
from urllib.parse import quote

# Replace with your own Vercel deployment URL
NETLIFY_URL = 'https://tr-ftl-bot-technoranch.netlify.app'

# Welcome message for bot
WELCOME_MSG = "Welcome to File to Link Bot! Send me a video file and I'll generate a high-speed permanent download link and a streamable link for you."

# Guideline page of bot (Contains commands accepted by the bot)
GUIDELINE_PAGE = """
*Commands*
/start - Start the bot
/help - View the list of available commands
"""

# Text decoration
BOLD = "<b>"
ITALIC = "<i>"
CODE = "<code>"
PRE = "<pre>"
HTML_CLOSE_TAG = "</>"

# Set up the Telegram bot

def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=WELCOME_MSG, parse_mode=ParseMode.HTML)


def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=GUIDELINE_PAGE, parse_mode=ParseMode.MARKDOWN)


def handle_video(update, context):
    file_id = update.message.video.file_id
    file_name = update.message.video.file_name
    file_size = update.message.video.file_size
    chat_id = update.message.chat_id
    message_id = update.message.message_id

    # Generate a permanent download link
    res = requests.post(f'{NETLIFY_URL}/api/download',
                        data=json.dumps({'file_id': file_id}))
    download_link = res.json().get('url')
    file_size = res.json().get('size')

    # Generate a streamable link
    encoded_file_name = quote(file_name)
    streamable_link = f"{NETLIFY_URL}/stream?file_id={file_id}&file_name={encoded_file_name}&file_size={file_size}"

    # Send the response to the user
    response_text = f"File Name: {encoded_file_name}\nHere are the links for your video\n\n📦File Size: {file_size}\n{BOLD}💌Download link:{HTML_CLOSE_TAG} {download_link}\n{BOLD}💻Streamable link:{HTML_CLOSE_TAG} {streamable_link}\n{BOLD}♻️ THIS LINK IS PERMANENT AND WILL NOT EXPIRE ♻️"
    context.bot.send_message(chat_id=chat_id, text=response_text,reply_to_message_id=message_id, parse_mode=ParseMode.HTML)

    # Save the file and links to the garbage channel
    garbage_channel_id = os.environ.get('GARBAGE_CHANNEL_ID')
    garbage_channel_url = f"https://t.me/c/{garbage_channel_id}"
    response_text = f"{BOLD}User:{HTML_CLOSE_TAG} {update.message.from_user.mention_html()}\n{BOLD}File:{HTML_CLOSE_TAG} {file_name}\n{BOLD}Download link:{HTML_CLOSE_TAG} {download_link}\n{BOLD}Streamable link:{HTML_CLOSE_TAG} {streamable_link}"
    context.bot.send_message(chat_id=garbage_channel_id,
                             text=response_text, parse_mode=ParseMode.HTML)
    context.bot.send_message(
        chat_id=chat_id, text=f"File and links saved in {garbage_channel_url}", reply_to_message_id=message_id)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def join(update, context):
    """Join the updates channel"""
    updates_channel_id = os.environ.get('UPDATES_CHANNEL_ID')
    updates_channel_url = f"https://t.me/c/{updates_channel_id}"
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Join {updates_channel_url} for updates and to use this bot!")


# Create the handlers
start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help)
video_handler = MessageHandler(Filters.video, handle_video)
join_handler = CommandHandler('join', join)

# Create the updater and add the handlers to it
updater = Updater(token=os.environ['BOT_TOKEN'], use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(video_handler)
dispatcher.add_handler(join_handler)

# Error handling
dispatcher.add_error_handler(error)

# # Start the bot
#     app = Flask(__name__)

# @app.route('/' methods=['POST'])
# def webhook():
#     json_string = request.get_data()
#     update = telegram.Update.de_json(json.loads(json_string), bot)
#     dispatcher.process_update(update)
#     return 'ok'

# if __name__ == '__main__':
#     app.run(debug=True)

# bot = telegram.Bot(token=os.environ['BOT_TOKEN'])
# updater = telegram.ext.Updater(token=os.environ['BOT_TOKEN'])
# dispatcher = updater.dispatcher

# dispatcher.add_handler(start_handler)
# dispatcher.add_handler(help_handler)
# dispatcher.add_handler(video_handler)
# dispatcher.add_handler(join_handler)

# updater.start_webhook(listen="0.0.0.0",
#                       port=int(os.environ.get('PORT', 5000)),
#                       url_path=os.environ['BOT_TOKEN'])
# updater.bot.setWebhook(url=f"{NETLIFY_URL}/{os.environ['BOT_TOKEN']}")

#     # Send a message to the updates channel to inform users that the bot is up and running
#     updates_channel_id = os.environ.get('UPDATES_CHANNEL_ID')
#     updates_channel_url = f"https://t.me/c/{updates_channel_id}"
#     context.bot.send_message(chat_id=updates_channel_id,
#                              text="Bot is up and running!", parse_mode=ParseMode.HTML)

#     # Block until the bot is stopped
#     updater.idle()

# Start the bot
app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    json_string = request.get_data()
    update = telegram.Update.de_json(json.loads(json_string), bot)
    dispatcher.process_update(update)
    return 'ok'

if __name__ == '__main__':
    bot = telegram.Bot(token=os.environ['BOT_TOKEN'])
    updater = telegram.ext.Updater(token=os.environ['BOT_TOKEN'])
    dispatcher = updater.dispatcher

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(video_handler)
    dispatcher.add_handler(join_handler)

    updater.start_webhook(listen="0.0.0.0",
                          port=int(os.environ.get('PORT', 5000)),
                          url_path=os.environ['BOT_TOKEN'])
    updater.bot.setWebhook(url=f"{NETLIFY_URL}/{os.environ['BOT_TOKEN']}")

    # Send a message to the updates channel to inform users that the bot is up and running
    updates_channel_id = os.environ.get('UPDATES_CHANNEL_ID')
    updates_channel_url = f"https://t.me/c/{updates_channel_id}"
    bot.send_message(chat_id=updates_channel_id,
                     text=f"Bot is up and running!\nJoin {updates_channel_url} for updates and to use this bot!")

    app.run(debug=True)
