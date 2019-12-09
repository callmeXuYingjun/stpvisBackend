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
    pM.append(input_zhangliang.transpose(
        (0, 1, 2)).reshape(A_lie, B_lie*C_lie))
    pM.append(input_zhangliang.transpose(
        (1, 0, 2)).reshape(B_lie, A_lie*C_lie))
    pM.append(input_zhangliang.transpose(
        (2, 0, 1)).reshape(C_lie, B_lie*A_lie))
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


    A_temp, norm_A = SKP.normalize(A_temp, axis=0, norm='l2', return_norm=True, copy=True)
    C_temp, norm_C = SKP.normalize(C_temp, axis=0, norm='l2', return_norm=True, copy=True)
    return [A_temp, C_temp, norm_A*norm_C*input_he]
