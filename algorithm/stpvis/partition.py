import numpy as np
import math
from algorithm.stpvis import load
from algorithm.stpvis import ncp_abc
from algorithm.stpvis import ncp_ac
from algorithm import models
import json
from sklearn.cluster import KMeans


def summation(number):
    sum = 0
    for i in range(number):
        sum += i
    return


zhangliang, zhangliang_ce = load.load()
A, B, C, he = ncp_abc.ncp_abc(zhangliang, 3)
ce_A, ce_C, ce_he = ncp_ac.ncp_ac(zhangliang_ce, B, he)


# 聚类
# kmeans = KMeans(n_clusters=3, random_state=0).fit(A)
# print(kmeans.labels_)


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

#节点数据结构
# class Node(object):
#     # 初始化一个节点
#     def __init__(self,value = None):
#         self.value = value  # 节点值
#         self.child_list = []    # 子节点列表
#     # 添加一个孩子节点
#     def add_child(self,node):
#         self.child_list.append(node)

# root = Node('A')
# B = Node('B')
# root.add_child(B)
# root.add_child(Node('C'))
# D = Node('D')
# root.add_child(D)
# B.add_child(Node('E'))
# B.add_child(Node('F'))
# B.add_child(Node('G'))
# D.add_child(Node('H'))
# D.add_child(Node('I'))
# D.add_child(Node('J'))
# print(json.dumps(root, default=lambda obj: obj.__dict__, sort_keys=True, indent=4))


