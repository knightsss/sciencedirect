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

1.2 redis安装相关(仅安装在一台机器即可)
---

    参考地址：http://www.runoob.com/redis/redis-install.html

1.3 mysql安装(主机安装)
-----------
略

1.4 Phantomjs安装
---------------

    下载地址：http://phantomjs.org/download.html
    直接加压即可，记住路径，后面需要phantomjs.exe

2. 相关设置
-----

模式设置（用户和权限表与数据库同步）
------------------

打开/spider/settings.py
根据自己本地数据库设置对应的，数据库名、用户名、密码、端口号、localhost

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

数据库设置（供多个数据库连接使用），同样设置对应的名字
---------------------------

打开/db/db_mysql.py

    def mysql_connect_localhost():
    try:
        mysql_conn = MySQLdb.connect("localhost","root","123456","db_sciencedirect")
    except:
        print "connect mysql error"
        return None
    return mysql_conn

redis设置
-------
代开/db/db_redis.py

    def redis_connect():
    try:
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

3. 启动前的准备
---------
需要将model同步到mysql数据库
打开/search/settings.py
找到如下代码

       INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'url',
        'article',
    )
    
'django.contrib.sessions','url',article三行保留，其它注释掉，也可以不注释，这可以自己选择，不注释的情况下数据库中会多几张用不到的表。
注：如果注释掉，在完成4.同步model之后记得把注释取消！！！

4. 同步model
----------
进入到manage.py的同级目录
执行：

    >python manage.py validate          #(检查是否有误)
    >python manage.py sqlall url        #（创建表）
    >python manage.py sqlall article    #（创建表）
    >python manage.py syncdb            #（同步到数据库）
    

5. 后台数据库插入数据
------------
执行上面(步骤四)语句后会在db_sciencedirect（步骤二）的数据库中出现两张表
url_thread（用于采集url的线程表）

        
        thread_id,
        thread_ip,
        thread_name,
        thread_status,
        
        mysql插入一条记录（可插入多条，但必须保证线程名称不一样，所有机器都不允许出现同样的线程名）
        insert into db_sciencedirect.`url_thread`(thread_id,thread_ip,thread_name,thread_status) values(1,'127.0.0.1','spider_url_thread1',0)

article_thread（用于采集文章的线程表）

        thread_id,
        thread_ip,
        thread_name,
        thread_status,
        
        mysql插入一条记录（可插入多条，但必须保证线程名称不一样，所有机器都不允许出现同样的线程名）
        insert into db_sciencedirect.`article_thread`(thread_id,thread_ip,thread_name,thread_status) values(1,'127.0.0.1','spider_article_thread1',0)

在数据库中新增表：
    
    作者表
    create table db_sciencedirect.t_sciencedirect_journals_author(
    author_id varchar(20),
    article_url varchar(100), 
    author_name varchar(100),
    author_affiliation varchar(500),
    author_emails varchar(100),
    author_correspondences varchar(200)
    )
    
    
    期刊内容表
    create table db_sciencedirect.t_sciencedirect_journals_article(
    article_id varchar(20),
    article_url varchar(100),   #   期刊论文的唯一URL http://www.sciencedirect.com/science/article/pii/S2212671614001024
    publication_title varchar(100),    #   AASRI Procedia
    volume varchar(100),   #  Volume 9, 2014, Pages 2-7
    article_title varchar(200),   #   A New Texture Analysis Approach for Iris Recognition
    author_group varchar(200),     #多个作者信息
    doilink varchar(100),    #链接  http://dx.doi.org/10.1016/j.actbio.2017.01.035
    abstract_author text,    #摘要
    keywords varchar(200)  #关键词
    )
    
    
    URL关系表
    create table db_sciencedirect.t_sciencedirect_journals_url(
    url_id varchar(20),
    main_url varchar(100),   #   主页中每个选项的URL    /science/journal/22126716
    volume_url varchar(100),   #  主页每个选项链接下的对应的卷URL   http://www.sciencedirect.com/science/journal/22126716     #href: /science/journal/22126716/9
    article_url varchar(100)   #   每卷对应的期刊的URL，唯一性    http://www.sciencedirect.com/science/article/pii/S2212671614001024
    )

    #类别表
    create table db_sciencedirect.t_sciencedirect_journals_class(
    class_id varchar(20),
    subject_name varchar(200),   #   主题、科目
    son_subject_name varchar(200),    #  子 主题、科目
    grandson_subject_name varchar(200),   #  孙子 主题、科目
    main_url varchar(200)   #   主页中每个选项的URL    /science/journal/22126716
    )

6. 启动登陆
-----
在manage.py的目录下，执行
>python manage.py runserver

打开浏览器(这个时候并不能跑任务，因为redis队列面还没有任务，接下来添加任务)
http://127.0.0.1:8000/spider_url/   爬取url线程

http://127.0.0.1:8000/spider_article/   爬取文章线程


7 redis添加任务并启动
-----------
这里需要两个redis的队列
一个存放主页的main_url
另外一个存放文章的article_url
第一步获取主页的main_url

操作方式：
打开get_all_main_url.py（在根目录下的一个单独文件），需要配置一下#phantomjs和redis路径，还有一个参数，如果测试使用pull_times = 5，如果跑完所有需要设置200，大概十几分钟跑完。
命令行运行(在get_all_main_url同级目录下执行)：

    >python get_all_main_url.py
会在redis下生成一个队列science_main_url

任务添加完成后可以在浏览器中启动采集url(先启动)，目的是获取article_url并存入第二个消息队列

确保science_article_url_tmp队列有数据时再启动获取文章采集（后启动）


8. 补充
最后补充的是类别的科目、主题以及子科目等需要单独跑，脚本已经写好，大概几个小时跑完所有科目。
打开/spider_class.py,配置好数据库连接及phantomjs路径
执行命令：>python spider_class.py
将会把数据存储在mysql数据库中，记得提前创建t_sciencedirect_journals_class
我这里也可以跑一下，直接把每个主题的数据发过去。


9 布隆过滤器（将主机上science_article_url_tmp队列过滤重复后存入science_article_url队列）
>pip install pybloom

在正式采集的时候启动该脚本
>python redis_url_filter.py
该脚本将science_article_url_tmp消息队列里的信息通过布隆过滤器
存入到最终的science_article_url，这里可以保证重复的URL不再入队
避免文章的重复采集。

注：正式采集的时候需要将/article/spider_article_thread.py文件更改
原始：url = pop_redis_list(redis_conn,'science_article_url_tmp')
更改后：url = pop_redis_list(redis_conn,'science_article_url')


脚本启动后将会生成bf_redis文件，每5分钟更新一次，这里记录了布隆过滤器的状态，采集完毕可自行备份。