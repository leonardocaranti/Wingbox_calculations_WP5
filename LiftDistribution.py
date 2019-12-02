maxload = 3.75

def Liftvectors():
    import csv
    import math
    import matplotlib.pyplot as plt
    import numpy as np

    with open('Lift.csv', 'r') as f:
        reader = csv.reader(f)
        Lpts = list(reader)


    WTOW = 2820900
    sweep = 29
    sweeprad = math.radians(sweep)

    Lscaled = []
    Ltot = []
    Lloc = []
    xscaled = []
    xsection = []
    L2dlist = []

    # print(Lpts)

    i = 0
    m = 0

    while i in range(len(Lpts)):

        # print(Lpts[i-1][0])
        xspan = float(Lpts[i][0])
        xcorr = xspan * (28.72 / 27.18)
        xcenter = (xspan + float(Lpts[i - 1][0])) * (28.72 / 27.18) / 2
        L2d = float(Lpts[i][1])
        L2dlist.append(L2d)

        # print(xspan,xcorr,xcenter)

        if m < 1:
            Lsec = L2d * (xcorr - 0)

        else:
            Lsec = L2d * (xcorr - float(Lpts[i - 1][0]) * (28.72 / 27.18))

        if xspan >= 0 and xspan <= 27.18:
            #print(xcenter)
            xscaled.append(xcenter)

            Lloc.append(Lsec)

            # xsection.append(xcorr - float(Lpts[i-1][0])/math.cos(sweeprad))

            # print(xcorr,float(Lpts[i-1][0])/math.cos(sweeprad))

            m = m + 1

        i = i + 1

    scalefac = (WTOW * maxload) / sum(Lloc)

    Lscaled = []

    for i in range(len(Lloc)):
        lscaled = -(Lloc[i] * scalefac)

        Lscaled.append(lscaled)

    # print(sum(xsection))
    # print(sum(Lscaled))
    # plt.plot(xscaled,Lscaled)
    # plt.xlabel('Span')
    # plt.ylabel('Lift')
    # plt.show()

    return (xscaled, Lscaled)


#Liftvectors()