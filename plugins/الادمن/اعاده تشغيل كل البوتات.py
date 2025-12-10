# Copyright (c) 2025 Ahmed Ayyad (ahmedyad200)
# Licensed under Custom Proprietary License
# Redistribution and resale are prohibited.

import os

from pyrogram import Client

from ahmedyad.filters import text_command
from ahmedyad.systemd_manager import SystemdManager


@Client.on_message(text_command('اعاده تشغيل بوت', admin=True))
async def restart_bot(client, message):
    message = await message.reply('جاري اعاده تشغيل كل البوتات')
    restarted_bots = []

    for user_id in os.listdir('Bots'):
        for bot_username in os.listdir(f'Bots/{user_id}'):
            # Restart systemd service (async - no blocking!)
            await SystemdManager.restart_service(bot_username)
            restarted_bots.append(bot_username)

    bots_list = '\n'.join(restarted_bots) if restarted_bots else 'لا يوجد بوتات'
    await message.edit(f'تم اعاده تشغيل كل البوتات:\n\n{bots_list}')
