import numpy as np
import math


def summation(number):
    sum = 0
    for i in range(number):
        sum += i
    return


num = 10
a = 7
b = 44
c = 10
A_bufen = []
B_bufen = []
C_bufen = []
for i in range(a):
    A_bufen.append(i)
for i in range(b):
    B_bufen.append(i)
for i in range(c):
    C_bufen.append(i)

quanzhong = np.zeros(num-1)
for kk in range(num-1):
    quanzhong[kk] = math.exp(-(kk-(num-1))**2/(num-1)**2)
quanzhong = quanzhong/quanzhong.sum()
ab = ['物业服务与管理', '供热', '占道经营', '违章建筑', '供水', '道路建设与维护', '工作效率', '噪声污染', '土地资源管理', '交通规划', '营运管理', '养老保险', '社会治安', '环境卫生', '优惠政策', '房屋产权办理', '工作纪律', '燃气', '劳动监察', '拆迁管理', '下水排水', '媒体内容',
      '低保管理', '工商活动', '农村路桥建设维护', '空气污染', '特殊扶助', '经营性收费', '交通秩序', '服务态度与质量', '交通设施建设维护', '消防安全', '人口管理', '医疗保险', '补课办班', '园林绿化', '路灯管理', '房屋交易', '政务公开', '基层组织建设', '供电', '房地产开发', '废弃物', '教学管理']
zhangliang = np.zeros((len(A_bufen), len(B_bufen), len(C_bufen)))
zhangliang_ce = np.zeros((len(A_bufen), len(B_bufen), len(C_bufen)))
for zhou in range(num):
    NN = np.zeros((7, 44, 10))
    for i in range(len(ab)):
        my_matrix = np.loadtxt(open("C:\\Users\\Administrator\\Desktop\\industry_two_7\\zhou_"+str(
            zhou)+"\\"+ab[i]+".csv", "rb"), delimiter=",", skiprows=1, usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        NN[:, i, :] = my_matrix
    if zhou == num:
        zhangliang_ce = NN[A_bufen, :, :][:, B_bufen, :][:, :, C_bufen]
    else:
        zhangliang = zhangliang+NN[A_bufen, :, :][:,
                                                  B_bufen, :][:, :, C_bufen]*quanzhong[zhou-1]

print(zhangliang[0, 0, 0], zhangliang_ce[0, 0, 0])

# index=1
# Main(zhangliang_ce,zhangliang,index)
