# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


#class TutorialPipeline(object):
#    def process_item(self, item, spider):
#        return item
from twisted.enterprise import adbapi
from twisted.internet import defer
import MySQLdb
import MySQLdb.cursors
import codecs
import json
import time
import threading
from logging import log

class SQLStorePipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb', host='127.0.0.1',db='houseinfo',
                user='root', passwd='Uo07s123123', cursorclass=MySQLdb.cursors.DictCursor,
                charset='utf8', use_unicode=True)
        global mutex
        mutex = threading.Lock()
  
    def process_item(self, item, spider):
        # run db query in thread pool
 #       print item["house_type"]
       
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        time.sleep(3)
        print "-------------------------------over"
        return item
  
    def _conditional_insert(self, tx, item):
        # create record if doesn't exist.
        # all this block run on it's own thread
        sql="INSERT INTO spiderhouse(house_type,house_area,num,full_square_meter,square_meter,date,weekday) VALUES(%s,%s,%s,%s,%s,%s,%s)"
   #     params=("abc","dse",11,123.1,321.1,"2017-10-19",3)
#        params=(item["house_type"][0],item["house_area"][0],item["num"][0],item["full_square_meter"][0],item["square_meter"][0],item["date"][0],item["weekday"][0])
        params=(item["house_type"],item["house_area"],item["num"],item["full_square_meter"],item["square_meter"],item["date"],item["weekday"])
 #       sql1="INSERT INTO testname(name,password) VALUES(%s,%s)"
  #      params1=("123","321")
        tx.execute(sql,params)
 #       print tx.fetchone()
    def close_spider(self, spider):
        self.dbpool.close()
        print "--------------------closing!!!!------------------------------"
    def handle_error(self,e):
        print '--------------database operation exception!!-----------------'
        print '-------------------------------------------------------------'
