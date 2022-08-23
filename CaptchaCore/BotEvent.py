# -*- coding: utf-8 -*-
# @Time    : 8/22/22 9:28 PM
# @FileName: BotEvent.py
# @Software: PyCharm
# @Github    ：sudoskys
import json
import telebot
from telebot import types, util
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from BotRedis import JsonRedis

verifyRedis = JsonRedis(20)


def load_config():
    global _config
    with open("config.json", encoding="utf-8") as f:
        _config = json.load(f)


def save_config():
    with open("config.json", "w", encoding="utf8") as f:
        json.dump(_config, f, indent=4, ensure_ascii=False)


# 支持三层读取创建操作并且不报错！
def readUser(where, group):
    where = str(where)
    group = str(abs(group))
    load_config()
    if _config.get(where):
        oss = _config[where].get(group)
        if oss:
            return oss
        else:
            return []
    else:
        return []


def popUser(where, group, key):
    where = str(where)
    group = str(abs(group))
    load_config()
    if _config.get(where):
        if _config[where].get(group):
            if key in _config[where][str(group)]:
                _config[where][str(group)].remove(key)
    save_config()


def saveUser(where, group, key):
    where = str(where)
    group = str(abs(group))
    load_config()
    if _config.get(where):
        if _config[where].get(group):
            if not key in _config[where][str(group)]:
                _config[where][str(group)].append(key)
        else:
            _config[where][str(group)] = []
            _config[where][str(group)].append(key)
    else:
        _config[where] = {}
        _config[where][str(group)] = []
        _config[where][str(group)].append(key)
    save_config()


def Start(bot, config):
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        load_config()
        if message.chat.type == "private":
            if verifyRedis.read(str(message.from_user.id)):
                bot.reply_to(message, "开始验证，你有175秒的时间计算这道题目")
                # bot.register_next_step_handler(msg, verify_step)
                # verify_step(bot, message)
                # 用户操作
                verifyRedis.promote(message.from_user.id)
            else:
                bot.reply_to(message, "未检索到你的信息。你无需验证")
        else:
            print(0)


def About(bot, config):
    @bot.message_handler(commands=['about'])
    def send_about(message):
        if message.chat.type == "private":
            bot.reply_to(message, "学习永不停息，进步永不止步，Project:https://github.com/sudoskys/")


def Group(bot, config):
    # if bot is added to group
    @bot.my_chat_member_handler()
    def my_chat_m(message: types.ChatMemberUpdated):
        old = message.old_chat_member
        new = message.new_chat_member
        if new.status == "member":
            load_config()
            if message.chat.id in _config.get("whiteGroup"):
                pass
                # bot.send_message(message.chat.id,
                #                 "Hello bro! i can use high level problem to verify new chat member~~")
            else:
                if _config.get("whiteGroupSwitch"):
                    bot.send_message(message.chat.id,
                                     "Somebody added me to THIS group,but the group not in my white list")
                    bot.leave_chat(message.chat.id)


def Left(bot, config):
    @bot.message_handler(content_types=['left_chat_member'])
    def left(msg):
        #   if msg.left_chat_member.id != bot.get_me().id:
        load_config()
        try:
            bot.delete_message(msg.chat.id, msg.message_id)

        except Exception as e:
            print(e)
            bot.send_message(msg.chat.id,
                             f"sorry,i am not admin")
        # 用户操作
        verifyRedis.removed(msg.from_user.id, str(msg.chat.id))


def New(bot, config):
    @bot.message_handler(content_types=['new_chat_members'])
    def new_comer(msg):
        # if msg.left_chat_member.id != bot.get_me().id:
        load_config()
        try:
            bot.delete_message(msg.chat.id, msg.message_id)

        except Exception as e:
            print(e)
            bot.send_message(msg.chat.id,
                             f"sorry,i am not admin")
        # 用户操作
        verifyRedis.add(msg.from_user.id, str(msg.chat.id))
        # saveUser("newComer", msg.chat.id, msg.from_user.id)
        bot.restrict_chat_member(msg.chat.id, msg.from_user.id, can_send_messages=False,
                                 can_send_media_messages=False,
                                 can_send_other_messages=False)
        InviteLink = "https://github.com/TelechaBot"
        mrkplink = InlineKeyboardMarkup()  # Created Inline Keyboard Markup
        mrkplink.add(
            InlineKeyboardButton("请与我展开私聊测试，来证明您是真人。 ", url=InviteLink))  # Added Invite Link to Inline Keyboard
        bot.send_message(msg.chat.id,
                         f"Hey there {msg.from_user.first_name}.", reply_markup=mrkplink)

    # InviteLink = "123"
    # mrkplink = InlineKeyboardMarkup()  # Created Inline Keyboard Markup
    # mrkplink.add(InlineKeyboardButton("click here to verify yourself🚀", url=InviteLink))
    # await bot.send_message(message.chat.id, "Hello {name}!, Pleas  Click the link below to verify".format(
    #    name=new.user.first_name),
    #                       reply_markup=mrkplink)  # Welcome message
