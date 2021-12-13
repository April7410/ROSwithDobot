from math import sqrt, sin, cos
import numpy as np
from numpy import transpose, cross, arctan2, arcsin
from numpy.linalg import norm

# q=subprob0(k,p1,p2)
#
# solve for q subtended between p1 and p2
#    k determines the sign of q
#
# input: k,p1,p2 as R^3 column vectors
# output: q (scalar)
#

def subprob0(k,p1,p2):

    p1=p1/norm(p1)
    p2=p2/norm(p2)

    q=2*np.arctan2(norm(p1-p2),norm(p1+p2))

    if transpose(k)*(cross(p1,p2))<0:
        q=-q
    return q




#
# q = subprob1(k, p1, p2)
#
# solve for q from
#
# exp(kx q) p1 = p2
#
# input: k, p1, p2 as R ^ 3 column vectors
# output: q(scalar)
#

def subprob1(k, p1, p2):

    p2 = p2 / norm(p2) * norm(p1);

    k = k / norm(k);
    pp1 = p1 - (transpose(p1)*k)*k;
    pp2=p2-(transpose(p2)*k)*k;

    epp1=pp1 / norm(pp1);
    epp2 = pp2 / norm(pp2);

    q = subprob0(k, epp1, epp2);
    return q

#
# q=subprob3(k,p1,p2,d)
#
# solve for theta from
#
# norm(p2-exp(k x q) p1) = d
#
# input: k,p1,p2 as R^3 column vectors, delta: scalar
# output: q (2x1 vector, 2 solutions)
#

def subprob3(k,p1,p2,d):

    pp1 = p1 - transpose(k) * p1 *k;
    pp2 = p2 - transpose(k)* p2* k;
    dpsq = d*d - (transpose(k)*(p1-p2))*(transpose(k)*(p1-p2));


    if dpsq==0:
        q = subprob1(k,pp1/norm(pp1),pp2/norm(pp2));
        return q


    bb=(norm(pp1)^2+norm(pp2)^2-dpsq)/(2*norm(pp1)*norm(pp2));
    if abs(bb)>1:
        q = transpose(np.array([NaN,NaN]))
        return q

    phi=acos(bb);

    q0=subprob1(k,pp1/norm(pp1),pp2/norm(pp2));
    q = np.zeros(2,1);

    q[0] = q0+phi;
    q[1] = q0-phi;
    return q

#
# q=subprob4(k,h,p,d)
#
# solve for theta from
#
# d=h'*rot(k,q)*p
#
# input: k,h,p as R^3 vectors, k,h are unit vectors, d: scalar
# output: q (up to 2 solutions)
#

def subprob4(k,h,p,d):
    print(k,"___", h, "___",  p, "___", d)
    d=d/norm(h);
    h=h/norm(h);
    ## Disclaimer: MAY CAUSE PROBLEMS IN MATLAB THIS WAS h.' NOT h'
    c= d - (transpose(h)*p + transpose(h)*hat(k)*hat(k)*p);
    a = transpose(h) * hat(k)*p;
    b=-transpose(h) * hat(k)*hat(k)*p;

    phi=arctan2(b,a);

    q = np.zeros((2,1));
    print(a)
    print(b)
    psi=arcsin(c/norm(a,b));

    q[1]=-phi+psi;
    q[2]=-phi-psi+pi;
    return q


def hat(k):

  return np.array([[0, -k[2], k[1]] , [k[2], 0, -k[1]],  [-k[1], k[0], 0]])

def rot(k,theta):

  k = k / norm(k);
  R=np.eye(3,3) + sin(theta) * hat(k)+(1-cos(theta))*hat(k)*hat(k);
