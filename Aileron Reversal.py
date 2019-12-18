#AILERON REVERSAL

#aileron effectiveness = delta L/ delta L_R
#aileron effectiveness as function of free stream velocity @ sea level and cruise
#plot for final wing box
#T = K*theta

from math import *
from matplotlib import pyplot as plt
import numpy as np


rho = 1.225	#[kg/m^3]
topV = 300 	#[m/s]
e = -0.1706043974864513
c = 3.9 	#[m]
K = 7.3215e7
S = 388.66      #[m^2]
epsilon = 6
clalpha = 11.46 	#[1/rad]
clepsilon = 7.78 	# [1/rad]
cM0epsilon = -1.04 	#[1/rad]

eff_tab = []
V_tab = []


for V in np.arange(0.1,topV,1):
	#deltaT = 0.5*rho*V*V*S*c((clalpha*theta + clepsilon*epsilon)*e + (cM0epsilon*epsilon))
	deltaL = 0.5*rho*V*V*S*(((0.5*rho*V*V*S*c*cM0epsilon*clalpha) + K*clepsilon)/(K - 0.5*rho*V*V*S*c*e*clalpha))
	deltaLR = clepsilon*0.5*rho*V*V*S
	eff = deltaL/deltaLR
	V_r = sqrt((-K*clepsilon)/(0.5*rho*S*c*cM0epsilon*clalpha))

	V_tab.append(V)
	eff_tab.append(eff)

print(V_r)
plt.plot(V_tab,eff_tab)
plt.xlim(0,topV)
plt.ylim(-0.2,1)
plt.xlabel("Freestream Velocity V [m/s]")
plt.ylabel("Aileron Effectiveness")
plt.title("Aileron Effectiveness Against Freestream Velocity")

plt.show()
