# -*- coding: utf-8 -*-
# @Time    : 8/22/22 9:28 PM
# @FileName: BotEvent.py
# @Software: PyCharm
# @Github    ：sudoskys
import telebot
import json, joblib
from telebot import types, util
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.async_telebot import AsyncTeleBot
import asyncio, aiohttp


def load_config():
    global _config
    with open("item.json", encoding="utf-8") as f:
        _config = json.load(f)


def save_config():
    with open("item.json", "w", encoding="utf8") as f:
        json.dump(_config, f, indent=4, ensure_ascii=False)


def Master(bot, config):
    @bot.message_handler(content_types=['text'])
    async def replay(message, items=None):
        userID = message.from_user.id
        if str(userID) == config.ClientBot.owner:
            try:
                # chat_id = message.chat.id
                command = message.text
                if command == "off":
                    joblib.dump("off", 'life.pkl')
                    await bot.reply_to(message, 'success！')
                if command == "on":
                    joblib.dump("on", 'life.pkl')
                    await bot.reply_to(message, 'success！')
            except Exception as e:
                await bot.reply_to(message, "Wrong:" + str(e))


def Group(bot, config):
    # if bot is added to group, this handler will work
    @bot.my_chat_member_handler()
    async def my_chat_m(message: types.ChatMemberUpdated):
        old = message.old_chat_member
        new = message.new_chat_member
        if new.status == "member":
            load_config()
            # print(_config)
            if message.chat.id in _config.get("whiteGroup"):
                pass
                # bot.send_message(message.chat.id,
                #                 "Hello bro! i can use high level problem to verify new chat member~~")
            else:
                if _config.get("whiteGroupSwitch"):
                    await bot.send_message(message.chat.id,
                                           "Somebody added me to THIS group,but the group not in my white list")
                    await bot.leave_chat(message.chat.id)

    @bot.message_handler(content_types=['new_chat_members'])
    async def delall(msg):
        InviteLink = "https://github.com/TelechaBot"
        mrkplink = InlineKeyboardMarkup()  # Created Inline Keyboard Markup
        mrkplink.add(InlineKeyboardButton("Join our group ", url=InviteLink))  # Added Invite Link to Inline Keyboard
        await bot.send_message(msg.chat.id,
                         f"Hey there {msg.from_user.first_name}.", reply_markup=mrkplink)

        # InviteLink = "123"
        # mrkplink = InlineKeyboardMarkup()  # Created Inline Keyboard Markup
        # mrkplink.add(InlineKeyboardButton("click here to verify yourself🚀", url=InviteLink))
        # await bot.send_message(message.chat.id, "Hello {name}!, Pleas  Click the link below to verify".format(
        #    name=new.user.first_name),
        #                       reply_markup=mrkplink)  # Welcome message
