#coding=utf-8
__author__ = 'shifeixiang'

import time
import thread
import threading
from drivers.webdrivers import get_webdriver
from url.spider_url import get_article_url,get_volume_url

from db.db_redis  import redis_connect,push_redis_list,pop_redis_list
from db.db_mysql import mysql_connect_localhost

class Spider(threading.Thread):
    # __metaclass__ = Singleton
    thread_stop = False
    thread_num = 0
    interval = 0
    behavior = None
    def run(self):
        self.behavior(self,self.thread_num,self.interval)
    def stop(self):
        self.thread_stop = True

class ThreadControl():
    thread_stop = False
    current_thread = {}
    def start(self,thread_num,interval):
        spider = Spider()
        spider.behavior = loaddata
        spider.thread_num = thread_num
        spider.interval = interval
        spider.start()
        self.current_thread[str(thread_num)] = spider
    #判断进程是否活跃
    def is_alive(self,thread_num):
        tt = self.current_thread[str(thread_num)]
        return tt.isAlive()
    #获取当前线程名称
    # def get_name(self):
    def stop(self,thread_num):
        print "stop"
        spider = self.current_thread[str(thread_num)]
        spider.stop()

def loaddata(c_thread,thread_num,interval):
    print "run......"
    driver = get_webdriver()
    if driver == None:
        return 0
    redis_conn = redis_connect()
    if redis_conn == None:
        return 0

    while not c_thread.thread_stop:
        print thread_num,"spider url"
        time.sleep(3)
        #出队列
        main_url = pop_redis_list(redis_conn,'science_main_url')

        print "main_url:",main_url
        if main_url == None:
            print "redis connect error or queue is null"
            break
        else:
            mysql_conn = mysql_connect_localhost()
            if mysql_conn == None:
                print "mysql connect error"
                break
            else:
                volume_url_list = get_volume_url(driver,main_url)
                if volume_url_list == 0:
                    push_redis_list(redis_conn,'science_main_url',main_url)
                    driver.quit()
                    time.sleep(2)
                    print 'restart webdriver'
                    driver = get_webdriver()
                else:
                    if not volume_url_list:
                        continue
                    else:
                        #获取最终文章URL
                        #返回值只做入队列使用
                        article_url_list_all = get_article_url(driver, mysql_conn, main_url, volume_url_list)
                        #超时处理
                        if article_url_list_all == 0:
                            push_redis_list(redis_conn,'science_main_url',main_url)
                            driver.quit()
                            time.sleep(2)
                            print 'restart webdriver'
                            driver = get_webdriver()
                        else:
                            #入消息队列
                            print "push article redis"
                            for article_url in  article_url_list_all:
                                push_redis_list(redis_conn,'science_article_url_tmp',article_url)
                mysql_conn.close()
    print thread_num,"exit"
    driver.close()