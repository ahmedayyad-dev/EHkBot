# Copyright (c) 2025 Ahmed Ayyad (ahmedyad200)
# Licensed under Custom Proprietary License
# Redistribution and resale are prohibited.

from pyrogram import Client, filters

from ahmedyad.database import datebase
from ahmedyad.filters import text_command



@Client.on_message(text_command('تفعيل اشتراك بوت',admin=True))
async def addSubscriptionToBots(client, message):
    msg = await message.askWithReq('ارسل معرف البوت بدون @')

    await datebase.sadd(f'{client.me.id}:Bots:Subscription', msg.text)
    await msg.reply('تم تفعيل اشتراك البوت')


@Client.on_message(text_command('تعطيل اشتراك بوت',admin=True))
async def DelSubscriptionToBots(client, message):
    msg = await message.askWithReq('ارسل معرف البوت بدون @')

    await datebase.srem(f'{client.me.id}:Bots:Subscription', msg.text)
    await message.reply('تم تعطيل اشتراك البوت')
