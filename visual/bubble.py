import numpy as np  
import seaborn as sns
import matplotlib.pyplot as plt

def DrawBubble():#气泡图
    sns.set(style = "whitegrid")#设置样式
    x = np.random.randint(1,100,50)#X轴数据
    y = np.random.rand(50)#Y轴数据
    y = np.abs(y)
    cm = plt.cm.get_cmap('RdYlBu')
    fig,ax = plt.subplots(figsize = (12,10))
    bubble = ax.scatter(x, y , s = x*10, c = y, cmap = cm, linewidth = 0.5, alpha = 0.5)
    ax.grid()
    fig.colorbar(bubble)
    ax.set_xlabel('people of cities', fontsize = 15)#X轴标签
    ax.set_ylabel('price of something', fontsize = 15)#Y轴标签
    plt.show()
if __name__=='__main__':
    DrawBubble()#气泡图