#coding=utf-8
__author__ = 'shifeixiang'
import time
import requests
from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from db.db_mysql import mysql_connect_localhost,insert_mysql_t_sciencedirect_journals_article,insert_mysql_t_sciencedirect_journals_author

def get_periodical(driver,url,mysql_conn):
    # response = requests.get(url)
    # print response.text.encode('utf-8')
    # request = urllib2.Request(url)
    # response = urllib2.urlopen(request)
    try:
        print "start get url"
        driver.get(url)
        try:
            element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID , "ccs-journalsLink")))
        except:
            print "request timeout"
            return 0
        print "get fininsh"
        # print driver.page_source
        time.sleep(3)

        current_page_all = driver.page_source
        soup = BeautifulSoup(current_page_all)
    except:
        print "request error,please wait..."
        time.sleep(30)
        return 0
    try:
        #最为判断使用
        flag = soup.find(class_='publication-title-link')
        #当没有元素时，返回None
        # print flag
        if flag == None:
            #方式二处理
            # if 1:
            try:
                #发布题目
                publication_title = soup.find(class_='publicationHead').div.string    #unicode类型
                publication_title_str = publication_title.encode('utf-8')
                # print"publication_title_str:", publication_title_str,type(publication_title_str)

                #volume
                volume_str = ''
                volumes = soup.find(class_='volIssue').stripped_strings
                for volume in volumes:
                    volume_str = volume_str + volume.encode('utf-8')
                # print "type volume_str:",type(volume_str)
                # print "volume_str:",volume_str

                #获取article_title文章标题
                article_title_str = ''
                article_titles = soup.find(class_='svTitle').stripped_strings
                for article_title in article_titles:
                    article_title_str = article_title_str + article_title.encode('utf-8')
                    # print 'type article_title',type(article_title.encode('utf-8'))
                # print 'article_title',article_title.encode('utf-8')

                #作者组
                author_group_str = ''
                author_groups = soup.find_all(class_='authorName')
                for author_group in author_groups:
                    author_group_str = author_group_str + unicode(author_group.string).encode('utf-8') + ';'
                    # print  'unicode(author_group.string).encode utf-8:',type(unicode(author_group.string).encode('utf-8'))
                    # print 'author_group:',author_group.string
                # print "author_group_str:",author_group_str

                #链接
                doilink = soup.find(class_='doiLink').a['href']
                doilink_str = doilink.encode('utf-8')
                # print 'type doilink.encode utf-8',type(doilink.encode('utf-8'))
                # print 'doilink_str',doilink_str,type(doilink_str)

                #abstract
                abstracts = soup.find(class_='abstract').stripped_strings
                count = 0
                for abstract in abstracts:
                    if count == 1:
                        abstract_str =  abstract.encode('utf-8')
                    count = count + 1
                # print "abstract_str:",abstract_str, type(abstract_str)

                #获取keyword
                keyword_str = ''
                keywords = soup.find(class_='keyword').stripped_strings
                for keyword in keywords:
                    keyword_str = keyword_str + keyword.encode('utf-8')
                    # print "keyword:", keyword
                # print 'keyword_str:',keyword_str


                #写入数据库 文章表
                article_id = str(int(time.time()))
                #id  url
                #publication_title_str  volume_str article_title_str  author_group_str  doilink_str abstract_str keyword_str
                print "+++article2 insert into mysql+++"
                insert_mysql_t_sciencedirect_journals_article(mysql_conn,article_id,url,publication_title_str,volume_str,article_title_str,author_group_str,doilink_str, abstract_str, keyword_str)
                print "+++article2 insert into over+++"

                driver_authors = driver.find_elements_by_class_name('authorName')
                count = 0
                for driver_author in driver_authors:
                    print count
                    count = count + 1

                #开始作者信息采集
                for driver_author in driver_authors:
                    # print "type(author) ",type(driver_author)
                    driver_author.click()
                    time.sleep(3)
                    current_page = driver.page_source
                    author_soup  = BeautifulSoup(current_page)
                    # print author_soup.find(class_='scrollArea').find(class_='author').find_all('dd')
                    author_name = author_soup.find(class_='workAuthor').string.encode('utf-8')
                    messages = author_soup.find(class_='scrollArea').find(class_='author').find_all('dd')
                    #定义机构、邮件、联系方式
                    author_affiliation = ''
                    author_emails = ''
                    author_correspondences = ''
                    #遍历每一个小信息
                    for message in messages:
                        msgs = message.stripped_strings
                        #获取字符串
                        for msg in msgs:
                            #判断是否为空None
                            if msg:
                                msg_str = msg.encode('utf-8')
                                # print"msg_str:",msg_str
                                # print "message:",message.string.encode('utf-8')
                                if '@' in msg:
                                    # print "邮件"
                                    author_emails = author_emails + msg_str + ';'
                                elif 'Tel' in msg:
                                    # print '电话/传真'
                                    author_correspondences = author_correspondences + msg_str + ';'
                                else:
                                    # print '其它'
                                    author_affiliation = author_affiliation + msg_str + ';'
                            else:
                                pass
                    #获取到所有的个人信息，并写入数据库 作者表
                    #article_url，author_name，author_affiliation，author_emails，author_correspondences
                    author_id = str(int(time.time()))
                    # print "author message-------"
                    # print author_id
                    # print url
                    # print author_name
                    # print author_affiliation
                    # print author_emails
                    # print author_correspondences
                    #插入数据库
                    print "insert into mysql author 2"
                    insert_mysql_t_sciencedirect_journals_author(mysql_conn,author_id,url,author_name,author_affiliation, author_emails, author_correspondences)
                    print "insert into mysql author 2 over"
            except:
                print "not found elements 2"


        else:
            #方式一处理

            #获取标题
            try:
                publication_title = soup.find(class_='publication-title-link').string
                publication_title_str = publication_title.encode('utf-8')
                # print"publication_title:", publication_title_str

                #获取卷名
                volume_str = ''
                volumes = soup.find(class_='publication-volume').div.stripped_strings
                for volume in volumes:
                    volume_str = volume_str + volume.encode('utf-8')
                # print "volume_str:",volume_str

                #获取文章名
                article_title_str = ''
                article_titles = soup.find(class_='article-title').stripped_strings
                for article_title in article_titles:
                    article_title_str = article_title_str + article_title.encode('utf-8')
                # print 'article_title_str',article_title_str

                #获取作者组
                author_group_str = ''
                author_groups = soup.find_all(class_='author-name')
                for author_group in author_groups:
                    author_group_str = author_group_str + unicode(author_group.string).encode('utf-8') + ';'
                    # print  'unicode(author_group.string).encode utf-8:',type(unicode(author_group.string).encode('utf-8'))
                    # print 'author_group:',author_group.string
                # print "author_group_str:",author_group_str

                #获取链接
                doilink = soup.find(class_='doi').string
                doilink_str = doilink.encode('utf-8')
                # print "doilink_str:", doilink_str

                #获取abstract
                abstracts = soup.find(class_='Abstracts').stripped_strings
                count = 0
                for abstract in abstracts:
                    if count == 1:
                        abstract_str = abstract.encode('utf-8')
                    count = count + 1
                # print "abstract_str:", abstract_str

                #获取keyword
                keyword_str = ''
                keywords = soup.find(class_='keywords-list').stripped_strings
                for keyword in keywords:
                    keyword_str = keyword_str + keyword.encode('utf-8')
                    # print "keyword:", keyword
                # print "keyword_str",keyword_str

                #写入数据库 文章表
                article_id = str(int(time.time()))
                #publication_title_str  volume_str article_title_str  author_group_str  doilink_str abstract_str keyword_str
                print "+++article insert into mysql+++"
                insert_mysql_t_sciencedirect_journals_article(mysql_conn,article_id,url,publication_title_str,volume_str, article_title_str,  author_group_str,  doilink_str, abstract_str, keyword_str)
                print "++++insert over++++"
                #遍历作者
                # print type(driver.find_element_by_class_name('author-name'))
                authors = driver.find_elements_by_class_name('author-name')
                # driver.find_elements_by_class_name()
                for author in authors:
                    # print "type(author) ",type(author)
                    author.click()
                    time.sleep(3)
                    current_page = driver.page_source
                    author_soup  = BeautifulSoup(current_page)

                    #article_url，author_name，author_affiliation，author_emails，author_correspondences
                    try:
                        author_name = author_soup.find(class_='WorkspaceAuthor').find(class_='author-name').string.encode('utf-8')
                        # print "author_name:",author_name,type(author_name)
                        author_affiliation = author_soup.find(class_='author-affiliation').string.encode('utf-8')
                        # print "author_affiliation:",author_affiliation,type(author_affiliation)
                    except:
                        author_name = ""

                    try:
                        author_emails = author_soup.find(class_='author-emails').a['href'][7:].encode('utf-8')
                        # print "author_emails:",author_emails,type(author_emails)
                    except:
                        author_emails = ""

                    author_correspondences = ''
                    try:
                        if author_soup.find(class_='author-correspondences') != None:
                            for x in author_soup.find(class_='author-correspondences').stripped_strings:
                                author_correspondences = author_correspondences + x.encode('utf-8')
                        # print "author_correspondences:",author_correspondences,type(author_correspondences)
                    except:
                        author_correspondences = ''
                    #获取到所有的个人信息，并写入数据库 作者表
                    #article_url，author_name，author_affiliation，author_emails，author_correspondences
                    author_id = str(int(time.time()))
                    # print "author message-------"
                    # print author_id
                    # print url
                    # print author_name
                    # print author_affiliation
                    # print author_emails
                    # print author_correspondences
                    print "insert into mysql author 1"
                    insert_mysql_t_sciencedirect_journals_author(mysql_conn,author_id,url,author_name,author_affiliation, author_emails, author_correspondences)
                    print "insert into mysql author 1 over"
            except:
                print "not found element 1"
    except:
        print 'url--',url
        # print "article None"
    time.sleep(1)


