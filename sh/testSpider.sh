#!/bin/sh
cd /root/testSpider/tutorial
scrapy crawl MySpider -o house.csv
echo " " | mailx  -s "house information `date +%F`" -a /root/testSpider/tutorial/house.csv sunzhi1019@163.com
exit
