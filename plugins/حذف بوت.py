# Copyright (c) 2025 Ahmed Ayyad (ahmedyad200)
# Licensed under Custom Proprietary License
# Redistribution and resale are prohibited.

from pyrogram import Client
from pyrogram.types import Message, ReplyKeyboardMarkup

from ahmedyad.filters import text_command
from ahmedyad.keyboards import cancel_key
from ahmedyad.yad import get_user_id, get_user_bots, delete_bot


@Client.on_message(text_command('حذف بوت'))
async def delete_Bot(client: Client, message: Message):
    user_id = await get_user_id(message)
    Bots = await get_user_bots(user_id)
    if len(Bots) > 1:
        key = ReplyKeyboardMarkup([], resize_keyboard=True)
        for user in Bots:
            key.keyboard.append([user])
        key.keyboard.append([cancel_key.keyboard[0][0]])
        message = await message.askWithReq("اختار يوزر البوت", reply_markup=key)
        bot_username = message.text
    elif len(Bots) == 1:
        bot_username = Bots.pop()
    else:
        return await message.reply('لا يوجد لديك اي بوتات علي المصنع')

    # Delete bot with error handling
    success, msg_text = await delete_bot(bot_username, user_id)
    if success:
        await message.reply(f'✅ {msg_text}')
    else:
        await message.reply(f'❌ {msg_text}')
