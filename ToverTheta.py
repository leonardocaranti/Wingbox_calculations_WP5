from math import *
from matplotlib import pyplot as plt
from moment_of_inertia import *
from LiftDistribution import *

L = 28.74 	#[m]
fus_diam = 6.01 #[m]

def TandTheta():
    from AeroMomentDistribution import Momentvectors
    from torsionalstiffnesscoefficient import torsionalstiffness

    s_factor = 1.1

    # Internal torque distribution
    (x, y) = Momentvectors()

    y = [b*s_factor for b in y]

    summationtorques, t_over_theta = [], []
    totaltorque = sum(y)
    span_tab, t_stiffness_tab = torsionalstiffness()
    Theta_tab, t_theta_tab = [], []
    t_dz, t_theta = 0, 0
    Theta = 0
    for i in range(len(y)):
        summationtorques.append(totaltorque - y[i])

        if i == 0:
            t_dz = 0

        else:
            t_dz += (totaltorque - y[i]) * (x[i] - x[i - 1])

        # Twist distribution over the span
        Theta = t_dz * (t_stiffness_tab[i])
        Theta_tab.append(Theta*180/pi)
        """

        if i==0:
            Theta += 0
        else:
            Theta += t_stiffness_tab[i]*(totaltorque - y[i]) * (x[i] - x[i - 1])

        Theta_tab.append(Theta * 180 / pi)
        """

        if Theta == 0:
            t_over_theta.append(0)

        if not Theta ==0:
            t_over_theta.append((totaltorque - y[i])/Theta)

        totaltorque = totaltorque - y[i]


    x_from_fus, t_over_theta_from_fus = [], []
    for i in range(len(x)):
        if x[i] > fus_diam:
            x_from_fus.append(x[i])
            t_over_theta_from_fus.append(t_over_theta[i])

    t_stiffness_tab = [1/t for t in t_stiffness_tab]


    print(span_tab)

    plt.plot(span_tab, t_stiffness_tab)
    plt.suptitle("Torsional stiffness per unit length distribution: " + str(maxload) + " g's")
    plt.xlabel("Spanwise location from root [m]")
    plt.ylabel("Torsional stiffness per unit length [Nm/(rad/m)]")
    plt.grid()
    if abs(max(t_stiffness_tab))>abs(min(t_stiffness_tab)):
        crit_val = max(t_stiffness_tab)
    else:
        crit_val = min(t_stiffness_tab)
    ind = t_stiffness_tab.index(crit_val)
    plt.axhline(y=crit_val, lw=1, ls='dashed', color='#d62728')
    plt.text(span_tab[ind], crit_val, str(round(crit_val)) + " [Nm/(rad/m)]")
    plt.show()

    plt.plot(x_from_fus, t_over_theta_from_fus)
    plt.title("Torsional stiffness distribution from the fuselage")
    plt.xlabel("Spanwise location from root (fuselage integration) [m]")
    plt.ylabel("Torsional stiffness [Nm/rad]")
    plt.grid()
    if abs(max(t_over_theta_from_fus))>abs(min(t_over_theta_from_fus)):
        crit_val = max(t_over_theta_from_fus)
    else:
        crit_val = min(t_over_theta_from_fus)
    ind = t_over_theta_from_fus.index(crit_val)
    plt.axhline(y=crit_val, lw=1, ls='dashed', color='#d62728')
    plt.text(x_from_fus[ind], crit_val, str(round(crit_val)) + " [Nm/rad]")
    plt.show()

    plt.title("Angle of twist distribution")
    plt.plot(x, Theta_tab)
    plt.xlabel("Spanwise location from root [m]")
    plt.ylabel("Angle of twist [deg]")
    plt.grid()
    if abs(max(Theta_tab))>abs(min(Theta_tab)):
        crit_val = max(Theta_tab)
    else:
        crit_val = min(Theta_tab)
    ind = Theta_tab.index(crit_val)
    plt.axhline(y=crit_val, lw=1, ls='dashed', color='#d62728')
    plt.text(x[ind], crit_val, str(round(crit_val, 3)) + " [deg]")
    plt.show()


    """
    # Plots
    plt.title("Internal Torque Distribution: 3.75 g's")
    plt.plot(x, summationtorques)
    plt.xlabel("Spanwise location from root [m]")
    plt.ylabel("Internal torque [Nm]")
    plt.grid()
    if abs(max(summationtorques)) > abs(min(summationtorques)):
        crit_val = max(summationtorques)
    else:
        crit_val = min(summationtorques)
    ind = summationtorques.index(crit_val)
    plt.axhline(y=crit_val, lw=1, ls='dashed', color='#d62728')
    plt.text(x[ind], crit_val, str(round(crit_val)) + " [Nm]")
    plt.show()
    """

#TandTheta()