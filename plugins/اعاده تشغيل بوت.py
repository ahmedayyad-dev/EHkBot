# Copyright (c) 2025 Ahmed Ayyad (ahmedyad200)
# Licensed under Custom Proprietary License
# Redistribution and resale are prohibited.

import os

from pyrogram import Client
from pyrogram.types import ReplyKeyboardMarkup

from ahmedyad.filters import text_command
from ahmedyad.keyboards import cancel_key
from ahmedyad.systemd_manager import SystemdManager
from ahmedyad.yad import get_user_id, get_user_bots


@Client.on_message(text_command('اعاده تشغيل بوت'))
async def restart_bot(client, message):
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

    # Restart systemd service (async - no blocking!)
    await SystemdManager.restart_service(bot_username)
    await message.reply(f'تم اعاده تشغيل البوت : @{bot_username}')

