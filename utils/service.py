# coding: utf-8
import json

import requests
from config.settings import micro_service_domain, APP_ID, APP_SECRET
from utils.functions import redis_client


# # 对requests方法的重写  直接获取res的json字符串
# class BaseHttpServer:
#     @staticmethod
#     def get(url, params):
#         res = requests.get(url=url, params=params)
#         return res.json()['data']
#
#     @staticmethod
#     def post(url, json_data):
#         res = requests.post(url=url, json=json_data)
#         return res.json()['data']


class WeixinServer:
    """微信公众号服务"""

    @staticmethod
    def get_access_token():
        """获取access_token"""
        hu_access_token = redis_client.get_instance('hu_access_token')
        if hu_access_token:
            return hu_access_token
        else:
            url = "https://api.weixin.qq.com/cgi-bin/token"
            params = {
                'appid': APP_ID,
                'secret': APP_SECRET,
                'grant_type': 'client_credential'
            }
            response = requests.get(url, params)
            res = response.json()
            redis_client.set_instance('hu_access_token', res['access_token'])
            return res['access_token']

    @staticmethod
    # def send_text_message(openid, content):
    #     #     """发送文本消息"""
    #     #     json_data = {
    #     #         'openid': openid,
    #     #         'content': content
    #     #     }
    #     #     url = "%s/api/weixin/service_center/send_text_message/" % micro_service_domain
    #     #     data = requests.post(url, json_data)
    #     #     return data
    def send_text_message(self, openid, content):
        """发送文本消息"""
        url = "https://api.weixin.qq.com/cgi-bin/message/custom/send"
        querystring = {
            "access_token": self.get_access_token}

        payload = (
                "{\"touser\": \"%s\", \"msgtype\": \"text\",  \"text\": {\"content\": \"%s\" }}" % (
            openid, content)).encode(
            'utf-8')
        headers = {
            'Content-Type': "application/json",
            'Cache-Control': "no-cache",
            'Postman-Token': "3a32082a-0052-5591-5a7e-bf815defb396"
        }

        response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
        return response.json()

    # 调用微信接口向用户发送模板消息
    def send_template_inform(self, params):
        access_token = self.get_access_token()
        url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s' % access_token
        response = requests.post(url=url, data=json.dumps(params), headers={'Content-Type': 'application/json'})
        res = response.content
        print(res)
        return response

    @staticmethod
    def code_authorize(code):
        """通过code获取网页授权"""
        url = "%s/api/weixin/service_center/code_authorize/" % micro_service_domain
        params = {'code': code}
        data = requests.get(url, params)
        return data

    @staticmethod
    def get_web_user_info(openid, access_token):
        """获取网页授权用户信息"""
        url = "%s/api/weixin/service_center/get_web_user_info/" % micro_service_domain
        data = requests.get(url, {'openid': openid, 'access_token': access_token})
        return data

    @staticmethod
    def get_base_user_info(openid, access_token):
        """获取基础的用户信息(非网页授权)"""
        url = "%s/api/weixin/service_center/get_user_info/" % micro_service_domain
        data = requests.get(url, {'openid': openid, 'access_token': access_token})
        return data

    @staticmethod
    def get_temporary_qr_code(action_name, scene_id, expired_time=7 * 24 * 60 * 60):
        """获取临时二维码"""
        url = "%s/api/weixin/service_center/temporary_qr_code/" % micro_service_domain
        json_data = {
            "action_name": action_name,
            "scene_id": scene_id,
            "expired_time": expired_time
        }
        data = requests.post(url, json_data)
        return data['qr_img_url']

    @staticmethod
    def get_forever_qr_code(action_name, scene_id):
        """获取永久二维码"""
        url = "%s/api/weixin/service_center/forever_qr_code/" % micro_service_domain
        json_data = {
            "action_name": action_name,
            "scene_id": scene_id,
        }
        data = requests.post(url, json_data)
        return data['qr_img_url']

    @staticmethod
    def img_content_send(access_token, openid, articles):
        url = "%s/api/weixin/service_center/send_img_content_message/" % micro_service_domain
        data = {
            "access_token": access_token,
            "openid": openid,
            "articles": articles
        }
        data = requests.post(url, json_data=data)
        return data

    @staticmethod
    def upload_medias(media_type, media_file, openid, access_token):
        """上传图片"""
        with open(media_file, "rb") as upload_media_file:
            url = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s" % (access_token, media_type)
            res = requests.post(url, files={"media": upload_media_file})
            print(res.content)
            print(res.text)
            url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s' % access_token
            data = {
                "touser": openid,
                "msgtype": "image",
                "image": {
                    "media_id": res.json().get('media_id', 'error_occur')
                    # "media_id": 'noK49V6hsstPONhEuW-rFlq_6xNHdSQQk-qALOdin76PmMO3HED6kgqmVSGlKHGf'
                }
            }
            res = requests.post(url=url, json=data)
            return res.json()

    def get_user_info(self, user_id, lang="zh_CN"):
        """
        获取用户基本信息。

        :param user_id: 用户 ID 。 就是你收到的 `Message` 的 source
        :param lang: 返回国家地区语言版本，zh_CN 简体，zh_TW 繁体，en 英语
        :return: 返回的 JSON 数据包
        """
        res = requests.get(url="https://api.weixin.qq.com/cgi-bin/user/info",
                           params={
                               "access_token": self.get_access_token(),
                               "openid": user_id,
                               "lang": lang
                           })
        print(res.json())
        return res.json()

    # 调用微信接口向用户发送模板消息
    def send_template_messages(self, params):
        access_token = self.get_access_token()
        url = "https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token=" + access_token
        response = requests.post(url=url, data=json.dumps(params), headers={'Content-Type': 'application/json'})
        if response.status_code != 200:
            raise Exception('连接微信服务器异常')
        res = response.json()
        print(res)
        return

    @classmethod
    def send_customer_message(self,params):
        access_token = self.get_access_token()
        url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={}".format(access_token)
        response = requests.post(url=url, data=json.dumps(params,ensure_ascii=False).encode('utf-8'), headers={'Content-Type': 'application/json',"charset": "UTF-8"})
        print('response:->{}'.format(response.json()))
        if response.status_code != 200:
            raise Exception('连接微信服务器异常')
        res = response.json()
        print(res)
        return

    def get_openid(self):
        access_token = self.get_access_token()
        params = {'access_token': access_token}
        url = "https://api.weixin.qq.com/cgi-bin/user/get"
        response = requests.get(url=url, params=params, headers={'Content-Type': 'application/json', "charset": "UTF-8"})
        res = response.json()
        openid_list = res['data']['openid']
        openid = openid_list[1]
        return openid


WeiXin_Server = WeixinServer()
