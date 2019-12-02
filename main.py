from VectorlistLiftplane import *
from VectorlistDragplane import *
from internal_force_calculations import *
from graph import *
from ToverTheta import *
from moment_of_inertia import *
from newT import *

"""
# Include all functions
import WingLoadFunction

xAr, zAr, M_Y = WingLoadFunction.WingLoad(massFuel=104790*0.588, accuracy=10000)

# optionally print the result
plt.plot(xAr, zAr, xAr, M_Y)
plt.show()


# Analysing the wingbox on the x-z plane
positions_xz, forces_xz = Liftplaneforce()
pos_list_xz, sh_load_xz, bend_mom_xz = int_load(forces_xz, positions_xz)
bend_mom_xz = [-i for i in bend_mom_xz]
force_diagrams("Internal force diagrams in the lift-plane: 3.75 g's", sh_load_xz, pos_list_xz, bend_mom_xz)


# Analysing the wingbox on the y-z plane
positions_yz, forces_yz = Dragplaneforce()
pos_list_yz, sh_load_yz, bend_mom_yz = int_load(forces_yz, positions_yz)
sh_load_yz = [-i for i in sh_load_yz]
force_diagrams("Internal force diagrams in the drag-plane", sh_load_yz, pos_list_yz, bend_mom_yz)
"""


# Plot cross section
plot_cross_section(0)
# Plot twist values
#TandTheta()
#newT()

# Print total mass
print("Wingbox weighs " + str(round(mass())) + " kg")