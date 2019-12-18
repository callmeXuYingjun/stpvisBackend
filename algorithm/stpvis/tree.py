import numpy as np
import math
from algorithm.stpvis import load
from algorithm.stpvis import ncp_abc
from algorithm.stpvis import ncp_ac
from algorithm import models
import json
from sklearn.cluster import KMeans

def tensorStatistic(tensor):
    [A_lie, B_lie, C_lie] = tensor.shape
    sum=np.sum(np.sum(np.sum(tensor)))
    marginalA=[]
    for i in range(A_lie):
        marginalA.append(np.sum(np.sum(tensor[i,:,:])))
    marginalB=[]
    for i in range(B_lie):
        marginalB.append(np.sum(np.sum(tensor[:,i,:])))
    marginalC=[]
    for i in range(C_lie):
        marginalC.append(np.sum(np.sum(tensor[:,:,i])))

    return [sum,marginalA,marginalB,marginalC]
# 节点数据结构
#name,value(张量原始不需要了),三个维度的边缘分布(marginalA,marginalB,marginalC)，分解得到三个维度的模式(A,B,C,ce_A,ce_B,ce_C),每个节点的数据量(sum)
class Node(object):
    # 初始化一个节点
    def __init__(self,name = None,tensor = None,ce_tensor = None,sum=None,marginalA=None,marginalB=None,marginalC=None,A=None,B=None,C=None,he=None,ce_A=None,ce_C=None,ce_he=None):
        self.name=name
        self.tensor = tensor  # 节点值
        self.ce_tensor = ce_tensor  # 节点值
        self.sum = sum  # 节点值
        self.marginalA = marginalA  # 节点值
        self.marginalB = marginalB  # 节点值
        self.marginalC = marginalC  # 节点值
        self.A = A  # 节点值
        self.B = B  # 节点值
        self.C = C  # 节点值
        self.he = he  # 节点值
        self.ce_A = ce_A  # 节点值
        self.ce_C = ce_C  # 节点值
        self.ce_he = he  # 节点值
        self.children = []    # 子节点列表
    # 添加一个孩子节点
    def add_children(self,node):
        self.children.append(node)
root=None
def treeInit():
    global root
    zhangliang, zhangliang_ce = load.load()
    A, B, C, he = ncp_abc.ncp_abc(zhangliang, 3)
    ce_A, ce_C, ce_he = ncp_ac.ncp_ac(zhangliang_ce, B, he)
    sum,marginalA,marginalB,marginalC=tensorStatistic(zhangliang)
    root=Node('Root',zhangliang,zhangliang_ce,sum,marginalA,marginalB,marginalC,A, B, C, he,ce_A, ce_C, ce_he)
treeInit()
def treeFind(node,str,out=None):
    """
    N叉树的前序遍历-查找
    """
    if node:
        if node.name==str:                    # 如果输入结点不为空
            out=node
        else:              # 添加结点值到结果列表
            for child in node.children:     # 对每一棵子树做前序遍历
                out=treeFind(child, str,out)
    return out
def treeTraversal(node):
    print("1111111111111111111111")
    print(dir(node))
    if node:
        for key in node.keys():
            if type(node[key])==np.ndarray:                    # 如果输入结点不为空
                node[key]=node[key].tolist()
        if  len(node.children):            # 添加结点值到结果列表
            for child in node.children:     # 对每一棵子树做前序遍历
                treeTraversal(child)
    return node
def partition(tensorName,clusterDimension,clusterNum):
    nodeSelected=treeFind(root, tensorName)
    # 聚类
    if clusterDimension==0:
        kmeans = KMeans(n_clusters=clusterNum, random_state=0).fit(nodeSelected.A)
    elif clusterDimension==1:
        kmeans = KMeans(n_clusters=clusterNum, random_state=0).fit(nodeSelected.B)
    else:
        kmeans = KMeans(n_clusters=clusterNum, random_state=0).fit(nodeSelected.C)
    for i in range(clusterNum):
        cluster_one = np.where(kmeans.labels_ == i)[0]
        tensorTemp=None
        ce_tensorTemp=None
        dimensionStrTemp=["-A","-B","-C"]
        if clusterDimension==0:
            tensorTemp=nodeSelected.tensor[cluster_one, :, :]
            ce_tensorTemp=nodeSelected.ce_tensor[cluster_one, :, :]
            # nodeTemp = Node(tensorName+"-A"+str(i),tensorTemp.tolist())
        elif clusterDimension==1:
            tensorTemp=nodeSelected.tensor[:, cluster_one, :]
            ce_tensorTemp=nodeSelected.ce_tensor[:, cluster_one, :]
            # nodeTemp = Node(tensorName+"-B"+str(i),tensorTemp.tolist())

        else:
            tensorTemp=nodeSelected.tensor[:, :, cluster_one]
            ce_tensorTemp=nodeSelected.ce_tensor[:, :, cluster_one]
            # nodeTemp = Node(tensorName+"-C"+str(i),tensorTemp.tolist())

        A, B, C, he = ncp_abc.ncp_abc(tensorTemp, 3)
        ce_A, ce_C, ce_he = ncp_ac.ncp_ac(ce_tensorTemp, B, he)
        sum,marginalA,marginalB,marginalC=tensorStatistic(tensorTemp)
        nodeTemp=Node(tensorName+dimensionStrTemp[clusterDimension]+str(i),tensorTemp,ce_tensorTemp,sum,marginalA,marginalB,marginalC,A, B, C, he,ce_A, ce_C, ce_he)
        # nodeTemp = Node(tensorName+dimensionStrTemp[clusterDimension]+str(i),tensorTemp.tolist())
        nodeSelected.add_children(nodeTemp)
    # return [tensor_subs,clusters]
    return root







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

