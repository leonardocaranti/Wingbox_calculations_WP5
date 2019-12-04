import moment_of_inertia
import numpy as np
import matplotlib.pyplot as plt

def ShearStress(pos_list_xz, sh_load_xz, pos_list_yz, sh_load_yz, bend_mom_xz, bend_mom_yz):

    shear_stress_Ar = []

    # loop through the span locations
    for i in range(len(pos_list_yz)):
        # Get const values
        cur_Span_Loc = pos_list_yz[i]
        V_z = -sh_load_xz[i]    # Correct the sign
        V_x = sh_load_yz[i]

        MoI = np.asarray(moment_of_inertia.MOI(cur_Span_Loc)) # xx-yy-xy

        # Compute the constants
        #MoI[2] = 0  # Ixy
        c1 = -(V_z*MoI[1]-V_x*MoI[2])/(MoI[0]*MoI[1]-MoI[2]**2) # stuff before the first and second integral
        c2 = -(V_x*MoI[0]-V_z*MoI[2])/(MoI[0]*MoI[1]-MoI[2]**2)

        # Get the wing box dimensions at a certain span wise location
        initial_values = moment_of_inertia.initial_values(cur_Span_Loc)

        # TODO Add effect of torque
        # Bredts formula q = T/2A


        # Compute the integrals
        # Because there is 4 walls only iterate to 4
        # Start in top right corner
        integrals = [0, 0]
        for j in range(4):
            if j%2 == 0:
                # For the angled plates
                ds = initial_values[2]/np.cos(initial_values[1])
                x = 0
                if j == 0:
                    y = initial_values[4]/2 + np.sin(initial_values[1])*ds
                else:
                    y = -(initial_values[4]/2 + np.sin(initial_values[1]) * ds)
            elif j == 1:
                # For the left plate
                ds = initial_values[3]
                y = 0
                x = initial_values[2]/2
            else:
                # For the right plate
                ds = initial_values[4]
                y = 0
                x = -initial_values[2] / 2

            # Calculate both integrals
            integrals[0] += initial_values[0]*y*ds
            integrals[1] += initial_values[0]*x*ds

        shear_flow_basic = c1*integrals[0] + c2*integrals[1]

        shear_constant = bend_mom_xz[i]/(2*moment_of_inertia.local_area(cur_Span_Loc))

        shear_stress = (shear_flow_basic + shear_constant)/initial_values[0]
        shear_stress_Ar.append(shear_stress*10**-6) # q/t = tau, convert from Pa to MPa

    plt.plot(pos_list_yz, shear_stress_Ar)
    plt.xlabel("Span [m]")
    plt.ylabel("Shear Stress [MPa]")
    plt.show()

    return shear_stress_Ar