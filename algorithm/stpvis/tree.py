import numpy as np
from algorithm.stpvis import load
from algorithm.stpvis import ncpEnsembles
import math
import sklearn.preprocessing as SKP
from sklearn.manifold import MDS


import json
from sklearn.cluster import KMeans

timeCoarse2Fine=None
timeCoarse2FineName=None
##需要更正！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
##每个网格的序号
areaCoarse2Fine=[[0,1,2,3],[4,5,6],[7,8,9],[10,11,12],[13,14,15],[16,17,18],[19,20,21],[22,23,24],[25,26,27],[28,29]]
##每个网格的名称
areaCoarse2FineName=np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30])
##每个网格的经纬度
areaCoarse2FineLocation=np.array([[125.318334, 43.64432],[125.318334, 43.64432],[125.318334, 43.64432],[125.318334, 43.64432],[125.318334, 43.64432],[125.318334, 43.64432],[125.318334, 43.64432],[125.318334, 43.64432],[125.318334, 43.64432],[125.318334, 43.64432],[125.318334, 43.64432],[125.318334, 43.64432],[125.318334, 43.64432],[125.318334, 43.64432],[125.318334, 43.64432],[125.318334, 43.64432],[125.318334, 43.64432],[125.318334, 43.64432],[125.318334, 43.64432],[125.318334, 43.64432],[125.318334, 43.64432],[125.318334, 43.64432],[125.318334, 43.64432],[125.318334, 43.64432],[125.318334, 43.64432],[125.318334, 43.64432],[125.318334, 43.64432],[125.318334, 43.64432],[125.318334, 43.64432],[125.318334, 43.64432]])
def Coarse2FineInit():
    global timeCoarse2Fine
    global timeCoarse2FineName
    timeCoarse2Fine=np.zeros(shape=(7,12))
    timeCoarse2FineIndex=[]
    timeCoarse2FineName=[]
    for i in range(7):
        for j in range(12):
            timeCoarse2Fine[i][j]=i*12+j
            timeCoarse2FineName.append(str(i)+"d"+str(j)+"h")
    timeCoarse2FineName=np.array(timeCoarse2FineName)
Coarse2FineInit()
def entropy(c):
    temp = SKP.normalize([c], axis=1, norm='l1', return_norm=False)
    result = -1
    if(len(temp[0]) > 0):
        result = 0
    for x in temp[0]:
        if(x > 0):
            result += (-x)*math.log(x, 2)
    # return result/temp[0].shape[0]
    return result


def tensorStatistic(tensor):
    [A_lie, B_lie, C_lie] = tensor.shape
    sum = np.sum(np.sum(np.sum(tensor)))
    marginalA = []
    for i in range(A_lie):
        marginalA.append(np.sum(np.sum(tensor[i, :, :])))
    marginalB = []
    for i in range(B_lie):
        marginalB.append(np.sum(np.sum(tensor[:, i, :])))
    marginalC = []
    for i in range(C_lie):
        marginalC.append(np.sum(np.sum(tensor[:, :, i])))

    return [sum, marginalA, marginalB, marginalC]
# 节点数据结构
# name,value(张量原始不需要了),三个维度的边缘分布(marginalA,marginalB,marginalC)，分解得到三个维度的模式(A,B,C,ce_A,ce_B,ce_C),每个节点的数据量(sum)


class Node(object):
    # 初始化一个节点
    def __init__(self, name=None, tensor=None, ce_tensor=None, sum=None, marginalA=None, marginalB=None, marginalC=None, A=None, B=None, C=None, he=None, ce_A=None, ce_C=None, ce_he=None, time=None, industry=None, area=None, areaLocation=None, entropyThree=None, pattern2D=None, anomalyTime=None, anomalyArea=None):
        self.name = name
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
        self.ce_he = ce_he  # 节点值
        self.time = time  # 节点值
        self.industry = industry  # 节点值
        self.area = area  # 节点值
        self.areaLocation = areaLocation
        self.entropyThree = entropyThree
        self.pattern2D = pattern2D
        self.anomalyTime = anomalyTime
        self.anomalyArea = anomalyArea
        self.children = []    # 子节点列表
    # 添加一个孩子节点

    def add_children(self, node):
        self.children.append(node)


root = None


