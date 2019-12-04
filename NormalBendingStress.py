from math import *
import matplotlib.pyplot as plt
from moment_of_inertia import *
from internal_moments import *

def NAangle(span_position):
    M_x, M_y = internal_moments(z)
    I_xx, I_yy, I_xy = MOI(z)

    y = M_y*I_xx-M_x*I_xy
    x = M_x*I_yy-M_y*I_xy
    alpha = atan2(y,x)

    return alpha*180/pi

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

    return -sigma1, -sigma2, -sigma3, -sigma4

b = 27.14
dz = 0.1
z = 0.1

sigma1tab, sigma2tab, sigma3tab, sigma4tab = [], [], [], []
alphatab, ztab, M_xtab, M_ytab = [], [], [], []
I_xxtab, I_yytab, I_xytab = [], [], []

while z<= b:
    sigma1, sigma2, sigma3, sigma4 = Normalstress(z)
    M_x, M_y = internal_moments(z)
    I_xx, I_yy, I_xy = MOI(z)

    alphatab.append(NAangle(z))
    ztab.append(z)
    sigma1tab.append(sigma1/10**6)
    sigma2tab.append(sigma2/10**6)
    sigma3tab.append(sigma3/10**6)
    sigma4tab.append(sigma4/10**6)
    M_xtab.append(M_x)
    M_ytab.append(M_y)
    I_xxtab.append(I_xx)
    I_yytab.append(I_yy)
    I_xytab.append(I_xy)

    z = z+dz

plt.subplot(121)
plt.title('Normal stress in points furthest away from neutral axis')
plt.plot(ztab,sigma1tab, label ='point 1')
plt.plot(ztab,sigma2tab, label = 'point 2')
plt.plot(ztab,sigma3tab, label = 'point 3')
plt.plot(ztab,sigma4tab, label = 'point 4')
plt.xlabel('Spanwise position [m]')
plt.ylabel('Stress [MPa]')
plt.legend()

plt.subplot(122)
plt.plot(ztab,alphatab)
plt.xlabel('Spanwise position [m]')
plt.ylabel('NA angle [deg]')

plt.show()

"""
plt.plot(ztab, M_xtab)
plt.xlabel('Spanwise position')
plt.ylabel('x-moment')

plt.plot(ztab, M_ytab)
plt.xlabel('Spanwise position')
plt.ylabel('y-moment')

plt.plot(ztab,I_xxtab)
plt.xlabel('Spanwise position')
plt.ylabel('MOI xx')

plt.plot(ztab,I_yytab)
plt.xlabel('Spanwise position')
plt.ylabel('MOI yy')

plt.plot(ztab,I_xytab)
plt.xlabel('Spanwise position')
plt.ylabel('MOI xy')

plt.plot(ztab,alphatab)
plt.xlabel('Spanwise position')
plt.ylabel('NA angle')
"""


