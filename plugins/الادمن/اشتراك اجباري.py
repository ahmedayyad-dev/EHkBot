# Copyright (c) 2025 Ahmed Ayyad (ahmedyad200)
# Licensed under Custom Proprietary License
# Redistribution and resale are prohibited.
from pyrogram import Client, filters

from ahmedyad.database import datebase
from ahmedyad.filters import text_command



@Client.on_message(text_command('تفعيل الاشتراك الاجباري',admin=True))
async def SetChCheckToBots(client, message):
    msg = await message.askWithReq('ارسل معرف الدردشه مع @ الان')
    try:
        await client.telebot.get_chat_member(msg.text, client.me.bot_id)
        ch = await client.telebot.get_chat(msg.text)
    except Exception as e:
        return await msg.reply('تاكد ان المصنع مرفوع في القناه او الجروب')
    await datebase.set(f'{client.me.id}:ChCheckToBots', ch.id)
    await msg.reply('تم تفعيل الاشتراك الاجباري للبوتات المصنوعه')


@Client.on_message(text_command('تعطيل الاشتراك الاجباري',admin=True))
async def DelChCheckToBots(client, message):
    await datebase.delete(f'{client.me.id}:ChCheckToBots')
    await message.reply('تم تعطيل الاشتراك الاجباري للبوتات المصنوعه')
