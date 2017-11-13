#!/bin/sh
cd /root/myscripts/py/png/
/usr/local/bin/python3.6 /root/myscripts/py/testHouseInfoBar.py
sleep 5m
echo " " | mailx  -s "houseInfo Bar`date +%F`" -a /root/myscripts/py/png/new.png -a /root/myscripts/py/png/old.png XXXXX@qq.com
echo " " | mailx  -s "houseInfo Bar`date +%F`" -a /root/myscripts/py/png/new.png -a /root/myscripts/py/png/old.png XXXXX@163.com
exit
