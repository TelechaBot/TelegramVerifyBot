# -*- coding: utf-8 -*-
# @Time    : 8/22/22 9:28 PM
# @FileName: BotEvent.py
# @Software: PyCharm
# @Github    ：sudoskys
import telebot
import json, joblib
from telebot import ExceptionHandler, types, util
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.async_telebot import AsyncTeleBot
import asyncio, aiohttp


def load_config():
    global _config
    with open("config.json", encoding="utf-8") as f:
        _config = json.load(f)


def save_config():
    with open("config.json", "w", encoding="utf8") as f:
        json.dump(_config, f, indent=4, ensure_ascii=False)


def Verfiy(id, text):
    _config["newCommer"].pop(id)
    save_config()


def verify_step(bot):
    @bot.message_handler(func=lambda message: True)
    async def echo_message(message):
        bot.reply_to(message, message.text)
        try:
            chat_id = message.chat.id
            answer = message.text
            Verfiy(message.msg.from_user.id, answer)
        except Exception as e:
            await bot.reply_to(message, 'oooops')


def Master(bot, config):
    @bot.message_handler(commands=['start'])
    async def send_welcome(message):
        load_config()
        # print(0)
        # print(message.msg.from_user.id)
        if message.chat.type == "private":
            if message.msg.from_user.id in _config.get("newCommer"):
                await bot.reply_to(message, "开始验证，你有175秒的时间计算这道题目")
                # bot.register_next_step_handler(msg, verify_step)
                verify_step(bot, message)
                # await bot.reply_to(message, )
            else:
                await bot.reply_to(message, "你无需验证")

    @bot.message_handler(commands=['about'])
    async def send_about(message):
        if message.chat.type == "private":
            await bot.reply_to(message, "学习永不停息，进步永不止步，Project:https://github.com/sudoskys/")


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

    @bot.message_handler(content_types=['left_chat_member'])
    async def left(msg):
        #   if msg.left_chat_member.id != bot.get_me().id:
        load_config()
        try:
            await bot.delete_message(msg.chat.id, msg.message_id)
        except Exception as e:
            await bot.send_message(msg.chat.id,
                                   f"sorry,i am not admin")
        _config["newCommer"].pop(msg.from_user.id)
        save_config()

    @bot.message_handler(content_types=['new_chat_member'])
    async def new_comer(msg):
        # if msg.left_chat_member.id != bot.get_me().id:
        load_config()
        try:
            await bot.delete_message(msg.chat.id, msg.message_id)
        except Exception as e:
            await bot.send_message(msg.chat.id,
                                   f"sorry,i am not admin")
        # aas(2)
        _config["newCommer"] = +[msg.from_user.id]
        _config["newCommer"] = list(set(_config["newCommer"]))
        save_config()
        await bot.restrict_chat_member(msg.chat.id, msg.from_user.id, can_send_messages=False,
                                       can_send_media_messages=False,
                                       can_send_other_messages=False)
        InviteLink = "https://github.com/TelechaBot"
        mrkplink = InlineKeyboardMarkup()  # Created Inline Keyboard Markup
        mrkplink.add(
            InlineKeyboardButton("请与我展开私聊测试，来证明您是真人。 ", url=InviteLink))  # Added Invite Link to Inline Keyboard
        await bot.send_message(msg.chat.id,
                               f"Hey there {msg.from_user.first_name}.", reply_markup=mrkplink)

    # InviteLink = "123"
    # mrkplink = InlineKeyboardMarkup()  # Created Inline Keyboard Markup
    # mrkplink.add(InlineKeyboardButton("click here to verify yourself🚀", url=InviteLink))
    # await bot.send_message(message.chat.id, "Hello {name}!, Pleas  Click the link below to verify".format(
    #    name=new.user.first_name),
    #                       reply_markup=mrkplink)  # Welcome message
