from moment_of_inertia import *
from internal_forces import *
from math import *
import numpy as np
import matplotlib.pyplot as plt

#Program that calculates the normal bending stress in the wing box along the span of the wing
#It only calculates the stress in the point the furthest away from the neutral axis, which is going to be
#one of the corner point of the wing box

def NAangle(span_position):
    y = M_y*I_xx-M_x*I_xy
    x = M_x*I_yy-M_y*I_xy
    alpha = atan2(-y,x)
    return alpha*180/pi

b = 28.74
dz = 0.1
z = 0.1

M_x, M_y = internal_moments(z)
I_xx, I_yy, I_xy = MOI(z)
width, frontheight, rearheight = initial_values(z)[2:5]
centroidx, centroidy = centroid(z)

x1, y1  = 0.5*width+centroidx, 0.5*rearheight-centroidy
x2, y2 =  0.5*width-centroidx, 0.5*rearheight-centroidy
x3, y3 =  0.5*width-centroidx, 0.5*rearheight+centroidy
x4, y4 =  0.5*width+centroidx, 0.5*rearheight+centroidy

sigma1tab = []
sigma2tab = []
sigma3tab = []
sigma4tab = []
alphatab = []
ztab = []
M_xtab = []
M_ytab = []

while z<= b:
    sigma1 = ((M_x*I_yy-M_y*I_xy)*y1+(M_y*I_xx-M_x*I_xy)*x1)/(I_xx*I_yy-I_xy**2)
    sigma2 = ((M_x*I_yy-M_y*I_xy)*y2+(M_y*I_xx-M_x*I_xy)*x2)/(I_xx*I_yy-I_xy**2)
    sigma3 = ((M_x*I_yy-M_y*I_xy)*y3+(M_y*I_xx-M_x*I_xy)*x3)/(I_xx*I_yy-I_xy**2)
    sigma4 = ((M_x*I_yy-M_y*I_xy)*y4+(M_y*I_xx-M_x*I_xy)*x4)/(I_xx*I_yy-I_xy**2)

    alphatab.append(NAangle(z))
    ztab.append(z)
    sigma1tab.append(sigma1)
    sigma2tab.append(sigma2)
    sigma3tab.append(sigma3)
    sigma4tab.append(sigma4)
    M_xtab.append(M_x)
    M_ytab.append(M_y)

    z = z+dz
    M_x, M_y = internal_moments(z)
    I_xx, I_yy, I_xy = MOI(z)
    width, frontheight, rearheight = initial_values(z)[2:5]
    centroidx, centroidy = centroid(z)
    x1, y1 = 0.5 * width + centroidx, 0.5 * rearheight - centroidy
    x2, y2 = 0.5 * width - centroidx, 0.5 * rearheight - centroidy
    x3, y3 = 0.5 * width - centroidx, 0.5 * rearheight + centroidy
    x4, y4 = 0.5 * width + centroidx, 0.5 * rearheight + centroidy

"""
plt.plot(ztab,alphatab)
plt.xlabel('Spanwise position')
plt.ylabel('NA angle')

plt.plot(ztab,sigma1tab)
plt.xlabel('Spanwise position')
plt.ylabel('Stress in point 1')

plt.plot(ztab,sigma2tab)
plt.xlabel('Spanwise position')
plt.ylabel('Stress in point 2')

plt.plot(ztab,sigma3tab)
plt.xlabel('Spanwise position')
plt.ylabel('Stress in point 3')

plt.plot(ztab,sigma4tab)
plt.xlabel('Spanwise position')
plt.ylabel('Stress in point 4')
plt.show()

plt.plot(ztab, M_xtab)
plt.xlabel('Spanwise position')
plt.ylabel('x-moment')
plt.show()
"""

plt.plot(ztab, M_ytab)
plt.xlabel('Spanwise position')
plt.ylabel('y-moment')
plt.show()

