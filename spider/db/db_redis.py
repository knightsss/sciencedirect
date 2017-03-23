#coding=utf-8
__author__ = 'shifeixiang'
import redis

def redis_connect():
    #带密码连接
    # r = redis.StrictRedis(host='localhost', port=6379, password='npq8pprjxnppn477xssn')
    try:
        redis_conn = redis.Redis(host='localhost',port=6379,db=0)
    except:
        print "connect redis error"
        redis_conn = None
    return redis_conn

#出wid消息队列
###redis连接 redis list名字
def pop_redis_list(redis_conn,redis_list_name):
    try:
        url = redis_conn.lpop(redis_list_name)
    except:
        print "pop faild"
        url = None
    return url

# #入临时消息队列
###redis连接 redis list名字 value
def push_redis_list(redis_conn,redis_list_name,value):
    try:
        redis_conn.rpush(redis_list_name,value)
    except:
        redis_conn = redis_connect()