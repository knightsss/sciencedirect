#coding=utf-8
__author__ = 'shifeixiang'

import time
import thread
import threading
#webdriver
from drivers.webdrivers import get_webdriver
#redis
from db.db_redis import redis_connect,push_redis_list,pop_redis_list

from db.db_mysql import mysql_connect_localhost,insert_mysql_t_sciencedirect_journals_article

#详细的获取信息
from article.spider_article import get_periodical


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
        print thread_num,"spider article"
        url = pop_redis_list(redis_conn,'science_article_url')
        if url == None:
            print "url queue is null"
            break
        else:
            print url,"====================================="
            mysql_conn = mysql_connect_localhost()
            if mysql_conn == None:
                print "mysql connect error!"
                break
            else:
                time.sleep(2)
                request_flag = get_periodical(driver,url,mysql_conn)
                if request_flag == 0:
                    push_redis_list(redis_conn,'science_article_url',url)
                    driver.quit()
                    time.sleep(2)
                    print 'restart webdriver'
                    driver = get_webdriver()
            # time.sleep(3)
            mysql_conn.close()
    #结束退出
    print thread_num," quit"
    driver.close()
