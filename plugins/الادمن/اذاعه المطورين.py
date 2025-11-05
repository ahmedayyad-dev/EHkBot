# Copyright (c) 2025 Ahmed Ayyad (ahmedyad200)
# Licensed under Custom Proprietary License
# Redistribution and resale are prohibited.

import os

from pyrogram import Client
from telebot.async_telebot import AsyncTeleBot

from ahmedyad.database import datebase
from ahmedyad.filters import text_command



@Client.on_message(text_command('اذاعه المطورين',admin=True))
async def brodcast_to_sudos(client, message):
    msg = await message.askWithReq('ارسل الرساله لارسلها لكل المطورين في المصنع (ادعم النصوص فقط)')

    await msg.reply('جاري ارسال الاذاعه للمطورين')
    for sudo_id in os.listdir('Bots'):
        for bot_username in await datebase.smembers(f'{client.me.id}:{sudo_id}:bot'):
            bot = AsyncTeleBot(await datebase.get(f'{client.me.id}:{bot_username}:token'))
            try:
                await bot.send_message(sudo_id, msg.text)
            except Exception as e:
                await msg.reply(f"{bot_username} : {e}")
    await msg.reply('لقد تم ارسال الرساله بنجاح')
