# coding: utf-8
import logging
import requests
from utils.service import WeixinServer
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
        response = requests.post(url=url, data=json.dumps(params), verify=False)

        return """创建菜单成功"""
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
