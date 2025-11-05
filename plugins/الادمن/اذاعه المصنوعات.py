# Copyright (c) 2025 Ahmed Ayyad (ahmedyad200)
# Licensed under Custom Proprietary License
# Redistribution and resale are prohibited.

import os

from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup
from telebot.async_telebot import AsyncTeleBot

from ahmedyad.database import datebase
from ahmedyad.filters import text_command
from ahmedyad.keyboards import cancel_key

brodcast_key = ReplyKeyboardMarkup(
    [
        ["جروبات", "خاص", "قنوات"],
        ["الكل"],
        [cancel_key.keyboard[0][0]],
    ],
    resize_keyboard=True
)


@Client.on_message(text_command('اذاعه المصنوعات',admin=True))
async def brodcast_for_all_bots(client, message):
    msg = await message.askWithReq('يرجي تنظيف المصنوعات قبل استخدام هذا الامر\nارسل الرساله لاقوم بعمل اذاعه في كل البوتات المصنوعه (ادعم النصوص فقط)')

    db_str_chats = ['{}:private','{}:group','{}:channel']
    text = msg.text
    msg = await msg.askWithReq('تريد عمل الاذاعه في الخاص او الجروبات ؟', reply_markup=brodcast_key)

    if msg.text == 'خاص':
        chats = db_str_chats[0]
    elif msg.text == 'جروبات':
        chats = db_str_chats[1]
    elif msg.text == 'قنوات':
        chats = db_str_chats[2]
    elif msg.text == 'الكل':
        chats = 'all'
    else:
        return await msg.reply('عذرا هناك خطأ ما تم الغاء الامر')
    await msg.reply('جاري عمل الاذاعه في البوتات المجانيه')
    for sudo_id in os.listdir('Bots'):
        for bot_username in await datebase.smembers(f'{client.me.id}:{sudo_id}:bot'):
            if await datebase.sismember(f'{client.me.id}:Bots:Subscription',bot_username):
                continue
            bot = AsyncTeleBot(await datebase.get(f'{client.me.id}:{bot_username}:token'))
            if chats == 'all':
                for chat_type in db_str_chats:
                    for chat in await datebase.smembers(chat_type.format(bot.bot_id)):
                        try:
                            await bot.send_message(chat, text)
                        except Exception as e:
                            print(e)
            else:
                for chat in await datebase.smembers(chats.format(bot.bot_id)):
                    try:
                        await bot.send_message(chat, text)
                    except Exception as e:
                        print(e)
    await msg.reply('جاري عمل الاذاعه في البوتات')
