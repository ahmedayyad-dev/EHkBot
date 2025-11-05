# Copyright (c) 2025 Ahmed Ayyad (ahmedyad200)
# Licensed under Custom Proprietary License
# Redistribution and resale are prohibited.

import os

from pyrogram import Client

from ahmedyad.database import backup_redis, restore_redis
from ahmedyad.filters import text_command



@Client.on_message(text_command("نسخ احتياطي للسيرفر",admin=True))
async def redis_backup(client, message):
    await message.reply('جاري اخد نسخه احتياطيه')
    backup_file = await backup_redis()
    await client.send_document(message.chat.id, backup_file, caption=f'redis backup',
                               file_name='backup.db')
    os.remove(backup_file)

@Client.on_message(text_command("رفع نسخه السيرفر",admin=True))
async def redis_restore(client, message):
    msg = await message.askWithReq('ارسل ملف النسخه الان')

    await msg.reply('جاري تحميل الملف ورفع النسخه')
    backup_file = await msg.download()
    await msg.reply('تم استعاده {} مقتاح'.format(await restore_redis(backup_file)))
    os.remove(backup_file)
