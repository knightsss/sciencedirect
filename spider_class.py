#coding=utf-8
__author__ = 'shifeixiang'

import redis
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import MySQLdb

def get_webdriver():
    #phantomjs
    driver = webdriver.PhantomJS('E:\\phantomjs\\phantomjs-2.1.1-windows\\phantomjs-2.1.1-windows\\bin\\phantomjs')

    #谷歌浏览器采集
    # chrome_driver = os.path.abspath(r"F:\auto_windows\atom-windows\Atom\new_chrome\chromedriver.exe")   #谷歌浏览器位置
    # os.environ["webdriver.chrome.driver"] = chrome_driver            #设置环境变量
    # driver = webdriver.Chrome(chrome_driver)             #webdriver获取
    return driver


import time


def get_classes_click(driver):
    #2.3.4.5
    element = driver.find_element_by_xpath("//ul[@class='browseSubjectTreeList']//li[2]//span//div")
    print element.text
    print element.click()
    time.sleep(3)

    element = driver.find_element_by_xpath("//ul[@class='browseSubjectTreeList']//li[2]//ul//li[1]//span/div")
    print element.text
    print element.click()
    time.sleep(3)

    element = driver.find_element_by_xpath("//ul[@class='browseSubjectTreeList']//li[2]//ul//li[1]//ul//li[1]//span/input")
    print element.text
    print element.click()
    time.sleep(3)

    driver.find_element_by_id('submitButton').click()
    time.sleep(3)

#获取主页里所有链接
def get_main_url(driver,url):

    driver.get(url)
    time.sleep(1)
    pull_times = 3
    for i in range(pull_times):
        print "pull ",str(i)
        js="var q=document.body.scrollTop=" + str((i+1)*1000)
        driver.execute_script(js)
        time.sleep(2)
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


def get_all_object(subject_name_list, son_subject_name_list, grandson_subject_name_list):

    url = 'http://www.sciencedirect.com/science/journals'
    driver = get_webdriver()

    driver.get(url)

    # print driver.page_source
    # time.sleep(5)
    count = 0
    element = driver.find_element_by_xpath("//ul[@class='browseSubjectTreeList']//li[1]")
    # for element in elements:
    #     if count !=0 and count != 5:
    #         print type(element.text)
    #         print element.text.encode('utf-8').strip('\n')
    #     count = count + 1
    print element.text
    object_name_list = []
    time.sleep(1)
    flag = 1
    while flag:
        try:
            #获取兄弟节点
            element_brother = element.find_element_by_xpath('./following-sibling::*')
            subject_name = element_brother.text.encode('utf-8')
            print "element_brother.text: ",subject_name
            element = element_brother
            #如果为空
            if element_brother.text.encode('utf-8') == '':
                flag = 0
                break

            # time.sleep(1)
            son_flag = 1
            son_element = element
            son_element.find_element_by_xpath('./span/div').click()
            son_element_brother = son_element.find_element_by_xpath('./ul/li[1]')
            while son_flag:
                try:
                    son_subject_name = son_element_brother.text.encode('utf-8')
                    print "----son_subject_name",son_subject_name
                    if son_subject_name == '':
                        son_flag = 0
                        break
                    son_element = son_element_brother

                    # time.sleep(1)

                    grandson_flag = 1
                    grandson_element = son_element
                    grandson_element.find_element_by_xpath('./span/div').click()
                    grandson_element_brother = grandson_element.find_element_by_xpath('./ul/li[1]')
                    while grandson_flag:
                        try:
                            grandson_subject_name = grandson_element_brother.text.encode('utf-8')
                            print "--------grandson_subject_name",grandson_subject_name
                            count = count + 1
                            if grandson_subject_name == '':
                                grandson_flag = 0
                                break

                            if (subject_name in subject_name_list)  and (son_subject_name in son_subject_name_list) and (grandson_subject_name in grandson_subject_name_list):
                                pass
                            else:
                                #开始模拟点击
                                print '--------start click'
                                grandson_element_brother.find_element_by_xpath('./span/input').click()
                                time.sleep(1)
                                print '--------start submit'
                                driver.find_element_by_id('submitButton').click()
                                time.sleep(1)
                                object_url = driver.current_url
                                driver.quit()
                                return subject_name,son_subject_name,grandson_subject_name,object_url


                            # class_list.appen(grandson_subject_name)
                            # #回退
                            # print '--------start back'
                            # driver.back()
                            # #点击取消
                            # time.sleep(3)
                            # print grandson_element_brother.text.encode('utf-8')
                            # print '--------start click'
                            # grandson_element_brother.find_element_by_xpath('./span/input').click()

                            grandson_element = grandson_element_brother
                            grandson_element_brother = grandson_element.find_element_by_xpath('./following-sibling::*')
                            # time.sleep(2)
                        except:
                            print "--------grandson_object finish"
                            break
                    son_element_brother = son_element.find_element_by_xpath('./following-sibling::*')
                except:
                    print "----son_object finish"
                    break
        except:
            flag = 0
            break
            print 'over'
    print "count",count
    driver.close()




