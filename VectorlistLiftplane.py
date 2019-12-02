def Liftplaneforce():
    from LiftDistribution import Liftvectors
    from WingLoadFunction import WingLoad
    import matplotlib.pyplot as plt
    import operator
    import numpy as np

    (lspan, lvec) = Liftvectors()

    (wspan, wvec) = WingLoad()[0:2]

    fspan = lspan + wspan

    fvec = lvec + wvec

    def sorted(fspan):
        sort = True
        for i in range(len(fspan) - 1):
            if fspan[i + 1] < fspan[i]:
                sort = False
        return sort

    while not sorted(fspan):
        for i in range(len(fspan) - 1):
            if fspan[i + 1] < fspan[i]:
                # Invert values of fspan
                oldv = fspan[i + 1]
                fspan[i + 1] = fspan[i]
                fspan[i] = oldv

                # Invert values of fvec
                oldvl = fvec[i + 1]
                fvec[i + 1] = fvec[i]
                fvec[i] = oldvl

    # print(fspan,fvec)

    # plt.plot(fspan,fvec)
    # plt.xlabel('Span')
    # plt.ylabel('Force')
    # plt.show()

    return (fspan, fvec)
