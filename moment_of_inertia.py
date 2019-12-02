from math import *
from matplotlib import pyplot as plt

b_2 = 28.74
density = 2.83 * 1000

# Tip
tip_chord = 2.75
rear_spar_h_tip = 0.2324  # At 65% of chord
front_spar_h_tip = 10.29 / 100 * tip_chord  # At 20% of chord
tip_dist = 0.45 * tip_chord
theta_tip = atan((front_spar_h_tip - rear_spar_h_tip) * 0.5 / tip_dist)

# Root
root_chord = 12.5
rear_spar_h_root = 0.8606
front_spar_h_root = 10.29 / 100 * root_chord
root_dist = 0.45 * root_chord
theta_root = atan((front_spar_h_root - rear_spar_h_root) * 0.5 / root_dist)

"""
#Case 1
t0, t1 = 0.07, 0.03
stringer_height_0, stringer_height_1 = 0.12, 0.12
stringer_thickness_0, stringer_thickness_1 = 0.03, 0.03
cross_section_value = 1                                     # 1 corresponds to a cross section of skins only + one central spar, 2 is skins + stringers on the top, 3 is stringers on top and bottom
no_stringers_top = 35                                        # Must be greater than 1 for code to work!
no_stringers_bott = 25                                       # Must be greater than 1 for code to work!
"""

"""
#Case 2
t0, t1 = 0.03, 0.03
stringer_height_0, stringer_height_1 = 0.05, 0.05
stringer_thickness_0, stringer_thickness_1 = 0.01, 0.01
cross_section_value = 2                                     # 1 corresponds to a cross section of skins only + one central spar, 2 is skins + stringers on the top, 3 is stringers on top and bottom
no_stringers_top = 14                                        # Must be greater than 1 for code to work!
no_stringers_bott = 5                                       # Must be greater than 1 for code to work!
"""

# Case 3
t0, t1 = 0.03, 0.03
stringer_height_0, stringer_height_1 = 0.05, 0.05
stringer_thickness_0, stringer_thickness_1 = 0.01, 0.01
cross_section_value = 3  # 1 corresponds to a cross section of skins only + one central spar, 2 is skins + stringers on the top, 3 is stringers on top and bottom
no_stringers_top = 10  # Must be greater than 1 for code to work!
no_stringers_bott = 5  # Must be greater than 1 for code to work!

"""Random
t0, t1 = 0.02, 0.01
stringer_height_0, stringer_height_1 = 0.012, 0.12
stringer_thickness_0, stringer_thickness_1 = 0.01, 0.01
cross_section_value = 2                                     # 1 corresponds to a cross section of skins only, 2 is skins + stringers on the top, 3 is stringers on top and bottom
no_stringers_top = 9                                        # Must be greater than 1 for code to work!
no_stringers_bott = 4                                       # Must be greater than 1 for code to work!
"""


class beam:

    def __init__(self, h, l, x_coord, y_coord, beta):
        self.height = h
        self.length = l
        self.area = l * h
        self.centroid = [x_coord, y_coord]

        # Calculate moment of inertia around the centroid
        self.moi_xx = l * h / 12 * (l ** 2 * (cos(beta)) ** 2 + h ** 2 * (sin(beta)) ** 2)
        self.moi_yy = l * h / 12 * (l ** 2 * (sin(beta)) ** 2 + h ** 2 * (cos(beta)) ** 2)
        self.moi_xy = l * h / 12 * cos(beta) * sin(beta) * (h ** 2 + l ** 2)

        self.x_coords = [x_coord + l / 2 * cos(beta) + h / 2 * sin(beta),
                         x_coord + l / 2 * cos(beta) - h / 2 * sin(beta),
                         x_coord - (l / 2 * cos(beta) + h / 2 * sin(beta)),
                         x_coord - (l / 2 * cos(beta) - h / 2 * sin(beta))]
        self.y_coords = [y_coord + l / 2 * sin(beta) - h / 2 * cos(beta),
                         y_coord + l / 2 * sin(beta) + h / 2 * cos(beta),
                         y_coord - (l / 2 * sin(beta) - h / 2 * cos(beta)),
                         y_coord - (l / 2 * sin(beta) + h / 2 * cos(beta))]
        self.x_coords.append(self.x_coords[0])
        self.y_coords.append(self.y_coords[0])


