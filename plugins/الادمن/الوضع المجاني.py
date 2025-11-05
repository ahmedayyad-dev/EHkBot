# Copyright (c) 2025 Ahmed Ayyad (ahmedyad200)
# Licensed under Custom Proprietary License
# Redistribution and resale are prohibited.

from pyrogram import Client, filters

from ahmedyad.database import datebase
from ahmedyad.filters import text_command


@Client.on_message(text_command('تفعيل الوضع المجاني',admin=True))
async def addFreeMode(client, message):
    await datebase.set(f'{client.me.id}:FreeMode', '3yad')
    await message.reply('تم تفعيل الوضع المجاني')


@Client.on_message(text_command('تعطيل الوضع المجاني',admin=True))
async def DelFreeMode(client, message):
    await datebase.delete(f'{client.me.id}:FreeMode')
    await message.reply('تم تعطيل الوضع المجاني')
