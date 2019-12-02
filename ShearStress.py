import moment_of_inertia
import numpy as np
import matplotlib.pyplot as plt

def ShearStress(pos_list_xz, sh_load_xz, pos_list_yz, sh_load_yz):

    shear_b_Ar = []

    # loop through the span locations
    for i in range(len(pos_list_yz)):
        cur_Span_Loc = pos_list_yz[i]

        V_z = sh_load_xz[i]
        V_x = sh_load_yz[i]

        MoI = moment_of_inertia.MOI(cur_Span_Loc) # xx-yy-xy

        c1 = -(V_z*MoI[1]-V_x*MoI[2])/(MoI[0]*MoI[1]-MoI[2]**2) # stuff before the first and second integral
        c2 = -(V_x*MoI[0]-V_z*MoI[2])/(MoI[0]*MoI[1]-MoI[2]**2)

        # Compute the integrals
        # Because there is 4 walls
        # Start in top right corner
        integrals = [0, 0]
        for j in range(4):
            initial_values = moment_of_inertia.initial_values(cur_Span_Loc)

            if j%2 == 0:
                ds = initial_values[2]/np.cos(initial_values[1])
                x = 0
                if j == 0:
                    y = initial_values[4]/2 + np.sin(initial_values[1])*ds
                else:
                    y = -(initial_values[4]/2 + np.sin(initial_values[1]) * ds)
            elif j == 1:
                ds = initial_values[3]
                y = 0
                x = -initial_values[2]/2
            else:
                ds = initial_values[4]
                y = 0
                x = initial_values[2] / 2

            integrals[0] += initial_values[0]*y*ds
            integrals[1] += initial_values[0]*x*ds

        shear_flow_basic = c1*integrals[0] + c2*integrals[1]
        shear_b_Ar.append(shear_flow_basic)

        # Compute the constant shear flow