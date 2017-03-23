#coding=utf-8
__author__ = 'shifeixiang'

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import redis
import MySQLdb
import os

#设置200次获取所有
pull_times = 5

def get_webdriver():
    #phantomjs
    driver = webdriver.PhantomJS('E:\\phantomjs\\phantomjs-2.1.1-windows\\phantomjs-2.1.1-windows\\bin\\phantomjs')



    return driver

#连接redis
def redis_connect():
    #带密码连接
    # r = redis.StrictRedis(host='localhost', port=6379, password='npq8pprjxnppn477xssn')
    try:
        redis_conn = redis.Redis(host='localhost',port=6379,db=0)
        # redis_conn = redis.StrictRedis(host='192.168.15.111', port=6379, password='npq8pprjxnppn477xssn',db=0)
    except:
        print "connect redis error"
        redis_conn = None
    return redis_conn

#入队
###redis连接 redis list名字 value
def push_redis_list(redis_conn,redis_list_name,value):
    try:
        redis_conn.rpush(redis_list_name,value)
    except:
        redis_conn = redis_connect()

#获取主页里所有链接
def get_main_url(driver,url):

    driver.get(url)
    time.sleep(3)
    for i in range(pull_times):
        print "pull ",str(i)
        js="var q=document.body.scrollTop=" + str((i+1)*1000)
        driver.execute_script(js)
        time.sleep(1)
    print "结束下拉"

    soup = BeautifulSoup(driver.page_source)

    elements = soup.find_all(class_='browseimpBrowseRow')
    main_url_list = []
    for element in elements:
        main_url = element.a['href'].encode('utf-8')
        if  'sciencedirect' in main_url:
            pass
        else:
            main_url = 'http://www.sciencedirect.com' + main_url
        print main_url
        main_url_list.append(main_url)
    print len(main_url_list)
    return main_url_list





if __name__ == '__main__':
    #获取主页多有url
    url = 'http://www.sciencedirect.com/science/journals'
    main_url_redis_name = 'science_main_url'
    driver = get_webdriver()
    main_url_list = get_main_url(driver,url)
    redis_conn = redis_connect()
    redis_conn.delete(main_url_redis_name)
    for main_url in  main_url_list:
        push_redis_list(redis_conn, main_url_redis_name, main_url)
    driver.close()