# -*- coding: utf-8 -*-
# @Time    : 8/22/22 6:40 PM
# @FileName: main.py
# @Software: PyCharm
# @Github    ：sudoskys
import pathlib
from pathlib import Path
from CaptchaCore.Bot import sendBot, clinetBot
from configparser import ConfigParser
from CaptchaCore.Event import Check, Read, Tool

# 初始化文件系统
Check().run()
# 初始化配置文件
config = Read(str(Path.cwd()) + "/Captcha.yaml").get()
if config.get("version"):
    Tool().console.print("完成初始化:" + config.version, style='blue')

pushService = sendBot(config.botToken)
clinetBot().run(config)


