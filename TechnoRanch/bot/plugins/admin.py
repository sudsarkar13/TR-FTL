import os
import time
import string
import random
import asyncio
import aiofiles
import datetime
from TechnoRanch.utils.broadcast_helper import send_msg
from TechnoRanch.utils.database import Database
from TechnoRanch.bot import StreamBot
from TechnoRanch.vars import Var
from pyrogram import filters, Client
from pyrogram.types import Message
from fastapi import FastAPI

app = FastAPI()
db = Database(Var.DATABASE_URL, Var.name)
broadcast_ids = {}

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

@app.get("/users")
async def get_users():
    total_users = await db.total_users_count()
    return {"total_users": total_users}

@app.post("/broadcast")
async def broadcast(message: Message):
    all_users = await db.get_all_users()
    broadcast_msg = message.reply_to_message
    while True:
        broadcast_id = ''.join([random.choice(string.ascii_letters) for i in range(3)])
        if not broadcast_ids.get(broadcast_id):
            break
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    failed = 0
    success = 0
    broadcast_ids[broadcast_id] = dict(
        total=total_users,
        current=done,
        failed=failed,
        success=success
    )
    async with aiofiles.open('broadcast.txt', 'w') as broadcast_log_file:
        async for user in all_users:
            sts, msg = await send_msg(
                user_id=int(user['id']),
                message=broadcast_msg
            )
            if msg is not None:
                await broadcast_log_file.write(msg)
            if sts == 200:
                success += 1
            else:
                failed += 1
            if sts == 400:
                await db.delete_user(user['id'])
            done += 1
            if broadcast_ids.get(broadcast_id) is None:
                break
            else:
                broadcast_ids[broadcast_id].update(
                    dict(
                        current=done,
                        failed=failed,
                        success=success
                    )
                )
    if broadcast_ids.get(broadcast_id):
        broadcast_ids.pop(broadcast_id)
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await asyncio.sleep(3)
    if failed == 0:
        return {
            "message": f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed."
        }
    else:
        with open('broadcast.txt', 'rb') as file:
            contents = file.read()
        os.remove('broadcast.txt')
        return {
            "message": f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
            "file": contents
        }
