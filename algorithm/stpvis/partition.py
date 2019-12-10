import numpy as np
import math
from algorithm.stpvis import load
from algorithm.stpvis import ncp_abc
from algorithm.stpvis import ncp_ac


def summation(number):
    sum = 0
    for i in range(number):
        sum += i
    return


zhangliang, zhangliang_ce = load.load()
A, B, C, he = ncp_abc.ncp_abc(zhangliang, 3)
ce_A, ce_C, ce_he = ncp_ac.ncp_ac(zhangliang_ce, B, he)
print(he)
print(ce_he)
