# coding: utf-8
import redis


redis_valid_time = 60 * 60

REDIS_CONFIG = {
    'host':'localhost',
    'port':6379
}


# 暂时没用
class RedisClient:
    @property
    def redis_client(self):
        pool = redis.ConnectionPool(host=REDIS_CONFIG['host'], port=REDIS_CONFIG['port'])
        client = redis.Redis(connection_pool=pool,db=1)
        return client

    def exist_key(self, key):
        """根据key判断元素是否存在缓存中"""
        return self.redis_client.exists(key)

    def get_instance(self, key, delete_cache=False):
        """根据key获取value（string类型数据操作）"""
        redis_instance = self.redis_client.get(key)
        if not redis_instance:
            return None
        try:
            res = eval(redis_instance)
        except:
            res = str(redis_instance, encoding='utf-8')
        if delete_cache:
            self.redis_client.delete(key)
        return res

    def get_instance_total(self, key, delete_cache=False):
        """根据key获取value（string类型数据操作），如果是None则返回 0 """
        redis_instance = self.redis_client.get(key)
        if not redis_instance:
            return 0
        try:
            res = eval(redis_instance)
        except:
            res = str(redis_instance, encoding='utf-8')
        if delete_cache:
            self.redis_client.delete(key)
        return res

    def mget(self, keys):
        """批量获取多个key的value值"""
        redis_instance = self.redis_client.mget(keys)
        try:
            res = [eval(str(ins)) for ins in redis_instance]
        except:
            res = str(redis_instance, encoding='utf-8')
        return res

    def mget_total(self, keys):
        """批量获取多个key的value值"""
        redis_instance = self.redis_client.mget(keys)
        try:
            res = [0 if not ins else int(ins) for ins in redis_instance]
        except:
            res = str(redis_instance, encoding='utf-8')
        return res

    def set_instance(self, key, value, default_valid_time=redis_valid_time):
        """设置键值对（string类型数据操作）"""
        self.redis_client.set(key, value, default_valid_time)
        return

    def delete(self, key):
        """删除键值对（string类型数据操作）"""
        self.redis_client.delete(key)
        return

    def incr_instance(self, key, amount=1):
        """根据key自增amount（string类型数据操作）"""
        self.redis_client.incr(key, amount)
        return

    def decr_instance(self, key, amount=1):
        """根据key自减amount（string类型数据操作）"""
        self.redis_client.decr(key, amount)
        return

    def sadd(self, name, *value):
        """根据key添加数据到集合set（set类型数据操作）"""
        self.redis_client.sadd(name, *value)
        return

    def sismember(self, name, value):
        """判断集合name中是否存在value元素（set类型数据操作）"""
        return self.redis_client.sismember(name, value)

    def smembers(self, name):
        """返回集合name中所有元素（set类型数据操作）"""
        return self.redis_client.smembers(name)

    def scard(self, name):
        """返回集合name中元素个数（set类型数据操作）"""
        return self.redis_client.scard(name)

    def spop(self, name):
        """从集合右侧返回并移除一个成员（set类型数据操作）"""
        return self.redis_client.spop(name)

    def srandmember(self, name, numbers):
        """从name对应的集合中随机获取numbers个元素（set类型数据操作）"""
        data_list = self.redis_client.srandmember(name, numbers)
        return [str(data, encoding='utf-8') for data in data_list]

    def srem(self, name, values):
        """在name对应的集合中删除某些值（set类型数据操作）"""
        return self.redis_client.srem(name, values)

    def hlen(self,name):
        return self.redis_client.hlen(name)

    def hset(self, name, key, value):
        """在name对应的集合中添加某些值（hash类型数据操作）"""
        return self.redis_client.hset(name, key, value)

    def hmset(self, name, mapping):
        """在name对应的集合中批量添加某些值（hash类型数据操作）"""
        return self.redis_client.hmset(name, mapping)

    def hget(self, name, key):
        """在name对应的集合中获取key的元素（hash类型数据操作）"""
        return self.redis_client.hget(name, key)

    def hdel(self, name, key):
        """删除key中对应的field"""
        return self.redis_client.hdel(name, key)

    def hmget(self, name, keys, *args):
        """在name对应的集合中批量获取元素（hash类型数据操作）"""
        return self.redis_client.hmget(name, keys, *args)

    def zadd(self, name, *args, **kwargs):
        """在name对应的有序集合中批量添加元素（zset类型数据操作）"""
        """zadd('test', 'redis', 100, 'mysql', 200, memcached=300,postgresql=400)"""
        return self.redis_client.zadd(name, *args, **kwargs)

    def zcard(self, name):
        """在name对应的有序集合中获取元素个数（zset类型数据操作）"""
        return self.redis_client.zcard(name)

    def zcount(self, name, min, max):
        """计算在有序集合中指定区间分数的成员数（zset类型数据操作）"""
        return self.redis_client.zcount(name, min, max)

    def zincrby(self, name, value, amount=1):
        """有序集合中对指定成员的分数加上增量 amount（zset类型数据操作）"""
        return self.redis_client.zincrby(name, value, amount)

    def zrange(self, name, start, end, withscores=False):
        """通过索引区间返回有序集合成指定区间内的成员"""
        return self.redis_client.zrange(name, start, end, withscores=withscores)

    def zrevrank(self, name, value):
        """获取成员排名"""
        ret = self.redis_client.zrevrank(name, value)
        return ret

    # def hincrby(self,key,field,value):
    #     return self.redis_client.hincrby(key,field,value)

    def lpush(self, name, *values):
        return self.redis_client.lpush(name, *values)

    def lrange(self, name, start, stop):
        return self.redis_client.lrange(name, start, stop)

    def zrevrange(self, name, start, end, withscores=False):
        """通过索引区间返回有序集合成指定区间内的成员,递减排序"""
        return self.redis_client.zrevrange(name, start, end, withscores=withscores)

    def expire(self, name, time):
        """设置过期时间"""
        return self.redis_client.expire(name,time)

redis_client = RedisClient()
