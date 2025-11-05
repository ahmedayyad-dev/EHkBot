# Copyright (c) 2025 Ahmed Ayyad (ahmedyad200)
# Licensed under Custom Proprietary License
# Redistribution and resale are prohibited.

import os

from pyrogram import Client
from pyrogram.errors import MessageTooLong

from ahmedyad.database import datebase
from ahmedyad.filters import text_command


@Client.on_message(text_command('البوتات المصنوعه',admin=True))
async def Bots_COUNT(client, message):
    m = await message.reply('جاري الحصول علي البوتات المصنوعه')
    if len(os.listdir('Bots')) >= 1:
        t = f"اليك البوتات المصنوعه"
        n = 0
        for sudo_id in os.listdir('Bots'):
            for bot_username in await datebase.smembers(f'{client.me.id}:{sudo_id}:bot'):
                n = n + 1
                token = await datebase.get(f'{client.me.id}:{bot_username}:token')
                bot_id2 = token.split(':AA')[0]
                t += f'\n{n}- @{bot_username} | {sudo_id}\n'
                t += ' | G{} | P{} | C{} | A{}'.format(
                    await datebase.scard(f'{bot_id2}:group'),
                    await datebase.scard(f'{bot_id2}:private'),
                    await datebase.scard(f'{bot_id2}:channel'),
                    await datebase.scard(f'{bot_id2}:userbots'),
                )

        t += f"\nG = عدد الجروبات"
        t += f"\nP = عدد الخاص"
        t += f"\nC = عدد القنوات"
        t += f"\nA = عدد المساعدين"
    else:
        t = "لا يوجد بوتات مصنوعه"
    try:
        await m.edit(t)
    except MessageTooLong:
        lines = t.split('\n')
        for i in range(0, len(lines), 51):
            part = '\n'.join(lines[i:i + 51])
            await m.reply(part)