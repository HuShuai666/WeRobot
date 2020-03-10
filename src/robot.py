# coding:utf-8
from werobot import WeRoBot
from werobot.replies import SuccessReply
from config.settings import APP_ID, APP_SECRET
from src.functions import handle_text_message, handle_image_message, subscribe_message_func, un_subscribe_message_func
from utils.template_func import remind

config = dict(
    TOKEN='hushuai_cs',
    SERVER="tornado",
    HOST="0.0.0.0",
    PORT="6060",
    SESSION_STORAGE=False,
    ENABLE_SESSION=False,
    APP_ID=APP_ID,
    APP_SECRET=APP_SECRET,
    ENCODING_AES_KEY=None
)
robot = WeRoBot(config=config)


@robot.text
def text_message(message):
    text = handle_text_message(message)
    return text


@robot.subscribe
def subscribe_message(message):
    text = subscribe_message_func(message)
    return text


@robot.image
def image_message(message):
    handle_image_message(message)
    return SuccessReply(message)


@robot.unsubscribe
def unsubscribe_message(message):
    un_subscribe_message_func(message)
    return SuccessReply(message)


@robot.scan
def scan_message(message):
    return


@robot.handler
def common_replay(message):
    return SuccessReply(message)


# 对点击时间的配置
@robot.key_click("holiday")
def holiday(message):
    try:
        remind()
    except Exception as e:
        with open('error', 'a') as f:
            f.write(e)
    return """你已经发送"""


@robot.key_click("CESHI")
def ce_shi(message):
    return """什么都没有，你还点我干啥"""
