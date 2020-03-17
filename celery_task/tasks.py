import requests
from celery_task.celery import celery_app


@celery_app.task(name="celery_upload_media")
def upload_medias(media_type, media_file, openid, access_token):
    """从服务器上传图片到微信   然后发送给用户"""
    with open(media_file, "rb") as upload_media_file:
        url = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s" % (access_token, media_type)
        res = requests.post(url, files={"media": upload_media_file})
        url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s' % access_token
        data = {
            "touser": openid,
            "msgtype": "image",
            "image": {
                "media_id": res.json().get('media_id', 'error_occur')
            }
        }
        res = requests.post(url=url, json=data)
        return res.json()