class stringer:

    # The coordinates of the position are related to the position of the corner
    def __init__(self, h, t, x_coord, y_coord, theta):
        self.height = h
        self.thickness = t
        self.area = (h - t) * t + h * t

        # Calculate moment of inertia around the centroid
        top_beam = beam(t, h - t, x_coord + h / 2 * cos(theta), y_coord + h / 2 * sin(theta), theta)
        bott_beam = beam(h, t, x_coord + h / 2 * sin(theta), y_coord - h / 2 * cos(theta), theta)
        self.centroid = [(top_beam.centroid[0] * top_beam.area + bott_beam.centroid[0] * bott_beam.area) / (
                    top_beam.area + bott_beam.area), \
                         (top_beam.centroid[1] * top_beam.area + bott_beam.centroid[1] * bott_beam.area) / (
                                     top_beam.area + bott_beam.area)]
        self.moi_xx = top_beam.moi_xx + top_beam.area * (
                    top_beam.centroid[1] - self.centroid[1]) ** 2 + bott_beam.moi_xx + bott_beam.area * (
                                  bott_beam.centroid[1] - self.centroid[1]) ** 2
        self.moi_yy = top_beam.moi_yy + top_beam.area * (
                    top_beam.centroid[0] - self.centroid[0]) ** 2 + bott_beam.moi_yy + bott_beam.area * (
                                  bott_beam.centroid[0] - self.centroid[0]) ** 2
        self.moi_xy = top_beam.moi_xy + top_beam.area * (top_beam.centroid[0] - self.centroid[0]) * (
                    top_beam.centroid[1] - self.centroid[1]) \
                      + bott_beam.moi_xy + bott_beam.area * (bott_beam.centroid[0] - self.centroid[0]) * (
                                  bott_beam.centroid[1] - self.centroid[1])

        self.x_coords = [x_coord, x_coord + h * cos(theta), x_coord + h * cos(theta) + t * sin(theta),
                         x_coord + t * cos(theta) + t * sin(theta), x_coord + t * cos(theta) + h * sin(theta),
                         x_coord + h * sin(theta)]
        self.y_coords = [y_coord, y_coord + h * sin(theta), y_coord + h * sin(theta) - t * cos(theta),
                         y_coord - t * cos(theta) + t * sin(theta), y_coord + t * sin(theta) - h * cos(theta),
                         y_coord - h * cos(theta)]
        self.x_coords.append(self.x_coords[0])
        self.y_coords.append(self.y_coords[0])


def param(initial_value, final_value, span_pos):
    return span_pos * (final_value - initial_value) / b_2 + initial_value


def initial_values(span_position):
    t, theta, dist, front_spar_h, rear_spar_h = param(t0, t1, span_position), param(theta_root, theta_tip,
                                                                                    span_position), param(root_dist,
                                                                                                          tip_dist,
                                                                                                          span_position), param(
        front_spar_h_root, front_spar_h_tip, span_position), param(rear_spar_h_root, rear_spar_h_tip, span_position)
    stringer_height, stringer_thickness = param(stringer_height_0, stringer_height_1, span_position), param(
        stringer_thickness_0, stringer_thickness_1, span_position)
    return t, theta, dist, front_spar_h, rear_spar_h, stringer_height, stringer_thickness


def cross_section(value, span_position):
    t, theta, dist, front_spar_h, rear_spar_h, stringer_height, stringer_thickness = initial_values(span_position)

    up_sheet = beam(t, (dist - 2 * t) / cos(theta), 0, front_spar_h / 2 - (front_spar_h - rear_spar_h) / 4, -theta)
    down_sheet = beam(t, (dist - 2 * t) / cos(theta), 0, -(front_spar_h / 2 - (front_spar_h - rear_spar_h) / 4), theta)
    front_spar = beam(front_spar_h + t, t, -dist / 2 + t / 2, 0, 0)
    rear_spar = beam(rear_spar_h + t, t, dist / 2 - t / 2, 0, 0)
    elements = [up_sheet, down_sheet, front_spar, rear_spar]

    if value == 1:
        central_spar = beam((front_spar_h + rear_spar_h) / 2 - t, t, 0, 0, 0)
        elements.append(central_spar)

    if value == 2:

        for i in range(no_stringers_top):
            if i < no_stringers_top - 1:
                string = stringer(stringer_height, stringer_thickness,
                                  -(dist - 2 * t) / 2 + (dist - 2 * t) / (no_stringers_top - 1) * i,
                                  front_spar_h / 2 - t - ((front_spar_h - rear_spar_h) / 2) / (
                                              no_stringers_top - 1) * i, 0)
                elements.append(string)
            else:
                string = stringer(stringer_height, stringer_thickness,
                                  -(dist - 2 * t) / 2 + (dist - 2 * t) / (no_stringers_top - 1) * i,
                                  front_spar_h / 2 - t - ((front_spar_h - rear_spar_h) / 2) / (
                                              no_stringers_top - 1) * i, -pi / 2)
                elements.append(string)

    if value == 3:

        for i in range(no_stringers_top):
            if i < no_stringers_top - 1:
                string = stringer(stringer_height, stringer_thickness,
                                  -(dist - 2 * t) / 2 + (dist - 2 * t) / (no_stringers_top - 1) * i,
                                  front_spar_h / 2 - t - ((front_spar_h - rear_spar_h) / 2) / (
                                              no_stringers_top - 1) * i, 0)
                elements.append(string)
            else:
                string = stringer(stringer_height, stringer_thickness,
                                  -(dist - 2 * t) / 2 + (dist - 2 * t) / (no_stringers_top - 1) * i,
                                  front_spar_h / 2 - t - ((front_spar_h - rear_spar_h) / 2) / (
                                              no_stringers_top - 1) * i, -pi / 2)
                elements.append(string)

        for i in range(no_stringers_bott):
            if i < no_stringers_bott - 1:
                string = stringer(stringer_height, stringer_thickness,
                                  -(dist - 2 * t) / 2 + (dist - 2 * t) / (no_stringers_bott - 1) * i, -(
                                front_spar_h / 2 - t - ((front_spar_h - rear_spar_h) / 2) / (
                                    no_stringers_bott - 1) * i), pi / 2)
                elements.append(string)
            else:
                string = stringer(stringer_height, stringer_thickness,
                                  -(dist - 2 * t) / 2 + (dist - 2 * t) / (no_stringers_bott - 1) * i, -(
                                front_spar_h / 2 - t - ((front_spar_h - rear_spar_h) / 2) / (
                                    no_stringers_bott - 1) * i), pi)
                elements.append(string)

    return elements


