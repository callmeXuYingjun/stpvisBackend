import numpy as np
from sktensor import ktensor

def muntf(X, k, init = None, min_iter = 20, max_iter = 100):
    #initialization
    if init is None:
        Finit = [np.random.rand(X.shape[i], k) for i in range(len(X.shape))]
    else:
        Finit = init

    F_cell = normalize_column_pair(Finit)
    FF = []
    for k in range(len(X.shape)):
        FF.append((F_cell[k].T.dot(F_cell[k])))
    # D = np.diag(np.sum(S, axis=1))
    norm_X = np.sqrt(np.sum(np.asarray(X.vals) ** 2))
    eps = 1e-16
    #iter
    for iter in range(max_iter):

        #cal A
        factor = X.uttkrp(F_cell, 0)
        ata = FF[1] * FF[2]
        dominator = F_cell[0].dot(ata)
        F_cell[0] *= (factor + eps) /(dominator + eps)

        F_cell[0][F_cell[0] < eps] = 0

        FF[0] = F_cell[0].T.dot(F_cell[0])
        #cal B
        factor = X.uttkrp(F_cell, 1)
        ata = FF[0] * FF[2]
        dominator = F_cell[1].dot(ata)
        F_cell[1] *= (factor + eps) / (dominator + eps)

        F_cell[1][F_cell[1] < eps]= 0

        FF[1] = F_cell[1].T.dot(F_cell[1])
        #cal C
        factor = X.uttkrp(F_cell, 2)
        dominator = F_cell[2].dot(F_cell[2].T).dot(factor)
        F_cell[2] *= (factor + eps) / (dominator + eps)

        F_cell[2][F_cell[2] < eps]= 0
        
        FF[2] = F_cell[2].T.dot(F_cell[2])

        #update
        F_cell = normalize_column_pair(F_cell)
        for k in range(len(X.shape)):
            FF[k] = F_cell[k].T.dot(F_cell[k])

        
    X_approx = ktensor(F_cell).toarray()
    error = np.sqrt(np.sum((X_approx - X.toarray()) ** 2))
    rel_error = error / norm_X
    print ('ntf error:%s, rel error:%s' % (error, rel_error))

    return ktensor(F_cell)

def normalize_column_pair(F,by_norm='l2'):

    import sklearn.preprocessing as SKP
    F[0], norm_A = SKP.normalize(F[0], axis=0, norm=by_norm, return_norm=True, copy=True)
    F[2], norm_C = SKP.normalize(F[2], axis=0, norm=by_norm, return_norm=True, copy=True)
    F[1] = F[1].dot(np.diag(norm_A * norm_C))

    return F