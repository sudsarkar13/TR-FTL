from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import filters
import time
import psutil
from fastapi import FastAPI, Request

app = FastAPI()

@app.get('/stats')
async def stats(request: Request):
    currentTime = time.strftime('%H:%M:%S', time.gmtime(time.time() - time.monotonic()))
    sent = psutil.net_io_counters().bytes_sent
    recv = psutil.net_io_counters().bytes_recv
    cpuUsage = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    botstats = {
        'Bot Uptime': currentTime,
        '📊Data Usage📊': {
            'Upload': sent,
            'Download': recv
        },
        'CPU Usage': cpuUsage,
        'Memory Usage': memory,
        'Disk Usage': disk
    }
    return {'message': botstats}
