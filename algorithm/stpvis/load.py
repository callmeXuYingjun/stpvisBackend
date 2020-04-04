import numpy as np
import math

def load():
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
    a_fine = 84
    b_fine= 44
    c_fine = 1440
    A_bufen_fine = []
    B_bufen_fine = []
    C_bufen_fine = []
    for i in range(a_fine):
        A_bufen_fine.append(i)
    for i in range(b_fine):
        B_bufen_fine.append(i)
    for i in range(c_fine):
        C_bufen_fine.append(i)

    # quanzhong = np.zeros(num-1)
    # for kk in range(1, num):
    #     quanzhong[kk-1] = math.exp(-(kk-(num-1))**2/(num-1)**2)
    # quanzhong = quanzhong/quanzhong.sum()
    # ab = ['物业服务与管理', '供热', '占道经营', '违章建筑', '供水', '道路建设与维护', '工作效率', '噪声污染', '土地资源管理', '交通规划', '营运管理', '养老保险', '社会治安', '环境卫生', '优惠政策', '房屋产权办理', '工作纪律', '燃气', '劳动监察', '拆迁管理', '下水排水', '媒体内容',
    #       '低保管理', '工商活动', '农村路桥建设维护', '空气污染', '特殊扶助', '经营性收费', '交通秩序', '服务态度与质量', '交通设施建设维护', '消防安全', '人口管理', '医疗保险', '补课办班', '园林绿化', '路灯管理', '房屋交易', '政务公开', '基层组织建设', '供电', '房地产开发', '废弃物', '教学管理']
    # zhangliang = np.zeros((len(A_bufen), len(B_bufen), len(C_bufen)))
    # zhangliang_ce = np.zeros((len(A_bufen), len(B_bufen), len(C_bufen)))
    # for zhou in range(num):
    #     NN = np.zeros((7, 44, 10))
    #     for i in range(len(ab)):
    #         my_matrix = np.loadtxt(open("C:\\Users\\Administrator\\Desktop\\industry_two_7\\zhou_"+str(
    #             zhou)+"\\"+ab[i]+".csv", "rb"), delimiter=",", skiprows=1, usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    #         NN[:, i, :] = my_matrix
    #     if zhou == num-1:
    #         zhangliang_ce = NN[A_bufen, :, :][:, B_bufen, :][:, :, C_bufen]
    #     else:
    #         zhangliang = zhangliang+NN[A_bufen, :, :][:,
    #                                                   B_bufen, :][:, :, C_bufen]*quanzhong[zhou]
    zhangliang = np.random.randint(1,10,(len(A_bufen), len(B_bufen), len(C_bufen)))
    zhangliang_ce =np.random.randint(1,10,(len(A_bufen), len(B_bufen), len(C_bufen)))
    zhangliang_fine = np.random.randint(1,10,(len(A_bufen_fine), len(B_bufen_fine), len(C_bufen_fine)))
    zhangliang_ce_fine =np.random.randint(1,10,(len(A_bufen_fine), len(B_bufen_fine), len(C_bufen_fine)))
    industryGroup1=[1,4,17,20,40]         #公共事业
    industryGroup2=[2,3,5,9,10,12,15,21,23,27,28,30,31,32,34,35,36,37,41,43]#城市管理
    industryGroup3=[0,6,11,14,16,18,29,33,38]#公共服务
    industryGroup4=[8,19,22,24,26,39]#乡村建设
    industryGroup5=[7,13,25,42]#环境污染

    #城市-工作日
    zhangliang1 = np.random.randint(20,30,(5,44,5))
    zhangliang1[:,industryGroup1,:] = zhangliang1[:,industryGroup1,:]*10
    zhangliang1[:,industryGroup2,:] = zhangliang1[:,industryGroup2,:]*3
    zhangliang1[:,industryGroup3,:] = zhangliang1[:,industryGroup3,:]*7
    zhangliang1[:,industryGroup4,:] = zhangliang1[:,industryGroup4,:]*1
    zhangliang1[:,industryGroup5,:] = zhangliang1[:,industryGroup5,:]*3
    #城市-周末
    zhangliang2 = np.random.randint(10,15,(2,44,5))
    zhangliang2[:,industryGroup1,:] = zhangliang2[:,industryGroup1,:]*10
    zhangliang2[:,industryGroup2,:] = zhangliang2[:,industryGroup2,:]*3
    zhangliang2[:,industryGroup3,:] = zhangliang2[:,industryGroup3,:]*7
    zhangliang2[:,industryGroup4,:] = zhangliang2[:,industryGroup4,:]*1
    zhangliang2[:,industryGroup5,:] = zhangliang2[:,industryGroup5,:]*3
    #乡镇-工作日
    zhangliang3 = np.random.randint(10,15,(5,44,5))
    zhangliang3[:,industryGroup1,:] = zhangliang3[:,industryGroup1,:]*2
    zhangliang3[:,industryGroup2,:] = zhangliang3[:,industryGroup2,:]*1
    zhangliang3[:,industryGroup3,:] = zhangliang3[:,industryGroup3,:]*5
    zhangliang3[:,industryGroup4,:] = zhangliang3[:,industryGroup4,:]*10
    zhangliang3[:,industryGroup5,:] = zhangliang3[:,industryGroup5,:]*5
    
    #乡镇-周末
    zhangliang4 = np.random.randint(0,5,(2,44,5))
    zhangliang4[:,industryGroup1,:] = zhangliang4[:,industryGroup1,:]*2
    zhangliang4[:,industryGroup2,:] = zhangliang4[:,industryGroup2,:]*1
    zhangliang4[:,industryGroup3,:] = zhangliang4[:,industryGroup3,:]*5
    zhangliang4[:,industryGroup4,:] = zhangliang4[:,industryGroup4,:]*10
    zhangliang4[:,industryGroup5,:] = zhangliang4[:,industryGroup5,:]*5

    zhangliang12=np.concatenate([zhangliang1,zhangliang2],axis=0)
    zhangliang34=np.concatenate([zhangliang3,zhangliang4],axis=0)
    zhangliang1234=np.concatenate([zhangliang12,zhangliang34],axis=2)
    # zhangliang1234
    # print(zhangliang3.shape)
    zhangliang_ce_1234=zhangliang1234.copy()
    zhangliang_ce_1234[0,:,:] = zhangliang_ce_1234[0,:,:]*10
    zhangliang_ce_1234[1,:,:] = zhangliang_ce_1234[1,:,:]*8
    zhangliang_ce_1234[2,:,:] = zhangliang_ce_1234[2,:,:]*9
    zhangliang_ce_1234[3,:,:] = zhangliang_ce_1234[3,:,:]*6
    zhangliang_ce_1234[4,:,:] = zhangliang_ce_1234[4,:,:]*7
    zhangliang_ce_1234[5,:,:] = zhangliang_ce_1234[5,:,:]*2
    zhangliang_ce_1234[6,:,:] = zhangliang_ce_1234[6,:,:]*1

    zhangliang_ce_1234[:,:,0] = zhangliang_ce_1234[:,:,0]*10
    zhangliang_ce_1234[:,:,1] = zhangliang_ce_1234[:,:,1]*8
    zhangliang_ce_1234[:,:,2] = zhangliang_ce_1234[:,:,2]*9
    zhangliang_ce_1234[:,:,3] = zhangliang_ce_1234[:,:,3]*6
    zhangliang_ce_1234[:,:,4] = zhangliang_ce_1234[:,:,4]*7
    zhangliang_ce_1234[:,:,5] = zhangliang_ce_1234[:,:,5]*2
    zhangliang_ce_1234[:,:,6] = zhangliang_ce_1234[:,:,6]*1
    zhangliang_ce_1234[:,:,7] = zhangliang_ce_1234[:,:,7]*3
    zhangliang_ce_1234[:,:,8] = zhangliang_ce_1234[:,:,8]*2
    zhangliang_ce_1234[:,:,9] = zhangliang_ce_1234[:,:,9]*1
    
    # zhangliang_ce_1234[:,1,:]=zhangliang_ce_1234[:,1,:]*10
    # zhangliang_ce_1234[:,0,:]=zhangliang_ce_1234[:,0,:]*10
    return [zhangliang1234, zhangliang_ce_1234,zhangliang_fine,zhangliang_ce_fine]
