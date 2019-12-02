'''
Weight force diagram generator that includes the wing weight, wingtip weight, engine weight and fuel weight
'''

import decimal
import moment_of_inertia

def WingLoad(accuracy = 1000, wingspan = 57.443, massEngine = 24984, massWing = 24014, massFuel = 104790*0.59, xEngine1 = 0.3*57.443/2,
             xEngine2 = 0.7*57.443/2, densityKerosine = 810, pointLoadWingTip = 16000):

    """
    Returns a 2D array giving the spanwise location alongside with the total force in the z direction (positive downward)
    :param accuracy: Defines for how many points the force is calculated
    :param wingspan: The wingspan of the aircraft (NOT half wingspan)
    :param massEngine: The mass of the engine in kg
    :param massWing: The mass of the wing in kg NOTE weight of the full wing
    :param massFuel: The mass of the fuel in kg NOTE this fuel amount goes in both of the wings
    :param xEngine1: The spanwise location of the first engine
    :param xEngine2: The spanwise location of the second engine
    :param densityKerosine: The density of the fuel used (kerosine)
    :param pointLoadWingTip: The estimated point load of the wingtip in Newtons
    :return: 2D Array giving x,z values where the z values corrospond to the force at the x position
    """

    # const
    g = 9.80665         # m/s^2
    halfwingspan = wingspan/2   # m
    dx = halfwingspan/accuracy

    # for wing weight only

    # Area of triangle 2 * A / b = h Note the 2 * drops out because mass of the wing is divided by 2
    rootForceWing = massWing*g/halfwingspan
    # slope = dz/dx note - sign because z axis is positive downwards
    slopeWing = -rootForceWing/halfwingspan

    def wingForce(b):
        """
        Calculates the force on the wing at spanwise location b
        :param b: spanwise position
        :return:
        """
        return slopeWing*b+rootForceWing

    # Get the amount of decimal places of the halfwingspan and dx and take the maximum amount
    decimalPlaces = \
        abs(min(decimal.Decimal(str(halfwingspan)).as_tuple().exponent, decimal.Decimal(str(dx)).as_tuple().exponent))

    # Calculate the fuel tank end location assuming it starts at the root
    Volume = 0
    RequiredVolume = (massFuel/2)/(densityKerosine)

    # Integrate untill the required fuel volume is reached
    for x in range(0, int(halfwingspan*10**decimalPlaces+dx*10**decimalPlaces), int(dx*10**decimalPlaces)):
        b = x / 10 ** int(decimalPlaces)
        Area = moment_of_inertia.local_area(b)
        Volume += Area * dx

        if Volume >= RequiredVolume:
            xFuelTankEnd = b
            #print("Fuel tank ends at a spanwise location of " + str(b) + " m")
            break
        elif b >= halfwingspan:
            xFuelTankEnd = halfwingspan
            #print("Error: integration for fuel volume failed, the length required is larger than the halxspan " + str(b) + " m")
            #return "Error in fuel volume"

    # For the fuel load only

    # For the fuel load assuming the fuel tank starts at the root, 2 drops out because massfuel is divided by 2
    rootForceFuel = massFuel*g/xFuelTankEnd
    # slope
    slopeFuel = -rootForceFuel/halfwingspan

    def fuelForce(b):
        """
        Calculates the force created by the weight at spanwise position b
        :param b: spanwise position
        :return:
        """
        if 0 <= b <= xFuelTankEnd:
            return slopeFuel*b+rootForceFuel
        else:
            return 0

    xspan = [xEngine1, xEngine2]
    wscaled = [massEngine*g, massEngine*g]
    M_y = []

    for x in range(0, int(halfwingspan*10**decimalPlaces+dx*10**decimalPlaces), int(dx*10**decimalPlaces)):
        b = x / 10 ** int(decimalPlaces)
        totalForce = wingForce(b) + fuelForce(b)

        # Account for the wingtip and engine
        if b == halfwingspan:
            totalForce += pointLoadWingTip
        #elif xEngine1-dx/2 <= b <= xEngine1+dx/2 or xEngine2-dx/2 <= b <= xEngine2+dx:
            #totalForce += massEngine*g

        xspan.append(b)
        wscaled.append(totalForce*dx)
        M_y.append(totalForce*b)

    def sorted(xspan):
        sort = True
        for i in range(len(xspan) - 1):
            if xspan[i + 1] < xspan[i]:
                sort = False
        return sort

    while not sorted(xspan):
        for i in range(len(xspan) - 1):
            if xspan[i + 1] < xspan[i]:
                # Invert values of xspan
                oldv = xspan[i + 1]
                xspan[i + 1] = xspan[i]
                xspan[i] = oldv

                # Invert values of wscaled
                oldvl = wscaled[i + 1]
                wscaled[i + 1] = wscaled[i]
                wscaled[i] = oldvl

    return (xspan, wscaled)