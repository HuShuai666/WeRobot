from config.settings import TEMPLATE_INFO
from .service import WeiXin_Server


def remind(message):
    openid = message.source
    data = {
        "touser": openid,
        "template_id": TEMPLATE_INFO['REMIND'],
        "data": {
            "first": {
                "value": "亲爱的李后居同学，你的寒假即将到来！",
                "color": "#173177"
            },
            "keyword1": {
                "value": "别日塔瞎，窝在家里打lol，说好的女朋友呢？",
                "color": "#173177"
            },
        }
    }
    return WeiXin_Server.send_template_inform(data)
