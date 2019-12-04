from VectorlistLiftplane import *
from VectorlistDragplane import *
from internal_force_calculations import *
from matplotlib import pyplot as plt

#Lift plane
positions_lift, forces_lift = Liftplaneforce()
pos_list_lift, sh_load_lift, bend_mom_lift = int_load(forces_lift, positions_lift)

#Drag plane
positions_drag, forces_drag = Dragplaneforce()
pos_list_drag, sh_load_drag, bend_mom_drag = int_load(forces_drag, positions_drag)

b_2 = 28.74

def internal_moments(span_position):    #Adjust the signs!!!

    #Lift
    count_lift = 0
    for i in range(len(positions_lift)):
        if span_position > positions_lift[i] and count_lift == 0:
            count_lift += 1
            bend_lift = bend_mom_lift[i]
    if count_lift == 0:
        bend_lift = 0
        print(str(span_position) +" is outside of the span positions available for bending in the lift plane")

    # Drag
    count_drag = 0
    for i in range(len(positions_drag)):
        if span_position < positions_drag[i] and count_drag == 0:
            count_drag += 1
            bend_drag = bend_mom_drag[i]
    if count_drag == 0:
        bend_drag = 0
        print(str(span_position) + " is outside of the span positions available for bending in the drag plane")

    return bend_lift, bend_drag

"""
M_lift_tab, M_drag_tab = [], []
x_drag, x_lift = [], []
for i in range(len(bend_mom_drag)):
    M_drag_tab.append(bend_mom_drag[i])
    x_drag.append(pos_list_drag[i])

for i in range(len(bend_mom_lift)):
    M_lift_tab.append(bend_mom_lift[i])
    x_lift.append(pos_list_lift[i])

plt.title("Drag bending moment")
plt.plot(x_drag, M_drag_tab)
plt.show()

plt.title("Lift bending moment")
plt.plot(x_lift, M_lift_tab)
plt.show()
"""
