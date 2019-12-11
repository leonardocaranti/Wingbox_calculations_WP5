from math import *
import matplotlib.pyplot as plt
from moment_of_inertia import *
from internal_moments import *
from NormalBendingStress import *
import matplotlib.lines

k1c= 35.1
c=0.0025
sigmastar=k1c/(sqrt(pi*c))
#sigma*= failure stress
#margin of safety crack
MOFC1list= []
MOFC2list= []
MOFC3list= []
MOFC4list= []
MOFC11list= []
MOFC22list= []
MOFC33list= []
MOFC44list= []


mofc1=0
mofc2=0
mofc3=0
mofc4=0
mofc11=0
mofc22=0
mofc33=0
mofc44=0


print(sigmastar)
for i in range(len(sigma1tab)):
	mofc1 = sigmastar/sigma1tab[i]
	MOFC1list.append(mofc1)

for j in range(len(sigma2tab)):
	mofc2 = sigmastar/sigma2tab[j]
	MOFC2list.append(mofc2)

for k in range(len(sigma3tab)):
	mofc3 = sigmastar/sigma3tab[k]
	MOFC3list.append(mofc3)

for l in range(len(sigma4tab)):
	mofc4 = sigmastar/sigma4tab[l]
	MOFC4list.append(mofc4)

for m in range(len(sigma1tab)):
	mofc11 = sigma1tab[m]/sigmastar
	MOFC11list.append(mofc11)

for n in range(len(sigma2tab)):
	mofc22 = sigma2tab[n]/sigmastar
	MOFC22list.append(mofc22)

for o in range(len(sigma3tab)):
	mofc33 = sigma3tab[o]/sigmastar
	MOFC33list.append(mofc33)

for p in range(len(sigma4tab)):
	mofc44 = sigma4tab[p]/sigmastar
	MOFC44list.append(mofc44)

print(MOFC1list)
print(MOFC2list)
print(MOFC3list)
print(MOFC4list)


plt.plot(ztab,MOFC1list,label= 'point 1' ,linestyle= 'solid')

plt.plot(ztab,MOFC2list,label= 'point 2' ,linestyle= 'dotted')

plt.plot(ztab,MOFC3list,label= 'point 3' ,linestyle= 'dashed')

plt.plot(ztab,MOFC4list,label= 'point 4' ,linestyle= 'dashdot')

plt.xlabel("Spanwise position [m]")
plt.ylabel("Margin of safety for crack propagation[-]")
plt.ylim((-300,300))
plt.legend()
plt.show()


plt.plot(ztab,MOFC11list,label= 'point 1' ,linestyle= 'solid')

plt.plot(ztab,MOFC22list,label= 'point 2' ,linestyle= 'dotted')

plt.plot(ztab,MOFC33list,label= 'point 3' ,linestyle= 'dashed')

plt.plot(ztab,MOFC44list,label= 'point 4' ,linestyle= 'dashdot')

plt.xlabel("Spanwise position [m]")
plt.ylabel("Applied stress/Failure stress[-]")
plt.legend()
plt.show()


""" 
plt.plot(ztab,MOFC11list,color='r')
plt.xlabel("Span")
plt.ylabel("Margin of safety at location 1")



plt.subplot(2,4,6)
plt.plot(ztab,MOFC22list,color='r')
plt.xlabel("Span")
plt.ylabel("Margin of safety at location 2")


plt.subplot(2,4,7)
plt.plot(ztab,MOFC33list,color='r')
plt.xlabel("Span")
plt.ylabel("Margin of safety at location 3")


plt.subplot(2,4,8)
plt.plot(ztab,MOFC44list,color='r')
plt.xlabel("Span")
plt.ylabel("Margin of safety at location 4")



plt.show()


"""
