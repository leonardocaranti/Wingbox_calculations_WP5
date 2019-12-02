import matplotlib.pyplot as plt

def Momentvectors():

    from LiftDistribution import Liftvectors

    from moment_of_inertia import chord

    from moment_of_inertia import centroid

    (xspan,lvec) = Liftvectors()

    mvec = []

    def cppos(x):
        xcp = .37 - chord(x)*(.37-.15)/28.74
        return xcp

        #print(centroid(span),cppos(span))

    for i in range(len(xspan)):
        lloc = lvec[i]
        span = xspan[i]

        marm = centroid(span)[0] - cppos(span)
        mloc = lloc * marm

        mvec.append(mloc)

    return(xspan,mvec)

#x,y) = Momentvectors()

#plt.plot(x,y)

#plt.show()

    
    
    
