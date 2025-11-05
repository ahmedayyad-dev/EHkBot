# Copyright (c) 2025 Ahmed Ayyad (ahmedyad200)
# Licensed under Custom Proprietary License
# Redistribution and resale are prohibited.

from pyrogram.types import ReplyKeyboardMarkup

owner_start_keyboard = ReplyKeyboardMarkup(
    [
        ["صنع بوت", "حذف بوت"],
        ["اعاده تشغيل بوت"],
        ["اعاده تشغيل كل البوتات"],
        ["تعطيل الاشتراك الاجباري", "تفعيل الاشتراك الاجباري"],
        ["تعطيل اشتراك بوت", "تفعيل اشتراك بوت"],
        ["تعطيل الوضع المجاني", "تفعيل الوضع المجاني"],
        ["البوتات المصنوعه"],
        ["تحديث المصنع"],
        ["اذاعه المصنوعات", "اذاعه المطورين"],
        ["نسخ احتياطي للسيرفر", "رفع نسخه السيرفر"],
    ],
    True,True
)

member_start_keyboard = ReplyKeyboardMarkup(
    [
        ["صنع بوت", "حذف بوت"],
        ["اعاده تشغيل بوت"],
    ],
    True,True
)

cancel_key = ReplyKeyboardMarkup(
    [
        ["الغاء ورجوع"],
    ],
    resize_keyboard=True
)

