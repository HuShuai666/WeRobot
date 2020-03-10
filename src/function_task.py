# 测试回复的具体逻辑
from src.qualities_reply import quality_questions
from utils.redis_helper import redis_client
from utils.service import WeiXin_Server
import json


def quality_test(content, openid):
    if content.strip() == "重新测试":
        redis_client.delete('hu_cs')
    WeiXin_Server.send_text_message(openid, """1""")
    if redis_client.hget('hu_cs', openid):
        WeiXin_Server.send_text_message(openid, """2""")
        WeiXin_Server.send_text_message(openid, f'{openid}')
        # 获取redis中用户的答题进度
        qid = int(redis_client.hget('hu_cs', openid)) + 1
        if qid == 9:
            response = WeiXin_Server.send_text_message(openid, """答题完毕！！！""")
        if content.strip() in ['A', 'a', 'B', 'b', 'C', 'c']:
            response = WeiXin_Server.send_text_message(openid, quality_questions.get(qid))
            redis_client.hset('hu_cs', openid, qid)
        else:
            response = WeiXin_Server.send_text_message(openid, """你的输入有误！！！""")
    else:
        redis_client.hset('hu_cs', openid, 1)
        response = WeiXin_Server.send_text_message(openid, quality_questions.get(1))
    return