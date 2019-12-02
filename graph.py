#graph calculation

import matplotlib.pyplot as plt

def force_diagrams(graph_name, force, xspan, moment=0):

    plt.suptitle(graph_name)

    plt.subplot(121)
    plt.plot(xspan,force)
    plt.title("Shear force diagram")
    plt.xlabel("Spanwise location from root [m]")
    plt.ylabel("Shear force [N]")
    plt.grid()
    if abs(max(force))>abs(min(force)):
        crit_val = max(force)
    else:
        crit_val = min(force)
    ind = force.index(crit_val)
    plt.axhline(y=crit_val, lw=1 ,ls='dashed' ,color='#d62728')
    plt.text(xspan[ind], crit_val, str(round(crit_val)) + " [N]")

    if not moment == 0:
        plt.subplot(122)
        plt.plot(xspan,moment)
        plt.title("Bending moment diagram")
        plt.xlabel("Spanwise location from root [m]")
        plt.ylabel("Bending moment [Nm]")
        plt.grid()
        if abs(max(moment)) > abs(min(moment)):
            crit_val = max(moment)
        else:
            crit_val = min(moment)
        ind = moment.index(crit_val)
        plt.axhline(y=crit_val, lw=1 ,ls='dashed' ,color='#d62728')
        plt.text(xspan[ind], crit_val, str(round(crit_val)) + " [Nm]")

    plt.show()