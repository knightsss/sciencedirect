使用说明（主机）
====

1. windows搭建环境
----

1.1 python相关
------------

环境python2.7
前端框架使用django
如果没有需要安装django(可以通过pip list查看)
python安装：

    python2.7下载地址：https://www.python.org/downloads/
    下载：2.7.9版本
    安装完成设置python.exe环境变量,并设置python/scripts目录下pip.exe环境变量
    命令行测试：python
    命令行测试：pip list
    查看是否正常运行
    
安装django命令:

    >pip install django==1.6

安装bs4

    >pip install bs4

安装redis

    >pip install redis
安装selenium

    >pip install selenium

安装requests

    >pip install requests

安装MySQLdb

    可以通过网站下载：http://www.codegood.com/archives/129
    64位下载这个版本：MySQL-python-1.2.3.win-amd64-py2.7.exe (1.0 MiB)



1.2 Phantomjs安装
---------------

    下载地址：http://phantomjs.org/download.html
    直接加压即可，记住路径，后面需要phantomjs.exe

2. 相关设置
-----

模式设置（用户和权限表与数据库同步）
------------------

打开/spider/settings.py
根据自己本地数据库（远程数据库）设置对应的，数据库名、用户名、密码、端口号、localhost（远程主机IP）

    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_sciencedirect',
        'USER':'root',
        'PASSWORD':'123456',
        'HOST':'localhost',
        'PORT':'3308',
    }
}

数据库设置（供多个数据库连接使用），同样设置对应的名字，这里host设置主机的IP地址,
---------------------------

打开/db/db_mysql.py

    def mysql_connect_localhost():
    try:
        mysql_conn = MySQLdb.connect("主机IP","root","123456","db_sciencedirect")
    except:
        print "connect mysql error"
        return None
    return mysql_conn

redis设置(host设置主机IP地址，如果有密码设置密码)
-------
代开/db/db_redis.py

    def redis_connect():
    try:
        #带密码设置
        #redis_conn = redis.StrictRedis(host='localhost', port=6379, password='npq8pprjxnppn477xssn')
        #不带密码设置
        redis_conn = redis.Redis(host='localhost',port=6379,db=0)
    except:
        print "connect redis error"
        redis_conn = None
    return redis_conn

phantomjs设置
-----------
打开/drivers/webdrivers.py 其中路径设置成自己安装phantomjs的路径

    def get_webdriver():
    try:
        driver = webdriver.PhantomJS('E:\\phantomjs\\phantomjs-2.1.1-windows\\phantomjs-2.1.1-windows\\bin\\phantomjs')
    except:
        driver = None
    return driver


3. 同步model
----------
进入到manage.py的同级目录
执行：

    >python manage.py validate          #(检查是否有误)
    >python manage.py sqlall url        #（创建表）
    >python manage.py sqlall article    #（创建表）
    >python manage.py syncdb            #（同步到数据库）
    

4. 启动登陆
-----
在manage.py的目录下，执行
>python manage.py runserver

打开浏览器
http://127.0.0.1:8000/spider_url/   爬取url线程

http://127.0.0.1:8000/spider_article/   爬取文章线程


