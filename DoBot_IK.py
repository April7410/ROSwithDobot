import numpy as np
from numpy import transpose, cross, arctan2, arcsin
from numpy.linalg import norm
from subprobs import *

def DoBot_IK(p0T):
    l1 = 103; l2 = 135; l3 = 160; l4 = 50; l5 = 75;
    ex = transpose([1,0,0]); ey = transpose([0, 1,0]); ez = transpose([0,0,1]);
    zv = transpose([0,0,0])
    h1 = ez; h2 = ey; h3 = ey; h4 = ey;
    p01 = l1 * ez; p12 = zv; p23 = l2 * ez; p34 = l3 * ex; p4T = l5 * ex - l5 * ez
    d = np.sum(transpose(ey) * (p23 + p34 + p4T))
    q1sol = subprob4(-ez, ey, p0T -p01, d)
    q3sol = np.zeros((2,2))
    q2sol =  np.zeros((2,2))

    for i in [0,1]:
        print("rot(h1, -q1sol[i])")
        print(rot(h1, -q1sol[i]))
        print("(p0T - p01) - p4T")
        print((p0T - p01) - p4T)
        d = norm(rot(h1, -q1sol[i]) * (p0T - p01) - p4T)

        q3sol = np.append(q3sol, subprob3(ey, -p34, p23, d), axis=1)
        q3sol = np.delete(q3sol, 0,1)
        print("*****q3sol***")
        print(q3sol)
        for j in [0,1]:
            q2sol[i,j] = subprob1(ey, p23+ rot(h3, q3sol[j,i]) @ p34, rot(h1, - q1sol[i]) @ (p0T - p01) - p4T)

    qsol = np.array([[float(q1sol[0]),float(q1sol[0]), float(q1sol[1]), float(q1sol[1])],
                     [q2sol[0,0], q2sol[1,0], q2sol[0,1], q2sol[1,1]],
                     [q3sol[0,0], q3sol[1,0], q3sol[0,1], q3sol[1,1]]])
    print("*******qsol**********")
    print(qsol)
    qsol = np.append(qsol, -(qsol[2,:] + qsol[1,:]), 1)
    print(qsol)
    return qsol