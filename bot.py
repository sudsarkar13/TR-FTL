import os
from pyrogram import Client, filters
from pyrogram.types import Message

# Telegram API credentials
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
BIN_CHANNEL = os.environ.get("BIN_CHANNEL")


# Define database handler
DATABASE_URL = os.environ.get("DATABASE_URL")

# Initialize the client
client = Client("trfiletolinkbot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, bin_channel=BIN_CHANNEL, database_url=DATABASE_URL)

# Define the start command handler
@client.on_message(filters.command("start"))
async def start_handler(_, message):
    await message.reply_text("Hi! I am a Telegram video downloader bot. Just send me a video file and I will provide you with a high-speed download link.")


# Define the video handler
@client.on_message(filters.video)
async def video_handler(_, message):
    file_id = message.video.file_id
    chat_id = message.chat.id
    message_id = message.message_id
    
    # Get the download link for the video file
    download_url = await client.send_video(
        chat_id=chat_id,
        video=file_id,
        supports_streaming=True,
        progress=progress_callback,
    )

    await client.send_message(chat_id, f"Download link: {download_url}")


# Define a progress callback function to track upload progress
async def progress_callback(current, total):
    print(f"Uploaded {current} out of {total}")


# Define an error handler
@client.on_message(filters.command(["cancel", "stop"]))
async def error_handler(_, message: Message):
    await message.reply_text("Operation cancelled!")


# Start the client
client.run()