def treeInit():
    global root
    global zhangliang, zhangliang_ce,zhangliang_fine,zhangliang_ce_fine
    time = np.array(["Monday", "Tuesday", "Wednesday",
                     "Thursday", "Friday", "Saturday", "Sunday"])
    industry = np.array(['物业服务与管理', '供热', '占道经营', '违章建筑', '供水', '道路建设与维护', '工作效率', '噪声污染', '土地资源管理', '交通规划', '营运管理', '养老保险', '社会治安', '环境卫生', '优惠政策', '房屋产权办理', '工作纪律', '燃气', '劳动监察', '拆迁管理', '下水排水',
                         '媒体内容', '低保管理', '工商活动', '农村路桥建设维护', '空气污染', '特殊扶助', '经营性收费', '交通秩序', '服务态度与质量', '交通设施建设维护', '消防安全', '人口管理', '医疗保险', '补课办班', '园林绿化', '路灯管理', '房屋交易', '政务公开', '基层组织建设', '供电', '房地产开发', '废弃物', '教学管理'])
    area = np.array(["朝阳区CY", "南关区NG", "宽城区KC", "二道区ED", "绿园区LY",
                     "双阳区SY", "九台市JT", "德惠市DH", "农安县NA", "榆树市YS"])
    areaLocation = np.array([[125.318334, 43.64432], [125.447115, 43.739438], [125.332132, 44.080271], [125.642587, 43.899292], [125.182654, 43.899292], [
                            125.667883, 43.522281], [125.854156, 44.154825], [125.720775, 44.545913], [125.182654, 44.450447], [126.562452, 44.841186]])
    zhangliang, zhangliang_ce,zhangliang_fine,zhangliang_ce_fine = load.load()
    AAll, BAll, CAll, heAll, ce_AAll, ce_CAll, ce_heAll, anomalyTime, anomalyArea = ncpEnsembles.ncpEnsembles(
        zhangliang, zhangliang_ce)
    # 降维
    temp1 = np.concatenate((AAll, BAll, CAll), axis=0)
    temp2 = np.concatenate((ce_AAll, BAll, ce_CAll), axis=0)
    patternABC = np.concatenate((temp1, temp2), axis=1)
    embedding = MDS(n_components=2)
    pattern2D = embedding.fit_transform(patternABC.T)
    sum, marginalA, marginalB, marginalC = tensorStatistic(zhangliang_ce)
    entropyThree = [entropy(marginalA), entropy(marginalB), entropy(marginalC)]
    root = Node('Root', zhangliang, zhangliang_ce, sum, marginalA, marginalB, marginalC, AAll.T, BAll.T,
                CAll.T, heAll, ce_AAll.T, ce_CAll.T, ce_heAll, time, industry, area, areaLocation, entropyThree, pattern2D, anomalyTime, anomalyArea)

treeInit()


def treeFind(node, str, out=None):
    """
    N叉树的前序遍历-查找
    """
    if node:
        if node.name == str:                    # 如果输入结点不为空
            out = node
        else:              # 添加结点值到结果列表
            for child in node.children:     # 对每一棵子树做前序遍历
                out = treeFind(child, str, out)
    return out


def partition(tensorName, clusterDimension, clusterNum):
    nodeSelected = treeFind(root, tensorName)
    # 聚类
    if clusterDimension == 0:
        kmeans = KMeans(n_clusters=clusterNum, random_state=0).fit(
            nodeSelected.ce_A.T)
    elif clusterDimension == 1:
        kmeans = KMeans(n_clusters=clusterNum,
                        random_state=0).fit(nodeSelected.B.T)
    else:
        kmeans = KMeans(n_clusters=clusterNum, random_state=0).fit(
            nodeSelected.ce_C.T)
    for i in range(clusterNum):
        if clusterDimension == 2:
            cluster_one = np.where(kmeans.labels_ == clusterNum-1-i)[0]
        else:
            cluster_one = np.where(kmeans.labels_ == i)[0]
        tensorTemp = None
        ce_tensorTemp = None
        dimensionStrTemp = ["-A", "-B", "-C"]
        if clusterDimension == 0:
            tensorTemp = nodeSelected.tensor[cluster_one, :, :]
            ce_tensorTemp = nodeSelected.ce_tensor[cluster_one, :, :]
            timeTemp = nodeSelected.time[cluster_one]
            industryTemp = nodeSelected.industry
            areaTemp = nodeSelected.area
            areaLocationTemp = nodeSelected.areaLocation
        elif clusterDimension == 1:
            tensorTemp = nodeSelected.tensor[:, cluster_one, :]
            ce_tensorTemp = nodeSelected.ce_tensor[:, cluster_one, :]
            industryTemp = nodeSelected.industry[cluster_one]
            timeTemp = nodeSelected.time
            areaTemp = nodeSelected.area
            areaLocationTemp = nodeSelected.areaLocation
        else:
            tensorTemp = nodeSelected.tensor[:, :, cluster_one]
            ce_tensorTemp = nodeSelected.ce_tensor[:, :, cluster_one]
            areaTemp = nodeSelected.area[cluster_one]
            areaLocationTemp = nodeSelected.areaLocation[cluster_one, :]
            timeTemp = nodeSelected.time
            industryTemp = nodeSelected.industry
        AAll, BAll, CAll, heAll, ce_AAll, ce_CAll, ce_heAll, anomalyTime, anomalyArea = ncpEnsembles.ncpEnsembles(
            tensorTemp, ce_tensorTemp)
        sum, marginalA, marginalB, marginalC = tensorStatistic(ce_tensorTemp)
        entropyThree = [entropy(marginalA), entropy(
            marginalB), entropy(marginalC)]
        # 降维
        temp1 = np.concatenate((AAll, BAll, CAll), axis=0)
        temp2 = np.concatenate((ce_AAll, BAll, ce_CAll), axis=0)
        patternABC = np.concatenate((temp1, temp2), axis=1)
        embedding = MDS(n_components=2)
        pattern2D = embedding.fit_transform(patternABC.T)
        nodeTemp = Node(tensorName+dimensionStrTemp[clusterDimension]+str(i), tensorTemp, ce_tensorTemp, sum, marginalA, marginalB, marginalC,
                        AAll.T, BAll.T, CAll.T, heAll, ce_AAll.T, ce_CAll.T, ce_heAll, timeTemp, industryTemp, areaTemp, areaLocationTemp, entropyThree,  pattern2D, anomalyTime, anomalyArea)
        nodeSelected.add_children(nodeTemp)
    return root

