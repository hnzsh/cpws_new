import datetime
# from redis_db import db_redis

import time


import redis

REDIS_HOST = "192.168.0.89"
REDIS_PORT = 16379
REDIS_PW = "@XDOPyZ&mCTQKe$c"
REDIS_DB = 0
pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True, password=REDIS_PW, db=REDIS_DB)
db_redis = redis.Redis(connection_pool=pool)




def get_ip(name):
    score_th =  int(db_redis.get("score")  if db_redis.get("score") else 70)
    key, key_delete = name + "_ip", name + "_ip_del"
    if datetime.datetime.now().minute % 20 == 0:
        all_d = db_redis.hgetall("ip_score")
        if len(all_d) > 20:
            for k, v in all_d.items():
                if int(v) < 70:
                    db_redis.hdel("ip_score", k)
    num = 0
    while True:
        ips = db_redis.spop(key, 1)
        if ips:
            ip = ips[0]
            key_web = ip + "_" + name
            ip_score = db_redis.hget("ip_score",key_web)
            if not ip_score:
                db_redis.hset("ip_score",key_web, 100)
                return ip
            elif int(ip_score) > score_th:
                return ip
            else:
                db_redis.hdel("ip_score",key_web)
                db_redis.srem(key, ip)
                db_redis.sadd(key_delete, ip)
                print("删除ip:%s" % ip)
        else:
            print("暂无代理ip")
            time.sleep(5)
            num += 1
            if num > 20:
                db_redis.delete(key_delete)
                num = 0