def mysql_connect_localhost():
    try:
        mysql_conn = MySQLdb.connect("localhost","root","123456","db_sciencedirect")
    except:
        print "connect mysql error"
        return None
    return mysql_conn


def insert_mysql_t_sciencedirect_journals_class(mysql_conn,tmp):
    mysql_cursor = mysql_conn.cursor()
    sql = "insert into t_sciencedirect_journals_class2(class_id,subject_name,son_subject_name,grandson_subject_name, main_url) values(%s, %s, %s, %s, %s)"
    # tmp结构 tmp = (('00', '0000'), ('10', '111'))
    mysql_cursor.executemany(sql, tmp)
    mysql_conn.commit()
    return 0

def get_tuple(subject_name,son_subject_name,grandson_subject_name, main_url_list):
    tmp_list = []
    count = 0
    ptime = str(int(time.time()))
    for main_url in main_url_list:
        class_id = ptime + str(count).zfill(3)
        tmp_tup = (class_id,subject_name,son_subject_name,grandson_subject_name,main_url)
        tmp_list.append(tmp_tup)
        count = count + 1
    return tuple(tmp_list)

if __name__ == '__main__':

    # url = 'http://www.sciencedirect.com/science/journals'
    subject_name_list = []
    son_subject_name_list = []
    grandson_subject_name_list = []


    mysql_conn = mysql_connect_localhost
    main_driver = get_webdriver()
    while 1:
        try:
            subject_name,son_subject_name,grandson_subject_name,object_url = get_all_object(subject_name_list, son_subject_name_list, grandson_subject_name_list)
        except:
            break
        print "start get main_class"
        current_url_list = get_main_url(main_driver,object_url)
        #入mysql
        mysql_conn = mysql_connect_localhost()
        print "insert mysql"
        tmp = get_tuple(subject_name,son_subject_name,grandson_subject_name,current_url_list)
        insert_mysql_t_sciencedirect_journals_class(mysql_conn,tmp)
        print "insert finish"
        mysql_conn.close()

        subject_name_list.append(subject_name)
        son_subject_name_list.append(son_subject_name)
        grandson_subject_name_list.append(grandson_subject_name)

        if subject_name == 'Social Sciences and Humanities' and son_subject_name == 'Social Sciences' and grandson_subject_name == 'Transportation':
            break
        print grandson_subject_name_list

    main_driver.quit()




    # driver = get_webdriver()
    # url = 'http://www.sciencedirect.com/science/journals/sub/filtraseparation'
    # current_url_list = get_main_url(driver,url)
    # driver.close()
    # print current_url_list


    # print driver.page_source

    # elements = driver.find_element_by_class_name('browseSubjectTreeList').find_elements_by_class_name('category')
    # print type(elements)
    # print len(elements)
    # count = 0
    # for element in elements:
    #     element.click()
    #     print count
    #     count =  count + 1
    #     if count > 1:
    #         break



