from playsvg.document import *
from playsvg.element import *
from playsvg.geom import *
from playsvg.path import *
from playsvg.element import *
import os
import string
docu = document.Document()

boxSize = 100
borderCorners = [Point(-1*boxSize, -1*boxSize),\
Point(boxSize, -1*boxSize),\
Point(boxSize, boxSize),\
Point(-1*boxSize, boxSize)]
borderCenters = []
for i in range(4):
    borderCenters.append(getMidpoint(borderCorners[i], borderCorners[(i+1)%4]))

borderBox = PathData().makeHull(borderCorners)
docu.appendElement(buildPath(docu, borderBox, {'style':'stroke:black; fill:none'}))
diamondBox = PathData().makeHull(borderCenters)
docu.appendElement(buildPath(docu, diamondBox, {'style':'stroke:black; fill:none'}))

diamondCenters = []
for i in range(4):
    diamondCenters.append(getMidpoint(borderCenters[i], borderCenters[(i+1)%4]))
innerBoxRatio = 0.25    
innerBoxCorners = [Point(-1*innerBoxRatio*boxSize, -1*innerBoxRatio*boxSize),\
Point(innerBoxRatio*boxSize, -1*innerBoxRatio*boxSize),\
Point(innerBoxRatio*boxSize, innerBoxRatio*boxSize),\
Point(-1*innerBoxRatio*boxSize, innerBoxRatio*boxSize)]
docu.appendElement(buildPath(docu, PathData().makeHull(innerBoxCorners), {'style':'stroke:none; fill:black'}))

innerBoxCenters = []
for i in range(4):
    innerBoxCenters.append(getMidpoint(innerBoxCorners[i], innerBoxCorners[(i+1)%4]))

def getTriangleMidpoint(verticies):
    return intersectLineLine(verticies[0], getMidpoint(verticies[1], verticies[2]), verticies[1], getMidpoint(verticies[2], verticies[0]))

def getInnerTrianglePoints(verticies, ratio):
    triPoints = []
    midPoint = getTriangleMidpoint(verticies)
    for i in range(3):
        triPoints.append(getLineDivision(midPoint, verticies[i], ratio))
    return triPoints
inRatio = 0.5
darkTriCornerGroup = docu.makeGroup()
for i in range(4):
    innerTri = getInnerTrianglePoints([borderCenters[i], borderCorners[(i+1)%4],  borderCenters[(i+1)%4]], inRatio) 
    darkTriCornerGroup.appendChild(buildPath(docu, PathData().makeHull(innerTri), {'style':'stroke:none; fill:black'}))
docu.appendElement(darkTriCornerGroup)
spireGroup = docu.makeGroup()

for i in range(4):
    spireGroup.appendChild(buildLine(docu,diamondCenters[i], innerBoxCorners[(i+1)%4],{'style':'stroke:black; fill:none'} ))
    spireGroup.appendChild(buildLine(docu,borderCenters[i], innerBoxCenters[i],{'style':'stroke:black; fill:none'} ))

docu.appendElement(spireGroup)
allRibs = docu.makeGroup()
def makeRibCage(arr):
        ribCageGroup = docu.makeGroup()
        for i in range(len(arr[0])):
            ribCageGroup.appendChild(buildLine(docu, arr[0][i], arr[1][i], {'style':'stroke:black; fill:none'}))
        return ribCageGroup

numRibs = 20
for i in range(4):
    
    pointsBetween= []
    pointsBetween.append(getLineDivisions(innerBoxCenters[i], borderCenters[i], numRibs))
    pointsBetween.append(getLineDivisions(innerBoxCorners[(i+1)%4], diamondCenters[i], numRibs))
    allRibs.appendChild(makeRibCage(pointsBetween))
    pointsBetween= []
    pointsBetween.append(getLineDivisions(innerBoxCorners[(i+1)%4], diamondCenters[i], numRibs))
    pointsBetween.append(getLineDivisions(innerBoxCenters[(i+1)%4], borderCenters[(i+1)%4], numRibs))
    allRibs.appendChild(makeRibCage(pointsBetween))
    
docu.appendElement(allRibs)
    
    
docu.writeSVG("88lemi.svg" )
print "done"

