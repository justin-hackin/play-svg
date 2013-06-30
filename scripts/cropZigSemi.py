"""generates a circular wave pattern"""
import playsvg.document
import playsvg.pathshapes
from playsvg.geom import *
from playsvg.element import *
from playsvg.path import *
docu = document.Document()
semiCirclePoints = []
numSemiPoints = 22
radius = 200
for i in range(numSemiPoints):
    semiCirclePoints.append(Point().polerInit(radius, float(i)/numSemiPoints*0.5))
diameterPoints = getLineDivisions(Point().polerInit(radius, 0.5), Point().polerInit(radius, 0), numSemiPoints)
crissPath = PathData()
crissPath.moveTo(diameterPoints[0])
for i in range(numSemiPoints):
    
    crissPath.lineTo(diameterPoints[i])
    crissPath.lineTo(semiCirclePoints[i])
docu.appendElement(buildPath(docu, crissPath, {'style':'stroke:black;fill:none'}))
docu.writeSVG('crissPath.svg')

docu = document.Document()
semiCirclePoints = []
numSemiPoints = 22
radius = 200
for i in range(numSemiPoints):
    semiCirclePoints.append(Point().polerInit(radius, float(i)/numSemiPoints*0.5))
diameterPoints = getLineDivisions(Point().polerInit(radius-50, 0.5), Point().polerInit(radius-50, 0), numSemiPoints)
crissPath = PathData()
crissPath.moveTo(diameterPoints[0])
for i in range(numSemiPoints):
    
    crissPath.lineTo(diameterPoints[i])
    crissPath.lineTo(semiCirclePoints[i])
docu.appendElement(buildPath(docu, crissPath, {'style':'stroke:black;fill:none'}))
docu.writeSVG('crissPath01.svg')

docu = document.Document()
semiCirclePoints = []
numSemiPoints = 22
radius = 200
for i in range(numSemiPoints):
    semiCirclePoints.append(Point().polerInit(radius, float(i)/(numSemiPoints-1)*0.5))
diameterPoints = getLineDivisions(Point().polerInit(radius-75, 0.5), Point().polerInit(radius-75, 0), numSemiPoints)
crissPath = PathData()
crissPath.moveTo(diameterPoints[0])
for i in range(numSemiPoints):
    crissPath.lineTo(semiCirclePoints[i])
    crissPath.moveTo(diameterPoints[(i+1)%numSemiPoints])

docu.appendElement(buildPath(docu, crissPath, {'style':'stroke:black;fill:none'}))
docu.writeSVG('crissPath02.svg')

docu = document.Document()
semiCirclePoints = []
numSemiPoints = 22
offset = 5
radius = 200
for i in range(numSemiPoints):
    semiCirclePoints.append(Point().polerInit(radius, float(i)/(numSemiPoints-1)*0.5))
diameterPoints = getLineDivisions(Point().polerInit(radius-75, 0.5), Point().polerInit(radius-75, 0), numSemiPoints)
crissPath = PathData()
crissPath.moveTo(diameterPoints[0])
for i in range(numSemiPoints-offset):
    crissPath.lineTo(semiCirclePoints[i+offset])
    crissPath.moveTo(diameterPoints[(i+1)%numSemiPoints])

crissPath.moveTo(semiCirclePoints[0])
for i in range( numSemiPoints-offset):
    crissPath.lineTo(diameterPoints[i+offset])
    crissPath.moveTo(semiCirclePoints[(i+1)%numSemiPoints])
    
docu.appendElement(buildPath(docu, crissPath, {'style':'stroke:black;fill:none'}))
docu.writeSVG('crissPath03.svg')

docu = document.Document()
semiCirclePoints = []
numSemiPoints = 32
offset = 5
radius = 200
for i in range(numSemiPoints):
    semiCirclePoints.append(Point().polerInit(radius, float(i)/(numSemiPoints-1)*0.5))
diameterPoints = getLineDivisions(Point().polerInit(radius-125, 0.5), Point().polerInit(radius-125, 0), numSemiPoints)
crissPath = PathData()
crissPath.moveTo(diameterPoints[0])
for i in range(1,int(numSemiPoints/2)):
    crissPath.lineTo(semiCirclePoints[numSemiPoints-1-i])
    crissPath.lineTo(diameterPoints[numSemiPoints-1])
    crissPath.lineTo(semiCirclePoints[i])
    crissPath.lineTo(diameterPoints[0])
crissPath.closePath()
    
docu.appendElement(buildPath(docu, crissPath, {'style':'stroke:black;fill:none'}))
docu.writeSVG('crissPath04.svg')
