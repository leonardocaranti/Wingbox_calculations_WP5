import moment_of_inertia
import numpy as np

def Deflection(spanAr, forceAr, halfspan = 57.443/2, E = 71*10**9):
    '''
    Outputs an array of deflection values and slopes dependant on the span array and force array
    :param spanAr:
    :param forceAr:
    :param halfspan:
    :param E:
    :return:
    '''

    # Deflection caused by point loads
    def pointLoadDeflection(F, distForce, x, halfspan, E):
        I = sum(moment_of_inertia.MOI(distForce))

        if 0 <= x <= distForce:
            return (F*x**2*(3*distForce-x))/(6*E*I)
        elif distForce <= x <= halfspan:
            return (F*distForce**2*(3*x-distForce))/(6*E*I)

    def pointLoadSlop(F, distForce, x, halfspan, E):
        I = sum(moment_of_inertia.MOI(distForce))

        if 0 <= x <= distForce:
            return (F*x*(2*distForce-x))/(2*E*I)
        elif distForce <= x <= halfspan:
            return (F*distForce**2)/(2*E*I)


    deflectionAr = []
    slopeAr = []
    # Run through each point load
    for i in range(0, len(spanAr)):
        # Run through each spanwise location of the point load
        distribution = []
        slope = []
        for x in range(0, len(spanAr)):
            distribution.append(pointLoadDeflection(forceAr[i], spanAr[i], spanAr[x], halfspan, E))
            slope.append(pointLoadSlop(forceAr[i], spanAr[i], spanAr[x], halfspan, E))
        deflectionAr.append(distribution)
        slopeAr.append(slope)

    np.array(deflectionAr)
    np.array(slopeAr)

    # Add up all deflections of all point loads
    deflectionAr = np.sum(deflectionAr, axis=0)
    slopeAr = np.sum(slopeAr, axis=0)

    return deflectionAr, slopeAr