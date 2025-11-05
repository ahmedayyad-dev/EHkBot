# Copyright (c) 2025 Ahmed Ayyad (ahmedyad200)
# Licensed under Custom Proprietary License
# Redistribution and resale are prohibited.

from pyrogram import Client
from pyrogram.types import Message

from ahmedyad.filters import text_command
from ahmedyad.keyboards import owner_start_keyboard, member_start_keyboard
from ahmedyad.yad import admins


@Client.on_message(text_command('/start'))
async def start(client: Client, message: Message):
    if message.from_user.id in admins:
        await message.reply_text('اهلا عزيزي المطور',reply_markup=owner_start_keyboard)
    else:
        await message.reply_text('اهلا يعزيزي المستخدم',reply_markup=member_start_keyboard)

