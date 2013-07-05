"""Discovers all triangles with whole number angles that have a phi relationship between 2 sides""" 

from playsvg.geom import *
from playsvg.document import *
from playsvg.element import *
from playsvg.path import *
from fractions import Fraction, Decimal
str(Fraction('3.1415926535897932').limit_denominator(1000))

lengthAB = 100
pointA = Point()
pointB = Point(0,lengthAB)
ratioBCtoAB = phi
allTriangles = Document()
for i in range(1,180):
    pointC = extendBendPoint(pointA, pointB,lengthAB*(1/ratioBCtoAB), i/360.0 )
    angleAB = 180 - i
    angleBC = angalBetween(pointB, pointC, pointA)*360 
    angleCA = angalBetween(pointC, pointA, pointB)*360 
    starIt = ""
    minDiff = 0.000000000001
    if ( abs(round(angleBC)-angleBC )< minDiff and  abs(round(angleCA)-angleCA ) < minDiff  ):
        BCtoAB = distanceBetween(pointB, pointC)/distanceBetween(pointC, pointA) 
        print "AngleAB: " + str(angleAB) + " BC:" + str(angleBC)+ " CA:" + str(angleCA ) + " BC:AB " + str(BCtoAB/phi)
        
        docu = Document()
        triangleName = "triangle_"+str(int(angleAB))+"-"+str(int(angleBC))+"-"+str(int(angleCA))
        
        attrs = defaultStyleAttrs
        attrs['id']=triangleName
        thisTriangle = buildPath(PathData().moveTo(pointA).lineTo(pointB).lineTo(pointC).lineTo(pointA), attrs )
        thisGroup = docu.makeGroup(triangleName+"-group")
        thisGroup.append(thisTriangle)
        for i in range(1,12):
            thisGroup.append(buildUse(triangleName, {'transform': 'rotate('+ str(30*i) +')'} ))
        docu.append(thisGroup)
        docu.writeSVG(triangleName+".svg")
        allTriangles.append(thisTriangle)
       
allTriangles.writeSVG("triangle_all-phi.svg")
        