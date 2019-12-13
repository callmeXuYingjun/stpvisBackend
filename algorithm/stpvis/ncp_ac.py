import numpy as np
import sklearn.preprocessing as SKP


def ncp_ac(input_zhangliang, input_B,input_he):
    eps = 1e-16
    [A_lie, B_lie, C_lie] = input_zhangliang.shape
    [m, R] = input_B.shape
    A_temp = np.random.rand(A_lie, R)
    B_temp =input_B*input_he
    C_temp = np.random.rand(C_lie, R)
    pM = []
    pM.append(input_zhangliang.transpose((0,1,2)).reshape((A_lie,B_lie*C_lie),order="F"))
    pM.append(input_zhangliang.transpose((1,0,2)).reshape((B_lie,C_lie*A_lie),order="F"))
    pM.append(input_zhangliang.transpose((2,0,1)).reshape((C_lie,B_lie*A_lie),order="F"))
    for it in range(1000):
        # print(it)
        # 更新A矩阵
        X_temp = pM[0]
        CB_KR = np.zeros((B_lie*C_lie, R))
        for k in range(R):
            CB_KR[:, k] = np.kron(C_temp[:, k], B_temp[:, k])
        F_temp = CB_KR
        shang_temp = X_temp.dot(F_temp)
        xia_temp = A_temp.dot(F_temp.T).dot(F_temp)
        for heng in range(A_lie):
            for song in range(R):
                A_temp[heng, song] =A_temp[heng, song]*(shang_temp[heng, song]+eps)/(xia_temp[heng, song]+eps)

        # 更新C矩阵
        X_temp = pM[2]
        BA_KR = np.zeros((B_lie*A_lie, R))
        for k in range(R):
            BA_KR[:, k] = np.kron(B_temp[:, k], A_temp[:, k])
        F_temp = BA_KR
        shang_temp = X_temp.dot(F_temp)
        xia_temp = C_temp.dot(F_temp.T).dot(F_temp)
        for heng in range(C_lie):
            for song in range(R):
                C_temp[heng, song] =C_temp[heng, song]*(shang_temp[heng, song]+eps)/(xia_temp[heng, song]+eps)
    
    loss=0
    Hui=np.zeros((A_lie,B_lie,C_lie))
    for ii in range(A_lie):
            for jj in range(B_lie):
                for mm in range(C_lie):
                    summ=0
                    for kk in range(R):
                        summ=summ+A_temp[ii,kk]*B_temp[jj,kk]*C_temp[mm,kk]
                    Hui[ii,jj,mm]=summ
                    loss=loss+(Hui[ii,jj,mm]-input_zhangliang[ii,jj,mm])**2
    jishu=np.sum(np.sum(np.sum(input_zhangliang**2)))
    relfit=(1-loss/jishu)*100
    # print(relfit)

    A_temp, norm_A = SKP.normalize(A_temp, axis=0, norm='l2', return_norm=True)
    C_temp, norm_C = SKP.normalize(C_temp, axis=0, norm='l2', return_norm=True)
    return [A_temp, C_temp, norm_A*norm_C*input_he]
