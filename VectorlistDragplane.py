def Dragplaneforce():
    from DragDistribution import Dragvectors
    from EngineForces import Thrustforce
    import matplotlib.pyplot as plt
    import operator
    import numpy as np

    (dspan, dvec) = Dragvectors()

    dvecn = []

    for i in range(len(dvec)):
        d = dvec[i]
        dvecn.append(-d)

    (tspan, tvec) = Thrustforce()

    fspan = dspan + tspan

    fvec = dvecn + tvec

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


    return (fspan, fvec)

