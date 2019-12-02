from scipy import integrate
from moment_of_inertia import *
from AeroMomentDistribution import Momentvectors
from matplotlib import pyplot as plt

L = 28.74 	#[m]
G = 28000000000


def newT2():
    s_factor = 1.1
    (x, y) = Momentvectors()
    y = [b*s_factor for b in y]
    summationtorques, totaltorque = [], sum(y)
    theta_tab = []

    for i in range(len(y)):
        Tor = totaltorque - y[i]
        summationtorques.append(Tor)
        totaltorque = Tor


    def T(span_pos):
        for i in range(len(x)):
            if x[i] < span_pos:
                crit_T = summationtorques[i]
            else:
                crit_T = 0
        return crit_T

    def theta(span_pos):
        integ = integrate.quad(lambda span_pos: (T(span_pos) / (G * J(span_pos))), 0, span_pos)
        return integ[0]

    for i in range(len(y)):
        theta_tab.append(theta(x[i])*180/pi)

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

newT2()