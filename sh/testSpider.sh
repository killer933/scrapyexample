#!/bin/sh
cd /root/testSpider/tutorial
scrapy crawl MySpider -o house.csv
echo " " | mailx  -s "house information `date +%F`" -a /root/testSpider/tutorial/house.csv XXXXXXX@163.com
exit
