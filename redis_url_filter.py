# coding=utf-8
__author__ = 'shifeixiang'

from datetime import datetime
import time
import redis
#布隆过滤器
from pybloom import BloomFilter, ScalableBloomFilter

def redis_connect():
    #带密码连接
    # r = redis.StrictRedis(host='localhost', port=6379, password='npq8pprjxnppn477xssn')
    try:
        redis_conn = redis.Redis(host='localhost',port=6379,db=0)
    except:
        print "connect redis error"
        return None
    return redis_conn


#出消息队列
def pop_redis_list(redis_conn):
    try:
        url = redis_conn.lpop("science_article_url_tmp")
        # print "pop ok"
    except:
        # redis_conn = redis_connect()
        print "pop faild"
        url = None
    return url

#入最终的article_url队列
def push_redis_list(redis_conn,auditor_mid):
    try:
        redis_conn.rpush("science_article_url",auditor_mid)
    except:
        redis_conn = redis_connect()

#读取布隆过滤器文件
def read_redis_bf_from_file():
    try:
        f_r = open('bf_redis','rb')
        bf_redis = BloomFilter.fromfile(f_r)
        f_r.close()
        print "file is exists,ok"
    except:
        f_w = open('bf_redis','wb')
        bf_redis = BloomFilter(capacity=10000000, error_rate=0.001)
        bf_redis.tofile(f_w)
        f_w.close()
        print "file not exists,new"
    return bf_redis

if __name__ == '__main__':
    redis_conn = redis_connect()
    #加载文件
    bf_redis = read_redis_bf_from_file()
    count = 1
    #出队
    while(1):
        wid = pop_redis_list(redis_conn)
        print count," wid is " ,wid
        if wid == None:
            print "wait 300s"
            time.sleep(300)
        else:
            #判断是否入队
            if wid in bf_redis:
                print wid,"already in bf_redis"
            else:
                # print wid,"add  bf_redis"
                #入队
                push_redis_list(redis_conn,wid)
                # push_redis_msg_list(redis_conn,wid)
                # push_redis_content_list(redis_conn,wid)
                bf_redis.add(wid)
            if count%500 == 0:
                print "load to bf file"
                f_redis = open('bf_redis','wb')
                bf_redis.tofile(f_redis)
                f_redis.close()
            count = count + 1


