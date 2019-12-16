from math import *
from CompressionBuckling import *
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
z = 0.1
dz = 0.1

MoS_point1_Columntab, MoS_point2_Columntab, MoS_point3_Columntab, MoS_point4_Columntab, ztab = [],[],[],[],[]

while z <= b:
    normalstress1, normalstress2, normalstress3, normalstress4 = Normalstress(z)

    MoS_point1_Column = normalstress1/columnbuckling(z)
    MoS_point2_Column = normalstress2/columnbuckling(z)
    MoS_point3_Column = normalstress3/columnbuckling(z)
    MoS_point4_Column = normalstress4/columnbuckling(z)

    ztab.append(z)
    MoS_point1_Columntab.append(MoS_point1_Column)
    MoS_point2_Columntab.append(MoS_point2_Column)
    MoS_point3_Columntab.append(MoS_point3_Column)
    MoS_point4_Columntab.append(MoS_point4_Column)

    z = z+dz

plt.plot(ztab, MoS_point1_Columntab)
plt.plot(ztab, MoS_point2_Columntab)
plt.plot(ztab, MoS_point3_Columntab)
plt.plot(ztab, MoS_point4_Columntab)
plt.xlabel('Spanwise position [m]')
plt.ylabel('Margin of Safety')

plt.show()
