#coding=utf-8
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pymysql
from datetime import datetime
import matplotlib.dates as mdates
import sys
class Mysqloperation(object):

    def __init__(self):
        self.conn = pymysql.connect(host='23.105.217.5', port=3306, user='root', passwd='Uo07s123123', db='houseinfo',charset='utf8')
        self.cursor = self.conn.cursor()
        self.user_list1 = []
        self.user_list2 = []
    def __del__(self):
        self.cursor.close()
        self.conn.close()
    def executesql(self,sql):
        self.cursor.execute(sql)
        ret1 = self.cursor.fetchall()
    #    ret1 = self.cursor.fetchone()
        return ret1
    def get_data(self,rows):
        for row in rows:
            if(str(row[0]) == "新房"):
                self.user_list1.append([str(row[0]),str(row[1]),int(row[2]),str(row[5])])
            else:
                self.user_list2.append([str(row[0]),str(row[1]),int(row[2]),str(row[5])])
        return self.user_list1,self.user_list2


class Draw(object):
    def drawplt(self,rows,type):
        if(type==False):
            typename = '新房一周行情'
            filename = 'new.png'
        else:
            typename = '二手房一周行情'
            filename = 'old.png'
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        mpl.rcParams['xtick.labelsize'] = 12
        mpl.rcParams['ytick.labelsize'] = 12
        mpl.rcParams['xtick.direction'] = 'in'
        mpl.rcParams['ytick.direction'] = 'in'
    #    np.random.seed(42)
        # x轴的采样点
        x = []
        y = []
        str = ['高新区', '武侯区', '成华区', '青羊区', '金牛区', '锦江区']
        col = ['green','blue','black','red','yellow','magenta']
        mar = ['o','D','*','+','s','p']
      #  x = np.linspace(0, 5, 100)
        # 通过下面曲线加上噪声生成数据，所以拟合模型就用y了……
     #   y = 2 * np.sin(x) + 0.3 * x ** 2
     #   y_data = y + np.random.normal(scale=0.3, size=100)
        # 两个图画一起
        plt.figure(figsize=(16,9),dpi=300)
        # 通过'k'指定线的颜色，lw指定线的宽度
        # 第三个参数除了颜色也可以指定线形，比如'r--'表示红色虚线
        # 更多属性可以参考官网：http://matplotlib.org/api/pyplot_api.html
        plt.grid(linestyle="--")
        for i in range(0, 6):
            for row in rows:
                if(str[i]==row[1]):
                     x.append(row[3])
                     y.append(row[2])
            xs = [datetime.strptime(d, '%Y-%m-%d').date() for d in x]
            plt.plot(xs, y, 'k', color=col[i], marker=mar[i], linewidth=2.5, linestyle="-", label=str[i])
            x.clear()
            y.clear()

#        plt.plot(x, y, 'k', color="blue", marker="o",linewidth=2.5, linestyle="-", label="武侯区")
        # scatter可以更容易地生成散点图
 #       plt.plot(x, y+2, 'k', color="red", marker="D", linewidth=2.5, linestyle="-", label="高新区")
        plt.gcf().autofmt_xdate()
        plt.title(typename, fontsize=20)
        plt.xlabel('时间', fontsize=12)
        plt.ylabel('价格 (元)',fontsize=12)
        plt.legend(loc='upper left',fontsize=16)

        # 将当前figure的图保存到文件result.png
        plt.savefig(filename, bbox_inches='tight')
        # 一定要加上这句才能让画好的图显示在屏幕上
        plt.show()

    # 获取第一行数据
   # row_1 = cursor.fetchone()

    # 获取前n行数据
    # row_2 = cursor.fetchmany(3)
    # 获取所有数据
    # row_3 = cursor.fetchall()


def main():
    print("Starting!")
    str1 =['新房','二手房']
    sqltest = Mysqloperation()
    draw = Draw()
#    draw.drawplt()
    sql = "SELECT * FROM spiderhouse where date > DATE_SUB(CURDATE(), INTERVAL 7 DAY)"
    rows = sqltest.executesql(sql)
    [list1,list2] = sqltest.get_data(rows)
    draw.drawplt(list1,False)
    print("Ending!")
if __name__ =='__main__':
    main()