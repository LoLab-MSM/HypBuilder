
# Lighthouse example from john Skillings web page
# http://www.inference.phy.cam.ac.uk/bayesys/
# compare to mininest.py + lighthouse.py

from NestedSamplingKDE import NS_KDE
from math import *

def likelihood(p):

    D = [ 4.73,  0.45, -1.73,  1.09,  2.19,  0.12,
        1.31,  1.00,  1.32,  1.07,  0.86, -0.49, -2.59,  1.73,  2.11,
        1.61,  4.98,  1.71,  2.23,-57.20,  0.96,  1.25, -1.56,  2.45,
        1.19,  2.17,-10.66,  1.91, -4.16,  1.92,  0.10,  1.98, -2.51,
        5.55, -0.47,  1.91,  0.95, -0.78, -0.84,  1.72, -0.01,  1.48,
        2.70,  1.21,  4.41, -4.79,  1.33,  0.81,  0.20,  1.58,  1.29,
        16.19,  2.75, -2.38, -1.79,  6.50,-18.53,  0.72,  0.94,  3.64,
        1.94, -0.11,  1.57,  0.57]

    N = len(D)
    logL = 0.0

    point = [4.0*p[0]-2,2*p[1]]

    for k in range(N):
        logL += log((point[1]/3.1416) / ((D[k]-point[0])*(D[k]-point[0]) + point[1]*point[1]))
    return logL

a = [0,1]
b = [0,1]

param_dist = [a, b]

print NS_KDE(likelihood, None, param_dist).Z