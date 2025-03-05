# Telegram File to Link Bot

A Telegram bot that converts uploaded files into high-speed downloadable and streamable links. Built with Python, Flask and the python-telegram-bot library.

## Features

- Converts uploaded files to permanent download & streaming links
- Web interface to check bot status
- File size limit of 50MB
- Webhook support for reliable message handling
- Required channel subscription before using bot
- HTML5 player for streaming media files
- Permanent links that don't expire

## Prerequisites

- Python 3.12+
- A Telegram Bot Token from [@BotFather](https://t.me/botfather)
- A hosting service that supports Python/Flask apps (e.g. Netlify)

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/telegram-file-bot.git
cd telegram-file-bot
```

2. Create and activate a virtual environment:

```bash
python -m venv bot
source bot/bin/activate # On Windows use: bot\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

1. Set the following environment variables:

```bash
export YOUR_API_TOKEN="your_telegram_bot_token"
export HTML_PAGE_URL="your_deployment_url"
export WEBHOOK_PATH="/webhook"
```

2. Create a telegram channel to store files and get its channel ID.

## Running Locally

1. Start the Flask development server:

```bash
python bot.py
```

2. The bot status page will be available at `http://localhost:5000`.

