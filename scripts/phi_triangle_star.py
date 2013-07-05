"""Discovers all triangles with whole number angles that have a phi relationship between 2 sides""" 

from playsvg.geom import *
from playsvg.document import *
from playsvg.element import *
from playsvg.path import *


lengthAB = 100
pointA = Point()
pointB = Point(0,lengthAB)
ratioBCtoAB = phi
allTriangles = Document()
phiTriAng = [132, 96, 72, 36, 24, 12]
numVert = 10
polyRad = 400
docSize = 640
docu = Document(gridSize=640)
docu.append(buildRect(Point(docSize*-1., docSize*-1.), docSize*2, docSize*2, {'style':'fill:black'} ))
for h in range(2):
    polyVert = createRadialPlots(Point(), polyRad, numVert, True)
    polySideLength = distanceBetween(polyVert[0], polyVert[1])
    thisRingGroup = docu.makeGroup("ring-group_"+str(h))   
    for i in range(numVert):
        for triAng in phiTriAng:
            pointA = polyVert[i]
            pointB = polyVert[(i+1)%numVert]
            
            pointC = extendBendPoint(pointA, pointB, polySideLength*(1/ratioBCtoAB), triAng/360.0)
            pointF = extendBendPoint(pointA , pointB ,polySideLength*(1/ratioBCtoAB), (1-triAng)/360.0 )
            
            pointD = extendBendPoint(pointB , pointA ,polySideLength*(1/ratioBCtoAB), (1-triAng)/360.0 )
            pointE = extendBendPoint(pointB , pointA ,polySideLength*(1/ratioBCtoAB), triAng/360.0 )
            
            angleAB = 180 - triAng
            angleBC = angalBetween(pointB, pointC, pointA)*360 
            angleCA = angalBetween(pointC, pointA, pointB)*360
                    
            triangleName = "triangle_"+str(int(angleAB))+"-"+str(int(angleBC))+"-"+str(int(angleCA))+"_iter-"+str(h)
            thisGroup = docu.makeGroup(triangleName+"-group_"+str(i))
            
            attrs = {'style':'fill:white;opacity:0.18;stroke:none'}
            
            
            attrs['id']=triangleName+"_LRD"
            thisTriangle1 = buildPath(PathData().moveTo(pointA).lineTo(pointB).lineTo(pointC).closePath(), attrs )
            thisGroup.append(thisTriangle1)
            
            attrs['id']=triangleName+"_RLD"
            thisTriangle2 = buildPath(PathData().moveTo(pointB).lineTo(pointA).lineTo(pointD).closePath(), attrs )
            thisGroup.append(thisTriangle2)
            
            attrs['id']=triangleName+"_LRU"
            thisTriangle3 = buildPath(PathData().moveTo(pointA).lineTo(pointB).lineTo(pointE).closePath(), attrs )
            thisGroup.append(thisTriangle3)
            
            attrs['id']=triangleName+"_LRU"
            thisTriangle4 = buildPath(PathData().moveTo(pointA).lineTo(pointB).lineTo(pointF).closePath(), attrs )
            thisGroup.append(thisTriangle4)
    
            thisRingGroup.append(thisGroup)
    docu.append(thisRingGroup)        
    polyRad = polyRad*(phi**-1)
    
        
docu.writeSVG("phi_triangle_star.svg")
