# -*- coding: utf-8 -*-
# @Time    : 8/22/22 9:28 PM
# @FileName: BotEvent.py
# @Software: PyCharm
# @Github    ：sudoskys
import telebot
import json, joblib
from telebot import types, util
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def load_config():
    global _config
    with open("data/list.json", encoding="utf-8") as f:
        _config = json.load(f)


def save_config():
    with open("data/list.json", "w", encoding="utf8") as f:
        json.dump(_config, f, indent=4, ensure_ascii=False)


def Master(bot, config):
    @bot.message_handler(content_types=['text'])
    def replay(message, items=None):
        userID = message.from_user.id
        if str(userID) == config.ClientBot.owner:
            try:
                # chat_id = message.chat.id
                command = message.text
                if command == "off":
                    joblib.dump("off", 'life.pkl')
                    bot.reply_to(message, 'success！')
                if command == "on":
                    joblib.dump("on", 'life.pkl')
                    bot.reply_to(message, 'success！')
            except Exception as e:
                bot.reply_to(message, "Wrong:" + str(e))


def Group(bot, config):
    # if bot is added to group, this handler will work
    @bot.my_chat_member_handler()
    def my_chat_m(message: types.ChatMemberUpdated):
        old = message.old_chat_member
        new = message.new_chat_member
        if new.status == "member":
            load_config()
            print(_config)
            if message.chat.id in _config.get("whiteGroup"):
                bot.send_message(message.chat.id,
                                 "Hello bro! i can use high level problem to verify new chat member~~")
            else:
                if  _config.get("whiteGroupSwitch"):
                    bot.send_message(message.chat.id,
                                     "Somebody added me to THIS group,but the group not in my white list")
                    bot.leave_chat(message.chat.id)

    @bot.chat_member_handler()
    def chat_m(message: types.ChatMemberUpdated):
        old = message.old_chat_member
        new = message.new_chat_member
        print("222")
        if new.status == "member":
            InviteLink = "123"
            mrkplink = InlineKeyboardMarkup()  # Created Inline Keyboard Markup
            mrkplink.add(InlineKeyboardButton("click here to verify yourself🚀", url=InviteLink))
            bot.send_message(message.chat.id, "Hello {name}!, Pleas  Click the link below to verify".format(
                name=new.user.first_name),
                             reply_markup=mrkplink)  # Welcome message
