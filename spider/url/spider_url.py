#coding=utf-8
__author__ = 'shifeixiang'
import time
from bs4 import BeautifulSoup
from db.db_mysql import insert_mysql_t_sciencedirect_journals_url,get_tuple


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#获取卷
def get_volume_url(driver,main_url):
    #构造aip链接
    volume_url_list = []
    print 'start get volume'
    try:
        volume_url = main_url[:-8] + 'aip/' + main_url[-8:]
        driver.get(volume_url)
        try:
            element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID , "ccs-journalsLink")))
        except:
            print "request url timeout"
            time.sleep(10)
            return 0
        volume_soup = BeautifulSoup(driver.page_source)

        elements = volume_soup.ol.find_all('li')

        #组标志，默认为非组
        flag_group = 0
        if volume_soup.find(class_='txtBold') == None:
            flag_group = 0
        else:
            flag_group = 1
        print flag_group
        # return 0

        #遍历为展开的元素组
        if flag_group:
            for element in elements:
                try:
                    sub_url = element.a['href'].encode('utf-8')
                    if 'open-access' not in sub_url:
                        volume_url = 'http://www.sciencedirect.com' + sub_url
                        #访问每一个卷的展开的链接
                        driver.get(volume_url)
                        try:
                            element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID , "ccs-journalsLink")))
                        except:
                            print "request url timeout"
                            time.sleep(10)
                            return 0
                        time.sleep(2)
                        volume_soup = BeautifulSoup(driver.page_source)
                        sub_elements = volume_soup.find_all(class_='currentVolumes')
                        #遍历每一组的所有元素
                        for sub_element in sub_elements:
                            try:
                                #获取所有的volume
                                # print sub_element.a['href'].encode('utf-8')
                                volume_url_list.append('http://www.sciencedirect.com' + sub_element.a['href'].encode('utf-8'))
                            except:
                                #获取当前页的volume
                                print 'no label sub element'
                                print sub_url
                                volume_url_list.append('http://www.sciencedirect.com' + sub_url)
                except:
                    print 'no a label'
        else:
            count = 0
            for element in elements:
                if count == 0:
                    print element
                    try:
                        sub_urls = element.find_all('a')
                        print sub_urls
                        for s_u in sub_urls:
                            try:
                                sub_url = s_u['href'].encode('utf-8')
                                volume_url = 'http://www.sciencedirect.com' + sub_url
                                print "first volume_url:",volume_url
                                volume_url_list.append(volume_url)
                            except:
                                print "no href"
                    except:
                        print "not found a from "
                count = count + 1
    except:
        print "get volume is null"
    print 'get volume finish'
    return  volume_url_list

    # for element in elements:
    #     print element['href']

#根据volume url获取论文的url
def get_article_url(driver, mysql_conn, main_url, volume_url_list):
    print 'start get article url'
    article_url_list_all = []
    try:
        for volume_url in volume_url_list:
            article_url_list = []
            driver.get(volume_url)
            try:
                element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID , "ccs-journalsLink")))
            except:
                print "request url timeout"
                time.sleep(30)
                return 0
            article_soup = BeautifulSoup(driver.page_source)
            elements = article_soup.find_all(class_='detail')
            for element in elements:
                try:
                    article_url = element.a['href'].encode('utf-8')
                    article_url_list.append(article_url)
                    article_url_list_all.append(article_url)
                except:
                    print "no label"
            #插入数据库
            print volume_url,"insert into mysql"
            tmp = get_tuple(main_url,volume_url,article_url_list)
            insert_mysql_t_sciencedirect_journals_url(mysql_conn,tmp)
            print volume_url,"insert into mysql finish"
    except:
        print "get article is null"
    print 'get article finish'
    return article_url_list_all






































#获取卷
def get_volume_url_old(driver,main_url):
    #构造aip链接
    volume_url = main_url[:-8] + 'aip/' + main_url[-8:]

    driver.get(volume_url)
    volume_soup = BeautifulSoup(driver.page_source)

    elements = volume_soup.ol.find_all('li')
    volume_url_list = []
    #遍历为展开的元素组
    for element in elements:
        try:
            sub_url = element.a['href']
            if 'open-access' not in sub_url:
                volume_url = 'http://www.sciencedirect.com' + sub_url
                #访问每一个卷的展开的链接
                driver.get(volume_url)
                time.sleep(2)
                volume_soup = BeautifulSoup(driver.page_source)
                sub_elements = volume_soup.find_all(class_='currentVolumes')
                #遍历每一组的所有元素
                for sub_element in sub_elements:
                    try:
                        #获取所有的volume
                        print sub_element.a['href']
                        volume_url_list.append('http://www.sciencedirect.com' + sub_element.a['href'])
                    except:
                        #获取当前页的volume
                        print 'no label sub element'
                        print sub_url
                        volume_url_list.append('http://www.sciencedirect.com' + sub_url)
        except:
            print 'no a label'
    return  volume_url_list

#根据volume url获取论文的url
def get_article_url_old(driver, main_url, volume_url_list):
    article_url_list = []
    for volume_url in volume_url_list:
        driver.get(volume_url)
        article_soup = BeautifulSoup(driver.page_source)

        elements = article_soup.find_all(class_='detail')
        for element in elements:
            print '------'
            try:
                article_url = element.a['href']
                # print element.a['href']
                article_url_list.append(element.a['href'])
                print main_url,volume_url,article_url
            except:
                print "no label"
    return article_url_list

