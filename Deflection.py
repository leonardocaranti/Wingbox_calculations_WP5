import moment_of_inertia
import numpy as np
import matplotlib.pyplot as plt
import VectorlistLiftplane
import VectorlistDragplane
import time

def Deflection(halfspan = 57.443/2, E = 71.7*10**9, xEngine1 = 0.4*57.443/2, xEngine2 = 0.7*57.443/2):
    '''
    Outputs an array of deflection values and slopes dependant on the span array and force array
    :param spanAr:
    :param forceAr:
    :param halfspan:
    :param E:
    :return:
    '''

    wingload = VectorlistLiftplane.Liftplaneforce()
    #wingload = VectorlistDragplane.Dragplaneforce()

    spanAr = wingload[0]
    forceAr = wingload[1]

    dx = spanAr[1]-spanAr[0]

    # Deflection caused by point loads
    def pointLoadDeflection(F, distForce, x, halfspan, E, I):

        if 0 <= x <= distForce:
            return (F*x**2*(3*distForce-x))/(6*E*I)
        elif distForce <= x <= halfspan:
            return (F*distForce**2*(3*x-distForce))/(6*E*I)

    def pointLoadSlop(F, distForce, x, halfspan, E, I):

        if 0 <= x <= distForce:
            return (F*x*(2*distForce-x))/(2*E*I)
        elif distForce <= x <= halfspan:
            return (F*distForce**2)/(2*E*I)


    deflectionAr = []
    slopeAr = []
    np.array(deflectionAr)
    np.array(slopeAr)

    # Run through each point load
    print("Starting deflection calculation")
    start_time = time.time()
    for i in range(0, len(spanAr)):
        # Run through each spanwise location of the point load
        distribution = []
        slope = []

        I = moment_of_inertia.MOI(spanAr[i])[0]

        for x in range(0, len(spanAr)):
            if spanAr[i]-dx/2 <= xEngine1 <= spanAr[i]+dx/2 or  spanAr[i]-dx/2 <= xEngine2 <= spanAr[i]+dx/2:
                distribution.append(pointLoadDeflection(forceAr[i], spanAr[i], spanAr[x], halfspan, E, I))
                #slope.append(pointLoadSlop(forceAr[i], spanAr[i], spanAr[x], halfspan, E, I))
            else:
                distribution.append(pointLoadDeflection(forceAr[i], spanAr[i], spanAr[x], halfspan, E, I))
                #slope.append(pointLoadSlop(forceAr[i], spanAr[i], spanAr[x], halfspan, E, I))
        deflectionAr.append(distribution)
        #slopeAr.append(slope)
        print("Deflection progress: " + str(i+1) +"/" + str(len(spanAr)) + " | " + str(round((i+1)*100/(len(spanAr)),2)) + "%")

    # Add up all deflections of all point loads
    deflectionAr = np.sum(deflectionAr, axis=0)
    #slopeAr = np.sum(slopeAr, axis=0)
    print("End deflection calculations, excecuting time: " + str(round(time.time()-start_time,2)) + " seconds")
    print("Tip deflection: " + str(round(deflectionAr[-1], 3)) + "m")

    plt.grid()
    plt.subplot(311)
    plt.title("Force and deflection vs span")
    plt.xlabel("Span [m]")
    plt.ylabel("Force [N]")
    plt.plot(wingload[0], wingload[1], color='blue')
    plt.subplot(312)
    plt.xlabel("Span [m]")
    plt.ylabel("Deflection [m]")
    plt.plot(wingload[0], deflectionAr, color='red')
    #plt.subplot(313)
    #plt.xlabel("Span [m]")
    #plt.ylabel("Slope")
    #plt.plot(wingload[0], slopeAr, color='green')
    plt.show()

    return deflectionAr, slopeAr

Deflection()