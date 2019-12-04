from VectorlistLiftplane import *
from VectorlistDragplane import *
from internal_force_calculations import *

#Lift plane
positions_lift, forces_lift = Liftplaneforce()
pos_list_lift, sh_load_lift, bend_mom_lift = int_load(forces_lift, positions_lift)
bend_mom_lift = [-i for i in bend_mom_lift]

#Drag plane
positions_drag, forces_drag = Dragplaneforce()
pos_list_drag, sh_load_drag, bend_mom_drag = int_load(forces_drag, positions_drag)
sh_load_drag = [-i for i in sh_load_drag]

b_2 = 28.74


# Use this only from 0 until 27.14 [m] !!!!
def internal_moments(span_position):    #Adjust the signs!!!

    # Lift
    if span_position > pos_list_lift[0] and span_position < pos_list_lift[-1]:
        count_lift = 0
        for i in range(len(pos_list_lift)):
            if pos_list_lift[i] > span_position and count_lift == 0:
                bend_lift = bend_mom_lift[i]
                count_lift += 1

    elif span_position==pos_list_lift[0]:
        bend_lift = bend_mom_lift[0]
    elif span_position==pos_list_lift[-1]:
        bend_lift= bend_mom_lift[-1]
    else:
        print("Lift value out of boundary")

    # Drag
    if span_position > pos_list_drag[0] and span_position < pos_list_drag[-1]:
        count_drag = 0
        for i in range(len(pos_list_drag)):
            if pos_list_drag[i] > span_position and count_drag == 0:
                bend_drag = bend_mom_drag[i]
                count_drag += 1

    elif span_position==pos_list_drag[0]:
        bend_drag = bend_mom_drag[0]
    elif span_position==pos_list_drag[-1]:
        bend_drag= bend_mom_drag[-1]
    else:
        print("Drag value out of boundary")


    return bend_lift, bend_drag
