#coding=utf-8
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
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
        i = 0
        for row in rows:
            i = i+1
            if(str(row[0]) == "新房"):
                self.user_list1.append([str(row[0]),str(row[1]),int(row[2]),str(row[5]),int(row[6])])
            else:
                self.user_list2.append([str(row[0]),str(row[1]),int(row[2]),str(row[5]),int(row[6])])
        count =i/12
        return self.user_list1,self.user_list2,count


class Draw(object):
    def drawplt(self,rows,type,count):
        if(type==False):
            typename =  '新房一周行情'
            filename = '/root/myscripts/py/png/' + datetime.now().strftime('%Y-%m-%d') + '-new.png'
            filenametmp = '/root/myscripts/py/png/' + 'new.png'
        else:
            typename = '二手房一周行情'
            filename = '/root/myscripts/py/png/' + datetime.now().strftime('%Y-%m-%d') + '-old.png'
            filenametmp = '/root/myscripts/py/png/' + 'old.png'
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        mpl.rcParams['xtick.labelsize'] = 12
        mpl.rcParams['ytick.labelsize'] = 12
        mpl.rcParams['xtick.direction'] = 'in'
        mpl.rcParams['ytick.direction'] = 'in'
        n_groups = count
        index = np.arange(n_groups)
        bar_width = 0.25
        opacity = 0.8

        #    np.random.seed(42)
        # x轴的采样点
        x = []
        y = []
        z = []
        flag =True
        temp =[]
        tempz = []
        kk = (0.84472049689441, 0.972477064220183, 1.0, 0.9655172413793104, 0.970970970970971,0.32)
        xs =[]
        str = ['高新区', '武侯区', '成华区', '青羊区', '金牛区', '锦江区']
        col = ['green','blue','black','red','yellow','magenta']
        mar = ['o','D','*','+','s','p']
        switcher = {
            1: "星期一",
            2: "星期二",
            3: "星期三",
            4: "星期四",
            5: "星期五",
            6: "星期六",
            7: "星期天",
        }
      #  x = np.linspace(0, 5, 100)
        # 通过下面曲线加上噪声生成数据，所以拟合模型就用y了……
     #   y = 2 * np.sin(x) + 0.3 * x ** 2
     #   y_data = y + np.random.normal(scale=0.3, size=100)
        # 两个图画一起
        plt.figure(figsize=(16,9),dpi=300)
        # 通过'k'指定线的颜色，lw指定线的宽度
        # 第三个参数除了颜色也可以指定线形，比如'r--'表示红色虚线
        # 更多属性可以参考官网：http://matplotlib.org/api/pyplot_api.html
        for i in range(0, 6):
            for row in rows:
                if(str[i]==row[1]):
                     x.append(row[3])
                     y.append(row[2])
                     z.append(switcher.get(row[4]))
            if(flag):
                tempz = z.copy()
                temp = x.copy()
                flag = False
            ys = tuple(y)
            xs = [datetime.strptime(d, '%Y-%m-%d').date() for d in x]
            plt.bar(index+i*bar_width/2, ys, bar_width / 2, alpha=opacity, color=col[i], label=str[i])
 #           plt.plot(xs, y, 'k', color=col[i], marker=mar[i], linewidth=2.5, linestyle="-", label=str[i])
            x.clear()
            y.clear()

        for i, val in enumerate(tempz):
            temp[i] = temp[i] +'\n' + val



        #        plt.plot(x, y, 'k', color="blue", marker="o",linewidth=2.5, linestyle="-", label="武侯区")
        # scatter可以更容易地生成散点图
 #       plt.plot(x, y+2, 'k', color="red", marker="D", linewidth=2.5, linestyle="-", label="高新区")
   #     plt.gcf().autofmt_xdate()
        plt.title(typename, fontsize=20)
        plt.xticks(index - 0.2 + 2 * bar_width, temp,fontsize = 12)
        plt.ylabel('套数 (套)',fontsize=12)
        plt.legend(loc='upper right',fontsize=16)

        # 将当前figure的图保存到文件result.png
        plt.savefig(filename, bbox_inches='tight')
        plt.savefig(filenametmp, bbox_inches='tight')
        # 一定要加上这句才能让画好的图显示在屏幕上
 #       plt.show()

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
    sql = "SELECT * FROM spiderhouse where date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)"
    rows = sqltest.executesql(sql)
    [list1,list2,count] = sqltest.get_data(rows)
    draw.drawplt(list1,False,count)
    draw.drawplt(list2,True,count)
    print("Ending!")
if __name__ =='__main__':
    main()
