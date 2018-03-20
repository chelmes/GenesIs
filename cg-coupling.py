#!/usr/bin/python
from sympy.physics.quantum.cg import CG
from sympy import S
# Get coefficients for all combinations of j1,j2,m1,m2 leading to j3,m3
def get_coefficients(j3,m3):
    # Perhaps a 2d numpy array is better suited, no that needs to be fixed
    # length
    single_quatnum_numbers = []
    for j1 in range(0,j3):
        for j2 in range(0,j3):
            
            # TODO: Implement logic in buried function
            if  j1 + j2 == j3:
            if  j1 - j2 == j3:
            if -j1 + j2 == j3:
            if -j1 - j2 == j3:        
    return single_quantum_numbers
Coeffs = [cg(1,0,1,0,1,1).doit() for ]