def centroid(span_position):
    elements = cross_section(cross_section_value, span_position)

    # Centroid calculations, to finish
    areas_dist_x = 0
    areas_dist_y = 0
    areas = 0
    for element in elements:
        areas_dist_x += element.area * element.centroid[0]
        areas_dist_y += element.area * element.centroid[1]
        areas += element.area

    centr_x, centr_y = areas_dist_x / areas, areas_dist_y / areas

    return centr_x, centr_y


def MOI(span_position):
    elements = cross_section(cross_section_value, span_position)

    moi_xx = 0
    moi_yy = 0
    moi_xy = 0
    for element in elements:
        moi_xx += element.moi_xx + element.area * (element.centroid[0] - centroid(span_position)[0]) ** 2
        moi_yy += element.moi_yy + element.area * (element.centroid[1] - centroid(span_position)[1]) ** 2
        moi_xy += element.moi_xy + element.area * (element.centroid[0] - centroid(span_position)[0]) * (
                    element.centroid[1] - centroid(span_position)[1])

    return moi_xx, moi_yy, moi_xy

def MOA(span_position):
    elements = cross_section(cross_section_value, span_position)


def centr_chord(span_position):
    centr_x, centr_y = centroid(span_position)
    ch = chord(span_position)



def J(span_position):
    moi_xx, moi_yy, moi_xy = MOI(span_position)
    return moi_xx + moi_yy


def plot_cross_section(span_position):
    elements = cross_section(cross_section_value, span_position)
    for element in elements:
        if type(element) == stringer:
            colour = "black"
        if type(element) == beam:
            colour = "black"
        plt.plot(element.x_coords, element.y_coords, color=colour)

    centr = centroid(span_position)
    plt.axvline(x=centr[0], lw=1, ls='dashed', color = "black")
    plt.axhline(y=centr[1], lw=1, ls='dashed', color = "black")
    plt.title(label="Cross-section at a span position of " + str(span_position) + "[m]")
    plt.text(centr[0]*10, centr[1]*10, "Centroid: (" + str(round(centr[0],2)) + "," + str(round(centr[1],2)) + ")", color = "green")

    plt.show()


def chord(span_position):
    chord0, chord1 = root_dist / 0.4, tip_dist / 0.4
    chord = span_position * (chord1 - chord0) / b_2 + chord0
    return chord


def local_area(span_position):
    # Define cross section
    t, theta, dist, front_spar_h, rear_spar_h, stringer_height, stringer_thickness = initial_values(span_position)
    area = (front_spar_h + rear_spar_h) / 2 * dist
    return area


def max_distances(span_position):
    centr = centroid(span_position)
    t, theta, dist, front_spar_h, rear_spar_h, stringer_height, stringer_thickness = initial_values(span_position)
    x_max = (front_spar_h / 2 + abs(centr[0])) * centr[0] / abs(centr[0])
    y_max = (dist / 2 + abs(centr[1])) * centr[1] / abs(centr[1])

    return x_max, y_max


def mass():
    elements_root = cross_section(cross_section_value, 0)
    area_root = 0
    for element_root in elements_root:
        area_root += element_root.area

    elements_tip = cross_section(cross_section_value, b_2)
    area_tip = 0
    for element_tip in elements_tip:
        area_tip += element_tip.area

    avg_area = (area_root + area_tip) / 2
    return density * avg_area
