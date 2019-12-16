from math import *
import numpy as np
from matplotlib import pyplot as plt
from moment_of_inertia import *
from internal_moments import *


def columnbuckling(span_position):
    elements = cross_section(cross_section_value,span_position)
    element = elements[-1]
    I_xx, area = element.moi_xx, element.area

    critical_force = (K*pi**2*E*I_xx)/L**2

    return critical_force/area

def skinbuckling(span_position):
    skin_thickness, WB_angle, WB_vertical_distance = initial_values(z)[0:3]
    width = WB_vertical_distance/cos(WB_angle)
    spacing = width/(no_stringers_top-1)

    skinbuckling_stress = (((pi**2*k_c*E)/(12*(1-poisson**2)))*(skin_thickness/spacing)**2)

    return skinbuckling_stress

def Normalstress(span_position):
    M_x, M_y = internal_moments(z)
    I_xx, I_yy, I_xy = MOI(z)
    width, frontheight, rearheight = initial_values(z)[2:5]
    centroidx, centroidy = centroid(z)

    x1, y1 = -0.5 * width - centroidx, 0.5 * rearheight - centroidy
    x2, y2 = 0.5 * width - centroidx, 0.5 * frontheight - centroidy
    x3, y3 = 0.5 * width - centroidx, -0.5 * frontheight - centroidy
    x4, y4 = -0.5 * width - centroidx, -0.5 * rearheight - centroidy

    sigma1 = ((M_x * I_yy - M_y * I_xy) * y1 + (M_y * I_xx - M_x * I_xy) * x1) / (I_xx * I_yy - I_xy ** 2)
    sigma2 = ((M_x * I_yy - M_y * I_xy) * y2 + (M_y * I_xx - M_x * I_xy) * x2) / (I_xx * I_yy - I_xy ** 2)
    sigma3 = ((M_x * I_yy - M_y * I_xy) * y3 + (M_y * I_xx - M_x * I_xy) * x3) / (I_xx * I_yy - I_xy ** 2)
    sigma4 = ((M_x * I_yy - M_y * I_xy) * y4 + (M_y * I_xx - M_x * I_xy) * x4) / (I_xx * I_yy - I_xy ** 2)

    return -sigma1/10**6, -sigma2/10**6, -sigma3/10**6, -sigma4/10**6


E = 71.7*10**9
b = 27.14
L = 5
poisson = 0.33
K = 4
k_c = 5 #7.43

z = 0
dz = 0.1

skinbucklingtab, columnbucklingtab, ztab = [], [], []
sigma1tab, sigma2tab, sigma3tab, sigma4tab = [],[],[],[]

while z <=b:
    stress1, stress2, stress3, stress4 = Normalstress(z)
    column_buckling_load = columnbuckling(z)
    skin_buckling_stress = skinbuckling(z)

    z = z+dz

    columnbucklingtab.append(column_buckling_load/10**6)
    skinbucklingtab.append(skin_buckling_stress/10**6)
    ztab.append(z)
    sigma1tab.append(stress1)
    sigma2tab.append(stress2)
    sigma3tab.append(stress3)
    sigma4tab.append(stress4)

print('Wing box mass:', mass(), 'kg')
print('Lowest column buckling stress:', min(columnbucklingtab), 'MPa')
print('Lowest skin buckling stress:', min(skinbucklingtab), 'MPa')
print('Maximum encountered stress:', min(min(sigma1tab), min(sigma2tab), min(sigma3tab), min(sigma4tab)), 'MPa')
print('Stringer type:', stringer_type)


"""
plt.subplot(221)
plt.plot(ztab, columnbucklingtab)
plt.xlabel('Spanwise position')
plt.ylabel('Column Buckling Stress [MPa]')
plt.ylim(0,max(columnbucklingtab)*1.5)

plt.subplot(222)
plt.plot(ztab, skinbucklingtab)
plt.xlabel('Spanwise position')
plt.ylabel('Skin Buckling Stress [MPa]')

plt.show()
"""