def selectNodeLiduFind(tensorName):
    """
    细粒度
    """
    time = np.array(["Monday", "Tuesday", "Wednesday",
                     "Thursday", "Friday", "Saturday", "Sunday"])
    industry = np.array(['物业服务与管理', '供热', '占道经营', '违章建筑', '供水', '道路建设与维护', '工作效率', '噪声污染', '土地资源管理', '交通规划', '营运管理', '养老保险', '社会治安', '环境卫生', '优惠政策', '房屋产权办理', '工作纪律', '燃气', '劳动监察', '拆迁管理', '下水排水',
                         '媒体内容', '低保管理', '工商活动', '农村路桥建设维护', '空气污染', '特殊扶助', '经营性收费', '交通秩序', '服务态度与质量', '交通设施建设维护', '消防安全', '人口管理', '医疗保险', '补课办班', '园林绿化', '路灯管理', '房屋交易', '政务公开', '基层组织建设', '供电', '房地产开发', '废弃物', '教学管理'])
    area = np.array(["朝阳区CY", "南关区NG", "宽城区KC", "二道区ED", "绿园区LY",
                     "双阳区SY", "九台市JT", "德惠市DH", "农安县NA", "榆树市YS"])
    nodeSelected = treeFind(root, tensorName)
    timeFine = np.array([])
    areaFine = np.array([])
    for i in range(len(nodeSelected.time)):
        index = np.where(time == nodeSelected.time[i])
        timeFine=np.append(timeFine,timeCoarse2Fine[index[0][0]])
    for i in range(len(nodeSelected.area)):
        index = np.where(area == nodeSelected.area[i])
        areaFine=np.append(areaFine,areaCoarse2Fine[index[0][0]])

    timeFine=np.array(list(map(int, timeFine)))
    areaFine=np.array(list(map(int, areaFine)))
    tensorTemp = zhangliang_fine[timeFine, :, :]
    tensorTemp = tensorTemp[:, :, areaFine]
    ce_tensorTemp = zhangliang_ce_fine[timeFine, :, :]
    ce_tensorTemp = ce_tensorTemp[:, :, areaFine]
    timeTemp = timeCoarse2FineName[timeFine]
    industryTemp = nodeSelected.industry
    
    areaTemp = areaCoarse2FineName[areaFine]
    areaLocationTemp = areaCoarse2FineLocation[areaFine]
    AAll, BAll, CAll, heAll, ce_AAll, ce_CAll, ce_heAll, anomalyTime, anomalyArea = ncpEnsembles.ncpEnsembles(tensorTemp, ce_tensorTemp)
    sum, marginalA, marginalB, marginalC = tensorStatistic(ce_tensorTemp)
    entropyThree = [entropy(marginalA), entropy(marginalB), entropy(marginalC)]
    # 降维
    temp1 = np.concatenate((AAll, BAll, CAll), axis=0)
    temp2 = np.concatenate((ce_AAll, BAll, ce_CAll), axis=0)
    patternABC = np.concatenate((temp1, temp2), axis=1)
    embedding = MDS(n_components=2)
    pattern2D = embedding.fit_transform(patternABC.T)
    nodeTemp = Node(nodeSelected.name+"-find", tensorTemp, ce_tensorTemp, sum, marginalA, marginalB, marginalC,
                    AAll.T, BAll.T, CAll.T, heAll, ce_AAll.T, ce_CAll.T, ce_heAll, timeTemp, industryTemp, areaTemp, areaLocationTemp, entropyThree,  pattern2D, anomalyTime, anomalyArea)
    nodeSelected.add_children(nodeTemp)
    return root