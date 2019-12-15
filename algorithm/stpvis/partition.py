import numpy as np
import math
from algorithm.stpvis import load
from algorithm.stpvis import ncp_abc
from algorithm.stpvis import ncp_ac
from algorithm import models
import json
from sklearn.cluster import KMeans

zhangliang, zhangliang_ce = load.load()
A, B, C, he = ncp_abc.ncp_abc(zhangliang, 3)
ce_A, ce_C, ce_he = ncp_ac.ncp_ac(zhangliang_ce, B, he)
# 节点数据结构
class Node(object):
    # 初始化一个节点
    def __init__(self,name = None,value=None):
        self.value = []  # 节点值
        self.name=[]
        self.children = []    # 子节点列表
    # 添加一个孩子节点
    def add_children(self,node):
        self.children.append(node)

root = Node('A',zhangliang)
# B = Node('B')
# root.add_children(B)
# root.add_children(Node('C'))
# D = Node('D')
# root.add_children(D)
# B.add_children(Node('E'))
# B.add_children(Node('F'))
# B.add_children(Node('G'))
# D.add_children(Node('H'))
# D.add_children(Node('I'))
# D.add_children(Node('J'))

def treeFind(node,str):
    """
    N叉树的前序遍历-查找
    """
    out=None
    if node:
        if node.value==str:                    # 如果输入结点不为空
            out=node
        else:              # 添加结点值到结果列表
            for child in node.children:     # 对每一棵子树做前序遍历
                out=treeFind(child, str)
    return out


# res=treeFind(root, 'J')
# print(res)


print(json.dumps(root, default=lambda obj: obj.__dict__, sort_keys=True, indent=4))

def partition(tensorIndex,clusterDimension,clusterNum):
    # 聚类
    if clusterDimension==0:
        kmeans = KMeans(n_clusters=clusterNum, random_state=0).fit(A)
    elif clusterDimension==1:
        kmeans = KMeans(n_clusters=clusterNum, random_state=0).fit(B)
    else:
        kmeans = KMeans(n_clusters=clusterNum, random_state=0).fit(C)
    clusters=[]
    tensor_subs=[]
    for i in range(clusterNum):
        cluster_one = np.where(kmeans.labels_ == i)[0]
        clusters.append(cluster_one)
        if clusterDimension==0:
            tensor_subs.append(zhangliang[cluster_one, :, :])
        elif clusterDimension==1:
            tensor_subs.append(zhangliang[:, cluster_one, :])
        else:
            tensor_subs.append(zhangliang[:, :, cluster_one])
    return [tensor_subs,clusters]


# print(partition("tensor1",0,2))

# 批量插入
# obj_list = []
# for i in range(size_A[0]):
#     obj = models.A(
#         a0=A[i][0],
#         a1=A[i][1],
#         a2=A[i][2]
#     )
#     obj_list.append(obj)
# models.A.objects.bulk_create(obj_list)

#查询
# a_list = models.A.objects.all()
# print(a_list)

