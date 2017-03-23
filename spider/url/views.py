#coding=utf-8

from django.shortcuts import render,render_to_response
from url.models import Thread
from url.spider_url_thread import ThreadControl
from drivers.get_ip import get_ip

# Create your views here.

def spider_url(requests):
    thread1_status = False
    url_active = True
    #获取IP
    IP = get_ip()
    #通过IP过滤
    thread_list = Thread.objects.filter(thread_ip=IP)
    #获取总数
    # thread_list = Thread.objects.all()
    print thread_list
    for thread in thread_list:
        c  = ThreadControl()
        try:
            #查看是否处于活跃状态
            status = c.is_alive(thread.thread_name)
            if status:
                #设置状态为1
                thread.thread_status = 1
                thread.save()
            else:
                #设置状态为0
                thread.thread_status = 0
                thread.save()
        except:
            thread.thread_status = 0
            thread.save()
    return render_to_response('spider_url.html',{'thread1_status':thread1_status,"url_active":url_active , "thread_list":thread_list})

def control_spider_url(request):
    th_name = request.POST['id']
    control = request.POST['control']
    print "thread_name is ",th_name
    import time
    time.sleep(5)
    #显示活跃状态
    url_active = True
    # thread = Thread.objects.filter(thread_name=th_name)
    thread = Thread.objects.get(thread_name=th_name)
    print "thread.thread_status is ", thread.thread_status,thread.thread_name

    if control == 'start':
        #状态信息
        # thread1_status = True
        c  = ThreadControl()
        # status = 1
        #出现错误，则线程不存在，因此启动线程
        try:
            status = c.is_alive(th_name)
            print "thread is alive? ",status
            if status:
                print "thread is alive,caonot start twice!"
            else:
                print "start ..........thread1"
                c.start(th_name,1)
        except:
            print "thread is not alive start!!!"
            c.start(th_name,1)
        thread.thread_status = 1
        thread.save()
    if control == 'stop':
        # thread1_status = False
        # status = 0
        c  = ThreadControl()
        try:
            c.stop(th_name)
            thread.thread_status = 0
            thread.save()
        except:
            print "not thread alive"
    #获取IP
    IP = get_ip()
    ##获取所有
    # thread_list = Thread.objects.all()
    #基于IP获取
    thread_list = Thread.objects.filter(thread_ip=IP)
    return render_to_response('spider_url.html',{"thread_name":th_name, "control":control, "thread_list":thread_list,"url_active":url_active})

def spider_url_all(request):
    thread_list = Thread.objects.all()
    all_url_active = True
    print "here"
    return render_to_response('spider_url.html',{"all_url_active":all_url_active, "thread_list":thread_list})
