#TORSIONAL STIFFNESS COEFFICIENT

from math import *
from matplotlib import pyplot as plt
import numpy as np
from moment_of_inertia import *

G = 28000000000

def torsionalstiffness():
        span_tab = []
        t_stiffness_tab = []
        for span_position in np.arange(0,b_2,0.01):

                t, theta, dist, front_spar_h, rear_spar_h, stringer_height, stringer_thickness = initial_values(span_position)

                A_m = ((rear_spar_h+front_spar_h)/2)*dist
                intdst = front_spar_h/t + rear_spar_h/t + (sqrt(((front_spar_h - rear_spar_h)/2)**2 + (dist*dist))*2)/t
                t_stiffness = (intdst)/(4*A_m*A_m*G)
                span_tab.append(span_position)
                t_stiffness_tab.append(t_stiffness)

        return span_tab, t_stiffness_tab



