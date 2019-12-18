from math import *
import matplotlib.pyplot as plt
from moment_of_inertia import *
from internal_moments import *
import matplotlib.lines


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
sigmayield = 414

sigma1tab, sigma2tab, sigma3tab, sigma4tab = [], [], [], []
alphatab, ztab, ztab1, ztab2, ztab3, ztab4, M_xtab, M_ytab = [], [], [], [], [], [], [], []
I_xxtab, I_yytab, I_xytab = [], [], []

CRITICALTAB = []

while z<= b:
    sigma1, sigma2, sigma3, sigma4 = Normalstress(z)
    M_x, M_y = internal_moments(z)
    I_xx, I_yy, I_xy = MOI(z)
    
    alphatab.append(NAangle(z))
    sigma1margin = sigmayield/(sigma1/10**6)
    sigma2margin = sigmayield/(sigma2/10**6)
    sigma3margin = sigmayield/(sigma3/10**6)
    sigma4margin = sigmayield/(sigma4/10**6)
    if abs(sigma1/10**6) >= 1:
        sigma1tab.append(sigma1margin)
        ztab1.append(z)    
    
    if abs(sigma2/10**6) >= 1:
        sigma2tab.append(sigma2margin)
        ztab2.append(z)
    if abs(sigma3/10**6) >= 1:
        sigma3tab.append(sigma3margin)
        ztab3.append(z)
    if abs(sigma4/10**6) >= 1:
        sigma4tab.append(sigma4margin)
        ztab4.append(z)

    if max(sigma1, sigma2, sigma3, sigma4) > 15*10**6:
        ztab.append(z)
        if abs(sigma4margin) <= abs(sigma3margin):
            CRITICALTAB.append(sigma4margin)
        elif abs(sigma4margin) >= abs(sigma3margin):
            CRITICALTAB.append(sigma3margin)
        
    M_xtab.append(M_x)
    M_ytab.append(M_y)
    I_xxtab.append(I_xx)
    I_yytab.append(I_yy)
    I_xytab.append(I_xy)

    z = z+dz

plt.minorticks_on()
plt.grid(b=True, which='major', color='#bebebe', linestyle='-')
plt.grid(b=True, which='minor', color='#e9e9e9', linestyle='-', linewidth = 0.5)
plt.plot(ztab, CRITICALTAB, label = 'Critical margin of safety')
plt.xlabel('Spanwise position [m]')
plt.ylabel('Margin of Safety')
plt.show()
    

plt.minorticks_on()
plt.grid(b=True, which='major', color='#bebebe', linestyle='-')
plt.grid(b=True, which='minor', color='#e9e9e9', linestyle='-', linewidth = 0.5)

plt.plot(ztab1,sigma1tab, label = 'point 1', linestyle = 'solid')

plt.plot(ztab2,sigma2tab, label = 'point 2', linestyle = 'dashed')

plt.plot(ztab3,sigma3tab, label = 'point 3', linestyle = 'dotted')

plt.plot(ztab4,sigma4tab, label = 'point 4', linestyle = 'dashdot')

plt.xlabel('Spanwise position [m]')
plt.ylabel('Margin of Safety')
plt.legend()

plt.show()


