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

        MoI = moment_of_inertia.MOI(cur_Span_Loc) # xx-yy-xy

        # Compute the constants
        #MoI[2] = 0  # Ixy
        c1 = -(V_z*MoI[1]-V_x*MoI[2])/(MoI[0]*MoI[1]-MoI[2]**2) # stuff before the first and second integral
        c2 = -(V_x*MoI[0]-V_z*MoI[2])/(MoI[0]*MoI[1]-MoI[2]**2)

        # Get the wing box dimensions at a certain span wise location
        initial_values = moment_of_inertia.initial_values(cur_Span_Loc)

        # Compute the integrals
        # Because there is 4 walls only iterate to 4
        # Start in top right corner
        integrals = [0, 0]

        # TODO Change initial_values[4] to [3] in case you switch the lift to be negative lift
        #y = -initial_values[4]/2
        y = -initial_values[3] / 2
        ytab = []
        shear_flow_Ar = []
        while y <= initial_values[3]/2:
            #Q_x = initial_values[0]*initial_values[4]*initial_values[2]/4 + initial_values[0] * (initial_values[4]/2 - y) * (y+(initial_values[4]/2 - y)/2)
            Q_y = -initial_values[0] * y * initial_values[2]/2

            Q_x = initial_values[0] * initial_values[3] * initial_values[2] / 4 + initial_values[0] * (
                        initial_values[3] / 2 - y) * (y + (initial_values[3] / 2 - y) / 2)

            shear_flow_lift = c1*Q_x
            shear_flow_drag = c2*Q_y
            shear_flow_bending = bend_mom_yz[i]/(2*moment_of_inertia.local_area(cur_Span_Loc))

            shear_flow_Ar.append(shear_flow_bending+shear_flow_drag+shear_flow_lift)


            y += .001
            ytab.append(y)

        shear_stress_Ar.append(max(shear_flow_Ar)/initial_values[0]*10**-6)

        if i%40 == 0:
            print("Shear progress: " + str(i + 1) + "/" + str(len(pos_list_yz)) + " | " + str(
            round((i + 1) * 100 / (len(pos_list_yz)), 2)) + "%")

    plt.plot(pos_list_yz, shear_stress_Ar)
    plt.grid()
    plt.xlabel("Span [m]")
    plt.ylabel("Shear Stress [MPa]")
    plt.axhline(y=shear_stress_Ar[0], lw=1, ls='dashed', color='#d62728')
    plt.show()
    return shear_stress_Ar