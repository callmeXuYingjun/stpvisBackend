import numpy as np
import sklearn.preprocessing as SKP
def ncp_abc(input_zhangliang,R):
    eps = 1e-16
    [A_lie,B_lie,C_lie]=input_zhangliang.shape
    A_temp=np.random.rand(A_lie,R)
    B_temp=np.random.rand(B_lie,R)
    C_temp=np.random.rand(C_lie,R)
    pM=[]
    pM.append(input_zhangliang.transpose((0,1,2)).reshape(A_lie,B_lie*C_lie))
    pM.append(input_zhangliang.transpose((1,0,2)).reshape(B_lie,A_lie*C_lie))
    pM.append(input_zhangliang.transpose((2,0,1)).reshape(C_lie,B_lie*A_lie))
    for it in range(1000):
        print(it)
        # 更新A矩阵
        X_temp=pM[0]
        CB_KR=np.zeros((B_lie*C_lie,R))
        for k in range(R):
            CB_KR[:,k]=np.kron(C_temp[:,k],B_temp[:,k])
        F_temp=CB_KR
        shang_temp=X_temp.dot(F_temp)
        xia_temp=A_temp.dot(F_temp.T).dot(F_temp)
        for heng in range(A_lie):
            for song in range(R):
                if xia_temp[heng,song]!=0:
                    A_temp[heng,song]=A_temp[heng,song]*shang_temp[heng,song]/xia_temp[heng,song]
                else:
                    A_temp[heng,song]=A_temp[heng,song]*shang_temp[heng,song]/(xia_temp[heng,song]+eps)
        A_temp = SKP.normalize(A_temp, axis=0, norm='l2', return_norm=False, copy=True)

        # 更新C矩阵
        X_temp=pM[2]
        BA_KR=np.zeros((B_lie*A_lie,R))
        for k in range(R):
            BA_KR[:,k]=np.kron(B_temp[:,k],A_temp[:,k])
        F_temp=BA_KR
        shang_temp=X_temp.dot(F_temp)
        xia_temp=C_temp.dot(F_temp.T).dot(F_temp)
        for heng in range(C_lie):
            for song in range(R):
                if xia_temp[heng,song]!=0:
                    C_temp[heng,song]=C_temp[heng,song]*shang_temp[heng,song]/xia_temp[heng,song]
                else:
                    C_temp[heng,song]=C_temp[heng,song]*shang_temp[heng,song]/(xia_temp[heng,song]+eps)
        C_temp = SKP.normalize(C_temp, axis=0, norm='l2', return_norm=False, copy=True)


        # 更新B矩阵
        X_temp=pM[1]
        CA_KR=np.zeros((C_lie*A_lie,R))
        for k in range(R):
            CA_KR[:,k]=np.kron(C_temp[:,k],A_temp[:,k])
        F_temp=CA_KR
        shang_temp=X_temp.dot(F_temp)
        xia_temp=B_temp.dot(F_temp.T).dot(F_temp)
        for heng in range(B_lie):
            for song in range(R):
                if xia_temp[heng,song]!=0:
                    B_temp[heng,song]=B_temp[heng,song]*shang_temp[heng,song]/xia_temp[heng,song]
                else:
                    B_temp[heng,song]=B_temp[heng,song]*shang_temp[heng,song]/(xia_temp[heng,song]+eps)
    B_temp,norm_B= SKP.normalize(B_temp, axis=0, norm='l2', return_norm=True, copy=True)
    return  [A_temp,B_temp,C_temp,norm_B]
