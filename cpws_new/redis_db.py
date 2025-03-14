import redis

REDIS_HOST_TASK = '192.168.0.89'
REDIS_PORT_TASK = 16379
REDIS_PW_TASK = '@XDOPyZ&mCTQKe$c'
REDIS_DB_TASK = 1


REDIS_HOST = "192.168.0.89"
REDIS_PORT = 16379
REDIS_PW = "@XDOPyZ&mCTQKe$c"
REDIS_DB = 0
pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True, password=REDIS_PW, db=REDIS_DB)
db_redis = redis.Redis(connection_pool=pool)

pool_ALI = redis.ConnectionPool(host=REDIS_HOST_TASK, port=REDIS_PORT_TASK, decode_responses=True, password=REDIS_PW_TASK, db=REDIS_DB_TASK)
db_redis_task = redis.Redis(connection_pool=pool_ALI)
