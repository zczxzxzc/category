import matplotlib.pyplot as plt
import numpy as np

x_values = np.linspace(0,20,100)   # 创建一个列表
plt.plot(x_values,np.sin(x_values))       # 对于每个点的sin值绘图
plt.show()                  # 显示

y_values=[x**2 for x in x_values]
#y轴的数字是x轴数字的平方
plt.plot(x_values,y_values,c='green')
#用plot函数绘制折线图，线条颜色设置为绿色
plt.title('Squares',fontsize=24)
#设置图表标题和标题字号
plt.tick_params(axis='both',which='major',labelsize=14)
#设置刻度的字号
plt.xlabel('Numbers',fontsize=14)
#设置x轴标签及其字号
plt.ylabel('Squares',fontsize=14)
#设置y轴标签及其字号
plt.show()
#显示图表

