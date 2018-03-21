#!/usr/bin/python

import numpy as np
import pandas as pd
from sympy.physics.quantum.cg import CG
from sympy import S

# Get coefficients for all combinations of j1,j2,m1,m2 leading to j3,m3
def get_coefficients(j3,m3,cutoff=3):
    """Reverse Clebsch-Gordan coupling

    This function returns a list of a list with all quantum numbers and
    coefficients leading to a fixed J,M combination

    Arguments
    ---------
    j3, m3: integers, Right hand side of CG-coefficients: <j1 j2 m1 m2|j3 m3>
    cutoff: (optional) integer, cutoff where to stop looking for couplings

    Returns
    -------
    sqm: a list of lists for each combination j1,j2,m1,m2, CG-coeff found for j3
         and m3
    """
    # Perhaps a 2d numpy array is better suited, no that needs to be fixed
    # length
    # List of lists: Each inner list holds j1,j2,m1,m2 and the coefficient
    sqm = []
    for j1 in range(0,cutoff):
        for j2 in range(0,cutoff):
            #Check boundaries of j3
            if np.abs(j1-j2) <= j3 and j1+j2 >= j3: 
                for m1 in range(-j1,j1+1):
                    for m2 in range(-j2,j2+1):
                        if m1+m2 == m3:
                            sqm.append([j1,j2,m1,m2,
                                        CG(j1,m1,j2,m2,j3,m3).doit()])
                            
    return sqm

def coupled_dirac_displacement(j3,m3,p_id,verb=False):
    """Couple gamma and displacements to correct CG-coefficients

    Arguments
    ---------
    j3,m3 : integer, the quantum numbers we want to couple to. 
    p_id : integer, Particle id for classification in Operators
    verb : (optional)

    Returns
    -------
    coeffs_frame: DataFrame that holds all quantum numbers and coefficients
    leading to a specific j3,m3 combination
    """
    # Get the first iteration of couplings that lead to j3 and m3
    coeffs_frame = pd.DataFrame(get_coefficients(1,0),
                                columns=['j^{%d}_{\gamma}'%p_id,'j^{%d}_{D}'%p_id,
                                         'm^{%d}_{\gamma}'%p_id,'m^{%d}_{D}'%p_id,
                                         'coeff'])
 
    # For the case of more than one displacement we recouple the displacements
    # TODO: This is not recursive yet!
    # Initialize dataframe. first two keys are the same as for the primary
    # dataframe
    secondary_coeffs = pd.DataFrame(columns=['j^{%d}_{D}'%p_id,'m^{%d}_{D}'%p_id,
                                             'j_{d1}','j_{d2}',
                                             'm_{d1}','m_d{2}','coeffs'])
    # loop over Displacements quantum numbers
    for jd in zip(coeffs_frame['j^{%d}_{D}'%p_id],
                  coeffs_frame['m^{%d}_{D}'%p_id],
                  coeffs_frame['coeff']):
        # get coefficients for j_D larger than 1
        if jd[0] > 1 and jd[2] != 0:
            tmp_coeffs = pd.DataFrame(get_coefficients(jd[0],
                jd[1],cutoff=jd[0]),columns=['j_{d1}','j_{d2}',
                    'm_{d1}','m_d{2}','coeffs'])
            tmp_coeffs['j^{%d}_{D}'%p_id] = jd[0]
            tmp_coeffs['m^{%d}_{D}'%p_id] = jd[1]
            secondary_coeffs = secondary_coeffs.append(tmp_coeffs)
    # Left merge them onto the primary dataframe 
    coeffs_frame = pd.merge(coeffs_frame,secondary_coeffs,how='left',
             on=['j^{%d}_{D}'%p_id,'m^{%d}_{D}'%p_id],left_index=True)
   

def main():
    #coeffs = np.asarray(get_coefficients(1,0))
    J,M = 1,0
    particle_id = 0

    coefficients_table = coupled_dirac_displacement(J,M,particle_id)

    print(coefficients_table)


if __name__ == "__main__":                          
    try:
        main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
