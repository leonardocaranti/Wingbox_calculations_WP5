from moment_of_inertia import *
from AeroMomentDistribution import Momentvectors
from matplotlib import pyplot as plt

L = 28.74 	#[m]
G = 28000000000
fus_diam = 6.01 #[m]

def newT():

    t_theta = []
    s_factor = 1.1
    (x, y) = Momentvectors()
    y = [b*s_factor for b in y]

    summationtorques, theta_tab, theta = [], [], 0
    totaltorque = sum(y)

    #Torque and twist angle
    for i in range(len(y)):

        T = totaltorque - y[i]
        summationtorques.append(T)
        if i == 0:
            theta = 0
        else:
            theta += T/(G*J(x[i]))*(x[i]-x[i-1])
        theta_tab.append(theta*180/pi)

        t_theta.append(G*J(x[i]))

        totaltorque = T

    #T/theta
    t_over_theta_tab, x_fus = [], []
    for i in range(len(y)):
        if x[i]>fus_diam/2:
            x_fus.append(x[i])
            t_over_theta_tab.append(summationtorques[i]/theta_tab[i])

    plt.title("Twist angle distribution")
    plt.plot(x, theta_tab)
    plt.xlabel("Spanwise location from root [m]")
    plt.ylabel("Twist angle [deg]")
    plt.grid()
    if abs(max(theta_tab))>abs(min(theta_tab)):
        crit_val = max(theta_tab)
    else:
        crit_val = min(theta_tab)
    ind = theta_tab.index(crit_val)
    plt.axhline(y=crit_val, lw=1, ls='dashed', color='#d62728')
    plt.text(x[ind], crit_val, str(round(crit_val, 3)) + " [deg]")
    plt.show()

newT()