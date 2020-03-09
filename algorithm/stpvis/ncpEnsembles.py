import numpy as np
from algorithm.stpvis import ncp_abc
from algorithm.stpvis import ncp_ac

def ncpEnsembles(zhangliang,zhangliang_ce):
    AAll=None
    BAll=None
    CAll=None
    heAll=None
    ce_AAll=None
    ce_CAll=None
    ce_heAll=None
    anomalyArea=None
    anomalyTime=None
    for i in range(3,10):
        print(i)
        A, B, C, he = ncp_abc.ncp_abc(zhangliang, i)
        ce_A, ce_C, ce_he = ncp_ac.ncp_ac(zhangliang_ce, B, he)
        anomalyTimeTemp = np.sqrt(np.sum(np.square(A-ce_A),axis=1))
        anomalyTimeTemp=anomalyTimeTemp.reshape(anomalyTimeTemp.shape[0],1)
        anomalyAreaTemp = np.sqrt(np.sum(np.square(C-ce_C),axis=1))
        anomalyAreaTemp=anomalyAreaTemp.reshape(anomalyAreaTemp.shape[0],1)
        if AAll is None:
            AAll=A
            BAll=B
            CAll=C
            heAll=he
            ce_AAll=ce_A
            ce_CAll=ce_C
            ce_heAll=ce_he
            anomalyTime=anomalyTimeTemp
            anomalyArea=anomalyAreaTemp
        else:
            AAll=np.concatenate((AAll,A),axis=1)
            BAll=np.concatenate((BAll,B),axis=1)
            CAll=np.concatenate((CAll,C),axis=1)
            heAll=np.concatenate((heAll,he),axis=0)
            ce_AAll=np.concatenate((ce_AAll,ce_A),axis=1)
            ce_CAll=np.concatenate((ce_CAll,ce_C),axis=1)
            ce_heAll=np.concatenate((ce_heAll,ce_he),axis=0)
            anomalyTime=np.concatenate((anomalyTime,anomalyTimeTemp),axis=1)
            anomalyArea=np.concatenate((anomalyArea,anomalyAreaTemp),axis=1)
    return [AAll, BAll, CAll, heAll,ce_AAll, ce_CAll, ce_heAll,anomalyTime,anomalyArea]