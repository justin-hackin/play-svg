"""
There are 6 different shaped triangles bearing the property that
1) their corners have whole numbered angles  
2) there exists one side whose length is phi times another side 
This holds UNDER THE BASE 360 degrees system

What if the base number of degrees in a circle were different.
This code explores this problem.  

It concludes that there seem to be no more than 6 phi triangles even for significantly large base systems,
and that base 60 degree system is all you need to produce 6 phi triangles, 
which would follow from phi_triangle_calculator.py ,
considering the only phi triangles in the 360 degree system have angle numbers all divisible by 6
""" 

from playsvg.geom import *

lengthAB = 10000
pointA = Point()
pointB = Point(0,lengthAB)
ratioBCtoAB = phi
bestValue=0
bestBase=0
for baseDeg in range(13,14400, 2): 
    
    numPhiTri = 0
    for i in range(1,baseDeg/2):
        pointC = extendBendPoint(pointA, pointB,lengthAB*(1/ratioBCtoAB), i/float(baseDeg) )
        angleAB = 180 - i
        angleBC = angalBetween(pointB, pointC, pointA)*baseDeg 
        angleCA = angalBetween(pointC, pointA, pointB)*baseDeg 
        
        minDiff = 0.00000001
        if ( abs(round(angleBC)-angleBC )< minDiff and  abs(round(angleCA)-angleCA ) < minDiff  ):
           #print "BASE: " + baseDeg + "AngleAB: " + str(angleAB) + " BC:" + str(angleBC)+ " CA:" + str(angleCA ) + " BC:AB " + str(BCtoAB/phi)
           numPhiTri += 1
    print "BASE: " + str(baseDeg) + ", # of phi triangles : " + str(numPhiTri)
    if numPhiTri > bestValue:
        bestValue = numPhiTri
        bestBase = baseDeg
        
print "The lowest base with the most phi triangles is: " +str(bestBase)+ " with # phi triangles being: " + str(bestValue)