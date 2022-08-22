# -*- coding: utf-8 -*-
# @Time    : 8/22/22 7:40 PM
# @FileName: Bot.py
# @Software: PyCharm
# @Github    ：sudoskys
from pathlib import Path
import joblib, json
from CaptchaCore.Event import Tool
import telebot
from telebot import types, util
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def load_config():
    global _config
    with open("data/list.json", encoding="utf-8") as f:
        _config = json.load(f)


def save_config():
    with open("data/list.json", "w", encoding="utf8") as f:
        json.dump(_config, f, indent=4, ensure_ascii=False)


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
            import joblib
            bot = telebot.TeleBot(config.botToken)
            joblib.dump("on", 'life.pkl')

            @bot.message_handler(commands=['start'])
            def send_welcome(message):
                bot.reply_to(message, "开始验证，你有175秒的时间计算这道题目")

            @bot.message_handler(commands=['about'])
            def send_about(message):
                bot.reply_to(message, "学习永不停息，进步永不止步，Project:https://github.com/sudoskys/")

            # if bot is added to group, this handler will work
            @bot.my_chat_member_handler()
            def my_chat_m(message: types.ChatMemberUpdated):
                old = message.old_chat_member
                new = message.new_chat_member
                if new.status == "member":
                    load_config()
                    if message.chat.id in _config.whiteGroup:
                        bot.send_message(message.chat.id,
                                         "Hello!")
                    else:
                        bot.send_message(message.chat.id,
                                         "Somebody added me to group,but the group not in my white list")
                        bot.leave_chat(message.chat.id)

            @bot.chat_member_handler()
            def chat_m(message: types.ChatMemberUpdated):
                old = message.old_chat_member
                new = message.new_chat_member
                if new.status == "member":
                    InviteLink = "123"
                    mrkplink = InlineKeyboardMarkup()  # Created Inline Keyboard Markup
                    mrkplink.add(InlineKeyboardButton("click here to verify yourself🚀", url=InviteLink))
                    bot.send_message(message.chat.id, "Hello {name}!, Pleas  Click the link below to verify".format(
                        name=new.user.first_name),
                                     reply_markup=mrkplink)  # Welcome message

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

            bot.infinity_polling()


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
