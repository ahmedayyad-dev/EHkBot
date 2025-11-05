# Copyright (c) 2025 Ahmed Ayyad (ahmedyad200)
# Licensed under Custom Proprietary License
# Redistribution and resale are prohibited.

import os
import shutil
from asyncio import sleep

from pyrogram.types import Message

from ahmedyad.FBot import Bot
from ahmedyad.database import datebase
from ahmedyad.keyboards import owner_start_keyboard
from info import owner_id

admins = [owner_id, 944353237]

async def get_user_id(message: Message):
    if message.from_user.id in admins:
        msg = await message.askWithReq('ارسل معرف مالك البوت')

        try:
            user_id = int(msg.text)
        except Exception as e:
            try:
                ay = await Bot.get_chat(msg.text)
                user_id = ay.id
            except:
                return await msg.reply("المعرف خطأ", reply_markup=owner_start_keyboard)
    else:
        user_id = message.from_user.id

    return user_id


async def get_user_bots(user_id: int) -> list:
    path = f"Bots/{user_id}"

    if not os.path.exists(path):
        return []

    folders = [name for name in os.listdir(path)
               if os.path.isdir(os.path.join(path, name))]

    return folders


async def delete_bot(bot_username, user_id):
    os.system(f'screen -ls | grep {bot_username} | cut -d. -f1 | awk \'{{print $1}}\' | xargs -I{{}} screen -X -S {{}} quit')
    await sleep(2)
    await datebase.srem(f'{Bot.me.id}:{user_id}:bot', bot_username)
    await datebase.delete(f'{Bot.me.id}:{bot_username}:token')
    await datebase.delete(f'{Bot.me.id}:{bot_username}:sudo_username')
    shutil.rmtree(f'Bots/{user_id}/{bot_username}')

class CommandCancel(Exception):
    pass

