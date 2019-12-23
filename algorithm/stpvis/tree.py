import numpy as np
from algorithm.stpvis import load
from algorithm.stpvis import ncpEnsembles

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
    AAll, BAll, CAll, heAll,ce_AAll, ce_CAll, ce_heAll=ncpEnsembles.ncpEnsembles(zhangliang,zhangliang_ce)
    sum,marginalA,marginalB,marginalC=tensorStatistic(zhangliang)
    root=Node('Root',zhangliang,zhangliang_ce,sum,marginalA,marginalB,marginalC,AAll.T, BAll.T, CAll.T, heAll,ce_AAll.T, ce_CAll.T, ce_heAll)
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
def partition(tensorName,clusterDimension,clusterNum):
    nodeSelected=treeFind(root, tensorName)
    # 聚类
    if clusterDimension==0:
        kmeans = KMeans(n_clusters=clusterNum, random_state=0).fit(nodeSelected.A.T)
    elif clusterDimension==1:
        kmeans = KMeans(n_clusters=clusterNum, random_state=0).fit(nodeSelected.B.T)
    else:
        kmeans = KMeans(n_clusters=clusterNum, random_state=0).fit(nodeSelected.C.T)
    for i in range(clusterNum):
        cluster_one = np.where(kmeans.labels_ == i)[0]
        tensorTemp=None
        ce_tensorTemp=None
        dimensionStrTemp=["-A","-B","-C"]
        if clusterDimension==0:
            tensorTemp=nodeSelected.tensor[cluster_one, :, :]
            ce_tensorTemp=nodeSelected.ce_tensor[cluster_one, :, :]
        elif clusterDimension==1:
            tensorTemp=nodeSelected.tensor[:, cluster_one, :]
            ce_tensorTemp=nodeSelected.ce_tensor[:, cluster_one, :]
        else:
            tensorTemp=nodeSelected.tensor[:, :, cluster_one]
            ce_tensorTemp=nodeSelected.ce_tensor[:, :, cluster_one]
        AAll, BAll, CAll, heAll,ce_AAll, ce_CAll, ce_heAll=ncpEnsembles.ncpEnsembles(tensorTemp,ce_tensorTemp)
        sum,marginalA,marginalB,marginalC=tensorStatistic(tensorTemp)
        nodeTemp=Node(tensorName+dimensionStrTemp[clusterDimension]+str(i),tensorTemp,ce_tensorTemp,sum,marginalA,marginalB,marginalC,AAll.T, BAll.T, CAll.T, heAll,ce_AAll.T, ce_CAll.T, ce_heAll)
        nodeSelected.add_children(nodeTemp)
    return root
