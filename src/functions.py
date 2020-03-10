# coding: utf-8
import logging
import requests
import time
from src.qualities_reply import quality_questions
from utils.redis_helper import redis_client
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
        qid = int(redis_client.hget('hu_cs', openid)) + 1
        # 如果redis中存在该用户的题号 就向微信发送问题
        if qid:
            # 如果答案标准
            if content.strip() in ['A', 'a', 'B', 'b', 'C', 'c']:
                redis_client.hset('hu_cs', openid, qid)
                response = WeiXin_Server.send_text_message(openid, quality_questions.get(qid))
            else:
                WeiXin_Server.send_text_message(openid, '哦豁，Nelly识别不了你的答案，请输入题目中包含答案对应的序号，如“A、B、C”')
            if qid == 9:
                WeiXin_Server.send_text_message(openid, '恭喜你，已经完成答题')
        else:
            redis_client.hset('hu_cs', openid, 1, 60*2)
            response = WeiXin_Server.send_text_message(openid, quality_questions.get(1))
    return json.dumps(response)


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
