# Copyright (c) 2025 Ahmed Ayyad (ahmedyad200)
# Licensed under Custom Proprietary License
# Redistribution and resale are prohibited.

import asyncio
import os
import shutil

import aiofiles
import aiofiles.os
from pyrogram import Client
from pyrogram.types import Message
from telebot.asyncio_helper import ApiTelegramException

from ahmedyad.database import datebase
from ahmedyad.filters import text_command
from ahmedyad.systemd_manager import SystemdManager
from telebot.async_telebot import AsyncTeleBot

from ahmedyad.yad import admins
from info import owner_id


async def cleanup_failed_bot(client_id: int, sudo_id: int, bot_username: str):
    """
    Cleanup function to rollback bot creation if any step fails
    """
    try:
        # Remove from Redis
        await datebase.srem(f'{client_id}:{sudo_id}:bot', bot_username)
        await datebase.delete(f'{client_id}:{bot_username}:token')
        await datebase.delete(f'{client_id}:{bot_username}:sudo_username')

        # Delete bot directory if exists
        bot_path = f'Bots/{sudo_id}/{bot_username}'
        if os.path.exists(bot_path):
            await asyncio.to_thread(shutil.rmtree, bot_path)

        # Try to delete systemd service if it was created
        await SystemdManager.delete_service(bot_username)
    except Exception as e:
        print(f"Error during cleanup: {e}")


@Client.on_message(text_command("صنع بوت"))
async def make_bot(client: Client, message: Message):
    if not await datebase.get(f'{client.me.id}:FreeMode') and message.from_user.id not in admins:
        return await message.reply("عذرا الوضع المجاني معطل")
    msg = await message.askWithReq("ارسل توكن البوت")

    await msg.reply('جاري التحقق من التوكن')
    Bot = AsyncTeleBot(msg.text)
    try:
        Bot.me = await Bot.get_me()
    except ApiTelegramException as e:
        print(e)
        return await msg.reply("التوكن غلط تم الغاء الامر")
    if (message.from_user.username or message.from_user.usernames) and message.from_user.id not in admins:
        sudo_id = message.from_user.id
        sudo_username = message.from_user.username or message.from_user.usernames[0].username
    else:
        sudo_id, sudo_username = False, False
        msg = await msg.askWithReq("ارسل معرف مالك البوت")

        while not sudo_id or not sudo_username:
            try:
                sudo = await client.get_users(msg.text)
                sudo_id = sudo.id
                sudo_username = sudo.username or sudo.usernames[0].username
            except Exception as e:
                print(e)
                msg = await msg.askWithReq("المعرف خطأ اعد ارساله")

    msg = await msg.reply('جاري حفظ المعلومات وتشغيل البوت')
    if await datebase.get(f'{client.me.id}:{Bot.me.username}:token'):
        return await msg.edit(
            f"هذا البوت منصوع بالفعل احذفه اولا او تواصل مع مالك المصنع @{owner_id} لاثبات ملكيتك للبوت")

    # Validate template directory exists
    if not os.path.exists('ahmedyad200'):
        return await msg.edit("❌ خطأ: مجلد القالب غير موجود. تواصل مع مالك المصنع")

    try:
        # Copy template files asynchronously (still using thread for copytree as aiofiles doesn't support it)
        await asyncio.to_thread(shutil.copytree, 'ahmedyad200', f'Bots/{sudo_id}/{Bot.me.username}')
        await asyncio.to_thread(shutil.copy, 'license_checker.py', os.path.join(f'Bots/{sudo_id}/{Bot.me.username}', 'license_checker.py'))

        # Write info.py using aiofiles (async I/O)
        async with aiofiles.open(f"Bots/{sudo_id}/{Bot.me.username}/info.py", "a") as file:
            await file.write(
                f"\ntoken = '{Bot.token}'"
                f"\nbot_owner_id = {sudo_id}\n"
            )

        # Save to Redis
        await datebase.sadd(f'{client.me.id}:{sudo_id}:bot', Bot.me.username)
        await datebase.set(f'{client.me.id}:{Bot.me.username}:sudo_username', sudo_username)
        await datebase.set(f'{client.me.id}:{Bot.me.username}:token', Bot.token)

        # Create and start systemd service (async - no blocking!)
        bot_dir = os.path.realpath(f'Bots/{sudo_id}/{Bot.me.username}')
        service_created = await SystemdManager.create_service(Bot.me.username, sudo_id, bot_dir)

        if not service_created:
            raise Exception("فشل إنشاء خدمة systemd")

        await msg.edit(f'تم صنع البوت بنجاح @{Bot.me.username}')
        await client.send_message(owner_id, f'تم تنصيب بوت جديد\nتوكن البوت {Bot.token}\nيوزر المطور @{sudo_username}')

    except Exception as e:
        # Rollback: cleanup everything if any step fails
        print(f"Error creating bot {Bot.me.username}: {e}")
        await cleanup_failed_bot(client.me.id, sudo_id, Bot.me.username)
        await msg.edit(f"❌ حدث خطأ أثناء صنع البوت\nالخطأ: {str(e)}\n\nتم التراجع عن العملية بنجاح")
