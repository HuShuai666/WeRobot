# 测试回复的具体逻辑
from celery_task.tasks import upload_medias
from src.qualities_reply import quality_questions
from utils.redis_helper import redis_client
from utils.service import WeiXin_Server
import time


def quality_test(content, openid, hu_access_token):
    if redis_client.hget('hu_cs', openid):
        # 获取redis中用户的答题进度
        qid = int(redis_client.hget('hu_cs', openid)) + 1
        if qid == 9:
            response = WeiXin_Server.send_text_message(openid, """答题完毕，请等待结果...""")
            upload_medias.delay('image', '/workspace/Vote/media/images/1.jpg', openid, hu_access_token)
            return
        if content.strip() in ['A', 'a', 'B', 'b', 'C', 'c']:
            response = WeiXin_Server.send_text_message(openid, quality_questions.get(qid))
            redis_client.hset('hu_cs', openid, qid)
        else:
            response = WeiXin_Server.send_text_message(openid, """你的输入有误！！！""")
    else:
        redis_client.hset('hu_cs', openid, 1)
        response = WeiXin_Server.send_text_message(openid, quality_questions.get(1))
    return
