import moment_of_inertia
import numpy as np
import matplotlib.pyplot as plt

def ShearStress(pos_list_xz, sh_load_xz, pos_list_yz, sh_load_yz, bend_mom_xz, bend_mom_yz):

    shear_stress_Ar = []
    shear_stress_min_array = []

    shear_stress_Ar_FS = []
    shear_stress_min_array_FS = []

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
        # TODO Change initial_values[4] to [3] in case you switch the lift to be negative lift

        #y = -initial_values[4]/2
        y = -initial_values[3] / 2
        ytab = []
        shear_flow_Ar = []
        shear_flow_Ar_FS = []
        while y <= initial_values[3]/2:

            Q_x = initial_values[0] * initial_values[3] * initial_values[2] / 4 + initial_values[0] * (initial_values[3] / 2 - y) * (y + (initial_values[3] / 2 - y) / 2)
            Q_y = -initial_values[0] * y * initial_values[2]/2

            shear_flow_lift = c1*Q_x
            shear_flow_drag = c2*Q_y
            shear_flow_bending = bend_mom_yz[i]/(2*moment_of_inertia.local_area(cur_Span_Loc))

            shear_flow_Ar.append(shear_flow_bending+shear_flow_drag+shear_flow_lift)

            y += .001
            ytab.append(y)

        y = -initial_values[4] / 2
        while y <= initial_values[4]/2:
            Q_y = initial_values[0] * y * initial_values[2]/2
            Q_x_FS = initial_values[0] * initial_values[4] * initial_values[2] / 4 + initial_values[0] * (
                        initial_values[4] / 2 - y) * (y + (initial_values[4] / 2 - y) / 2)

            shear_flow_lift_FS = c1*Q_x_FS
            shear_flow_drag = c2*Q_y
            shear_flow_bending = bend_mom_yz[i]/(2*moment_of_inertia.local_area(cur_Span_Loc))
            shear_flow_Ar_FS.append(shear_flow_bending+shear_flow_drag+shear_flow_lift_FS)

            y += .001


        shear_stress_Ar.append(max(shear_flow_Ar)/initial_values[0]*10**-6)
        shear_stress_min_array.append(min(shear_flow_Ar)/initial_values[0]*10**-6)

        shear_stress_Ar_FS.append(max(shear_flow_Ar_FS)/initial_values[0]*10**-6)
        shear_stress_min_array_FS.append(min(shear_flow_Ar_FS)/initial_values[0]*10**-6)

        if i%50 == 0:
            print("Shear stress progress: " + str(i + 1) + "/" + str(len(pos_list_yz)) + " | " + str(
            round((i + 1) * 100 / (len(pos_list_yz)), 2)) + "%")

    plt.subplot(211)
    plt.plot(pos_list_yz, shear_stress_Ar, label="Maximum shear stress rear spar", marker="*", markevery=50, markersize=7)
    plt.plot(pos_list_yz, shear_stress_min_array, label="Minimum shear stress rear spar", marker="v", markevery=50, markersize=7)
    plt.grid()
    plt.legend()
    plt.ylabel("Shear Stress [MPa]")
    plt.title("Shear stress distribution over the span")

    plt.subplot(212)
    plt.plot(pos_list_yz, shear_stress_Ar_FS, label="Max shear stress front spar", marker="*", markevery=50, markersize=7)
    plt.plot(pos_list_yz, shear_stress_min_array_FS, label="Min shear stress front spar", marker="v", markevery=50, markersize=7)
    plt.grid()
    plt.legend()
    plt.xlabel("Span [m]")
    plt.ylabel("Shear Stress [MPa]")
    plt.show()

    # Calculate the critical shear stress
    def tCrit(k, E, t, b, v):
        return (np.pi ** 2 * k * E * (t / b) ** 2) / (12 * (1 - v ** 2))

    k = 9.5
    E = 71.7 * 10 ** 9  # Pa
    initial_values = moment_of_inertia.initial_values(0)
    tCritvalFS = tCrit(k, E, initial_values[0], initial_values[3], 0.32)
    tCritvalRS = tCrit(k, E, initial_values[0], initial_values[4], 0.32)
    print("Tcrit FS= " + str(tCritvalFS * 10 ** -6))
    print("Tcrit RS= " + str(tCritvalRS * 10 ** -6))

    print("halfspan: " + str(pos_list_yz[-1]) + " average height: " + str(moment_of_inertia.initial_values(pos_list_yz[int(len(pos_list_yz)/2)])[3]))
    critStress = tCrit(k, E, moment_of_inertia.initial_values(pos_list_yz[int(len(pos_list_yz)/2)])[0], moment_of_inertia.initial_values(pos_list_yz[int(len(pos_list_yz)/2)])[3], 0.32)
    print("critical stress: " + str(critStress))
    # Get amount of stiffiners required
    stiffiners = 0
    for i in range(len(pos_list_yz)):
        aspectRat = (pos_list_yz[-1]/(stiffiners+1))/moment_of_inertia.initial_values(pos_list_yz[i])[4]    #a/b
        if aspectRat <= 5:
            print(str(stiffiners) + " Stiffiners required for an AR of: " + str(aspectRat))
            break
        stiffiners += 1

    return [[shear_stress_Ar,shear_stress_min_array],[shear_stress_Ar_FS, shear_stress_min_array_FS]]