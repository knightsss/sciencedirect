#coding=utf-8
__author__ = 'shifeixiang'
import MySQLdb
import time

def mysql_connect_localhost():
    try:
        mysql_conn = MySQLdb.connect("localhost","root","123456","db_sciencedirect")
    except:
        print "connect mysql error"
        return None
    return mysql_conn


#写入mysql mysql数据库需要将unnicode转换成str
def insert_mysql_t_sciencedirect_journals_article(mysql_conn,*args):
    # print args
    if len(args) == 9:
        article_id = args[0]
        article_url = args[1]
        publication_title = args[2]
        volume = args[3]
        article_title = args[4]
        author_group = args[5]
        doilink = args[6]
        abstract_author = args[7]
        keywords = args[8]

        abstract_author = abstract_author.replace("'","''")
        # print article_id, article_url, publication_title
        # print "type abstract_author:::::::",type(abstract_author)
        # print "abstract_author:::::::",abstract_author
    # time.sleep(3)
    try:
        mysql_cursor = mysql_conn.cursor()
        sql = '''insert into t_sciencedirect_journals_article (article_id, article_url, publication_title, volume, article_title,
                  author_group, doilink, abstract_author, keywords) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')''' \
                    %(article_id, article_url, publication_title, volume, article_title,author_group, doilink, abstract_author, keywords)
        mysql_cursor.execute(sql)
        mysql_conn.commit()
    except:
        print "insert article into faild!"
    # time.sleep(3)
    return 0


def insert_mysql_t_sciencedirect_journals_author(mysql_conn,*args):
    # print args
    if len(args) == 6:
        author_id = args[0]
        article_url = args[1]
        author_name = args[2]
        author_affiliation = args[3]
        author_emails = args[4]
        author_correspondences = args[5]
        author_affiliation = author_affiliation.replace("'","''")
    try:
        mysql_cursor = mysql_conn.cursor()
        sql = '''insert into t_sciencedirect_journals_author (author_id, article_url, author_name, author_affiliation, author_emails, author_correspondences)
                  values('%s', '%s', '%s', '%s', '%s', '%s')''' \
                    %(author_id, article_url, author_name, author_affiliation, author_emails,author_correspondences)
        mysql_cursor.execute(sql)
        mysql_conn.commit()
    except:
        print "insert author into faild!"
    return 0


def insert_mysql_t_sciencedirect_journals_url(mysql_conn,tmp):
    mysql_cursor = mysql_conn.cursor()
    sql = "insert into t_sciencedirect_journals_url(url_id,main_url,volume_url,article_url) values(%s, %s, %s, %s)"
    # tmp结构 tmp = (('00', '0000'), ('10', '111'))
    mysql_cursor.executemany(sql, tmp)
    mysql_conn.commit()
    return 0

def get_tuple(main_url,volume_url,article_url_list):
    tmp_list = []
    for article_url in article_url_list:
        url_id = article_url[-16:]
        tmp_tup = (url_id,main_url,volume_url,article_url)
        tmp_list.append(tmp_tup)
    return tuple(tmp_list)


