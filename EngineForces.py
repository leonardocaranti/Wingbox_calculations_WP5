b_2 = 28.74

def Thrustforce():

    import math
    
    #engine bending diagram
    Mint=[]
    A=1
    x=0
    abcd=[]
    zxcv=[]

    span= 27.313
    sweepgrad=36
    sweeprad=sweepgrad*math.pi/180
    Eg1_thrust=374000
    Eg2_thrust=374000
    Eg1_width_posit=b_2*0.4
    Eg2_width_posit=b_2*0.7
    Eg1_height_posit=0.
    Eg1_height_posit=0.

    Eg1Fx=math.sin(sweeprad)*Eg1_thrust
    Eg2Fx=math.sin(sweeprad)*Eg2_thrust
    Eg1Fy=math.cos(sweeprad)*Eg1_thrust
    Eg2Fy=math.cos(sweeprad)*Eg1_thrust
    T1 = Eg1Fy
    T2 = Eg2Fy
    #to test use these values
    #Eg1Fy=10
    #Eg2Fy=10

    Xloclist=[]

    while A==1:
        if x>=7:
            Eg1Fy=0
        if x>=15:
            Eg1Fy=0
            Eg2Fy=0
            
        lst=[]
        L1=Eg1_width_posit - x
        L2=Eg2_width_posit - x
        Me1=L1*Eg1Fy
        Me2=L2*Eg2Fy
        Mtemp=Me1+Me2

        abcd.append(Mtemp)
        zxcv.append(x)
        
        x=round(x,3)
        Mtemp=round(Mtemp,3)
        lst.append(Mtemp)
        lst.append(x)
        x=x+0.100000
        Mint.append(lst)
        if x>=27.313:
            break
    #print (Mint)

    x = [Eg1_width_posit,Eg2_width_posit]
    Th = [T1,T2]

    print(Eg1Fy,Eg2Fy)

    #from matplotlib import pyplot as plt


    #plt.plot(zxcv,abcd,color='r')
    #plt.xlabel("Distance [m]")
    #plt.ylabel("Internal bending moment [Nm]")

    #plt.show()

    return(x,Th)



