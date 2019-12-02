def Dragvectors():
    import csv
    import math
    import matplotlib.pyplot as plt
    import numpy as np

    with open('Drag.csv', 'r') as f:
        reader = csv.reader(f)
        Lpts = list(reader)

    dragwfactor = 0 #0.5
    WTOW = 2820900
    thrust = 1496360
    thrust_sweep = 1496360*math.cos(36*math.pi/180)

    Dscaled = []
    Dtot = []
    Dloc = []
    xsection = []
    D2dlist = []
    xpos = []

    # print(Lpts)

    i = 0
    m = 0

    while i in range(len(Lpts)):

        xspan = float(Lpts[i][0])
        xcenter = (xspan + float(Lpts[i - 1][0])) / 2
        D2d = float(Lpts[i][1])
        D2dlist.append(D2d)

        # print(xspan,xcorr,xcenter)

        if m < 1:
            Dsec = D2d * (xspan - 0)

        else:
            Dsec = D2d * (xspan - float(Lpts[i - 1][0]))

        if xspan > 0 and xspan < 27.18:
            xpos.append(xcenter)

            Dloc.append(Dsec)

            # xsection.append(xcorr - float(Lpts[i-1][0])/math.cos(sweeprad))

            # print(xcorr,float(Lpts[i-1][0])/math.cos(sweeprad))

            m = m + 1

        i = i + 1

    scalefac = ((WTOW * dragwfactor) + thrust_sweep*0.5) / sum(Dloc)

    Dscaled = []

    for i in range(len(Dloc)):
        dscaled = Dloc[i] * scalefac

        Dscaled.append(dscaled)

    # print(sum(xsection))
    #print("Scaled drag sum:", sum(Dscaled))
    # plt.plot(xpos,Dscaled)
    # plt.xlabel('Span')
    # plt.ylabel('Drag')
    # plt.show()

    return (xpos, Dscaled)

# Dragvectors()

# print(Dragvectors())