#!/usr/bin/python

import numpy as np
from sympy.physics.quantum.cg import CG
from sympy import S
# Get coefficients for all combinations of j1,j2,m1,m2 leading to j3,m3
def get_coefficients(j3,m3):
    # Perhaps a 2d numpy array is better suited, no that needs to be fixed
    # length
    # List of lists: Each inner list holds j1,j2,m1,m2 and the coefficient
    sqm = []
    for j1 in range(0,3):
        for j2 in range(0,3):
            #Check boundaries of j3
            if np.abs(j1-j2) <= j3 and j1+j2 >= j3: 
                for m1 in range(-j1,j1+1):
                    for m2 in range(-j2,j2+1):
                        if m1+m2 == m3:
                            sqm.append([j1,j2,m1,m2,
                                        CG(j1,m1,j2,m2,j3,m3).doit()])
                            
    return sqm

def main():
    coeffs = get_coefficients(1,0)
    for c in coeffs:
        print(c)
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
