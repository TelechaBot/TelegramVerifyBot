# -*- coding: utf-8 -*-
# @Time    : 8/22/22 7:40 PM
# @FileName: Bot.py
# @Software: PyCharm
# @Github    ：sudoskys
import aiohttp
from pathlib import Path
import joblib, json
from CaptchaCore.Event import Tool
import telebot
from telebot import types, util
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.async_telebot import AsyncTeleBot


class clinetBot(object):
    def __init__(self):
        pass

    @staticmethod
    def life():
        try:
            if joblib.load('life.pkl') == "on":
                return True
            else:
                return False
        except Exception as e:
            print("Wrong:life.pkl do not exist" + str(e))
            joblib.dump("off", 'life.pkl')
            return False

    def run(self, config):
        if config.statu:
            Tool().console.print("Bot Running", style='blue')
            import telebot
            from telebot.async_telebot import AsyncTeleBot
            import joblib
            bot = AsyncTeleBot(config.botToken)
            joblib.dump("on", 'life.pkl')
            from CaptchaCore.BotEvent import Master
            from CaptchaCore.BotEvent import Group

            @bot.message_handler(commands=['start'])
            async def send_welcome(message):
                await bot.reply_to(message, "开始验证，你有175秒的时间计算这道题目")

            @bot.message_handler(commands=['about'])
            async def send_about(message):
                await bot.reply_to(message, "学习永不停息，进步永不止步，Project:https://github.com/sudoskys/")

            # Master(bot, config)
            # Group(bot, config)
            import asyncio
            asyncio.run(bot.polling())  # allowed_updates=util.update_types))
            # bot.infinity_polling()


class sendBot(object):
    # robotPush(token,groupID).postAudio(fileroad,info,name):
    def __init__(self, token):
        self.BOT = telebot.TeleBot(token, parse_mode="HTML")  # You can set parse_mode by default. HTML or MARKDOWN

    def sendMessage(self, objectID, msg):
        self.BOT.send_message(objectID, str(msg))

    def replyMessage(self, objectID, msg, reply_id):
        self.BOT.send_message(objectID, str(msg), reply_to_message_id=reply_id)

    def postDoc(self, objectID, files):
        if Path(str(files)).exists():
            doc = open(files, 'rb')
            self.BOT.send_document(objectID, doc)
            doc.close()
            return files

    def postVideo(self, objectID, files, source, name):
        if Path(str(files)).exists():
            video = open(files, 'rb')
            self.BOT.send_video(objectID, video, source, name, name)
            # '#音乐MV #AUTOrunning '+str(source)+"   "+name
            # 显示要求为MP4--https://mlog.club/article/5018822
            # print("============Already upload this video============")
            video.close()
            return files

    def postAudio(self, objectID, files, source, name):
        if Path(str(files)).exists():
            audio = open(files, 'rb')
            self.BOT.send_audio(objectID, audio, source, name, name)
            # '#音乐提取 #AUTOrunning '+str(source)+"   "+name
            # print("============ALready upload this flac============")
            audio.close()
            return files
