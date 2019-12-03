import redis
from werobot.session.redisstorage import RedisStorage

db = redis.Redis(db=1,charset='utf-8')
session_storage = RedisStorage(db, prefix='')