import networkx as nx
import matplotlib.pyplot as plt

'''
方法一：生成一个任意m个点，n条边的图G，图一定是connected的

'''
while True: #直到找到完全连通的图G为止
    G = nx.dense_gnm_random_graph(10,9) #点数m=10，边数n=9
    if nx.is_connected(G):
        break;
print('graph 1:')
print(G.edges())

'''
方法二：生成一个小世界网络G，G有m个点，每个点有k个直接连通的邻居点，p为重连接(rewire)一条边的概率
'''
G = nx.connected_watts_strogatz_graph(10, 3, 0.5, tries=100, seed=None) #m=10,k=3, p=0.5
print('graph 1:')
print(G.edges())

'''
画图：首先设定一种layout，并计算出所有点的位置，存入pos_dict
然后画图，画图的标记文字，最后显示出来
'''
pos_dict = nx.spring_layout(G) #设定图的layout，可以有多种可选： circular_layout；random_layout；shell_layout；spectral_layout
nx.draw(G,pos=pos_dict) #画图
labels=nx.draw_networkx_labels(G,pos=pos_dict) #画点的标记
plt.show() #显示