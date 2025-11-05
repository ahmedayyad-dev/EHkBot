# Copyright (c) 2025 Ahmed Ayyad (ahmedyad200)
# Licensed under Custom Proprietary License
# Redistribution and resale are prohibited.

from os import execle, environ
from sys import executable

from pyrogram import Client

from ahmedyad.ahmedgit import update_bot
from ahmedyad.filters import text_command


@Client.on_message(text_command('تحديث المصنع',admin=True))
async def update_all_files(client, message):
    m = await message.reply('جاري تحديث جميع الملفات واخد نسخه احتياطيه من الملفات الحاليه')
    res = update_bot()
    if res:
        await m.edit(f"تم نقل الملفات الحاليه الي المسار {res}\nجاري اعاده تشغيل الصانع")
        args = [executable, "main.py"]
        execle(executable, *args, environ)
    else:
        await m.edit("حدث خطأ ما")