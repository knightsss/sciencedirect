#coding=utf-8
from selenium import webdriver

def get_webdriver():
    try:
        driver = webdriver.PhantomJS('E:\\phantomjs\\phantomjs-2.1.1-windows\\phantomjs-2.1.1-windows\\bin\\phantomjs')
    except:
        driver = None
    return driver