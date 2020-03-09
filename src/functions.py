# coding: utf-8
import logging
import requests
import time
from src.qualities_reply import quality_questions
from utils.service import WeixinServer, WeiXin_Server
import json
logger = logging.getLogger('info')


# 处理文本信息
def handle_text_message(message):
    content = message.content
    openid = message.source
    hu_access_token = WeixinServer.get_access_token()
    if content.strip() == '自定义菜单':
        params = {
                "button": [
                    {
                        "type": "view",
                        "name": "兮兮",
                        "url": "http://www.baidu.com/"

                    },
                    {
                        "name": "菜单",
                        "sub_button": [
                            {
                                "type": "view",
                                "name": "百度一下",
                                "url": "http://www.baidu.com/"
                            },
                            {
                                "type": "click",
                                "name": "放假",
                                "key": "holiday"
                            }]
                    },
                    {
                        "type": "click",
                        "name": "测试",
                        "key": "CESHI"
                     }
                ]
            }

        url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s' % hu_access_token
        response = requests.post(url=url, data=json.dumps(params, ensure_ascii=False).encode('utf-8'), verify=False)
        if response.status_code != 200:
            return """创建菜单失败"""
        else:
            return """创建成功"""
    if content.strip() == '测试回复':
        try:
            count = len(list(quality_questions))
            answer = 1
            WeiXin_Server.send_text_message(openid, quality_questions.get(answer))
            while answer <= count:
                if content.strip() in ['A', 'a', 'B', 'b', 'C', 'c']:
                    answer += 1
                else:
                    WeiXin_Server.send_text_message(openid, """哦豁，Nelly识别不了你的答案，请输入题目中包含答案对应的序号，如“A、B、C”""")
                WeiXin_Server.send_text_message(openid, """恭喜你，已经完成答题""")
            time.sleep(2)
            WeiXin_Server.send_text_message(openid, """稍等片刻，正在为你揭晓答案。。。""")
        except Exception as f:
            with open('error.txt', 'a') as e:
                e.write(f)
    return


# 处理图片信息
def handle_image_message(message):
    return


# 订阅返回信息
def subscribe_message_func(message):
    return """死亡如风，常伴吾身
"""


# 取关返回信息
def un_subscribe_message_func(message):
    return """你轻轻的走，正如你轻轻地来
    """
