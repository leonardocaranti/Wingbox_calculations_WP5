from VectorlistLiftplane import *
from VectorlistDragplane import *
from internal_force_calculations import *

#Lift plane
positions_lift, forces_lift = Liftplaneforce()
pos_list_lift, sh_load_lift, bend_mom_lift = int_load(forces_lift, positions_lift)

#Drag plane
positions_drag, forces_drag = Dragplaneforce()
pos_list_drag, sh_load_drag, bend_mom_drag = int_load(forces_drag, positions_drag)

def internal_moments():
    return bend_mom_lift, bend_mom_drag