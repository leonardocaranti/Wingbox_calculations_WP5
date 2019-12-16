from math import *
from moment_of_inertia import *
from internal_moments import *

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

criticalstresstabtension, criticalstresstabcompression = [], []
alphatab, ztab, M_xtab, M_ytab = [], [], [], []

while z<= b:
    sigma1, sigma2, sigma3, sigma4 = Normalstress(z)
    M_x, M_y = internal_moments(z)
    I_xx, I_yy, I_xy = MOI(z)

    ztab.append(z)

    criticalcompressionstress = min(sigma1, sigma2, sigma3, sigma4)
    criticaltensilestress = max(sigma1, sigma2, sigma3, sigma4)

    criticalstresstabtension.append(criticaltensilestress/10**6)
    criticalstresstabcompression.append(criticalcompressionstress/10**6)

    z = z+dz

plt.title('Critical stress in the wing box')
plt.plot(ztab, criticalstresstabcompression, linestyle = 'solid')
plt.plot(ztab, criticalstresstabtension, linestyle = 'dashed')
plt.xlabel('Spanwise position [m]')
plt.ylabel('Stress [MPa]')
plt.show()