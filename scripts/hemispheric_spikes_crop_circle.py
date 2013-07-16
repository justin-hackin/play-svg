"""generates a circular wave pattern"""
import playsvg.document
import playsvg.pathshapes
from playsvg.geom import *
from playsvg.element import *
from playsvg.path import *
docu = document.Document()

semiCirclePoints = []
numSemiPoints = 32

radius = 200*3
inset = 125*3
for i in range(numSemiPoints):
    semiCirclePoints.append(Point().polerInit(radius, float(i)/(numSemiPoints-1)*0.5))
diameterPoints = getLineDivisions(Point().polerInit(radius-inset, 0.5), Point().polerInit(radius-inset, 0), numSemiPoints)
crissPath = PathData()
crissPath.moveTo(diameterPoints[0])
for i in range(1,int(numSemiPoints/2)):
    crissPath.lineTo(semiCirclePoints[numSemiPoints-1-i])
    crissPath.lineTo(diameterPoints[numSemiPoints-1])
    crissPath.lineTo(semiCirclePoints[i])
    crissPath.lineTo(diameterPoints[0])
crissPath.closePath()
    
docu.append(buildPath( crissPath, {'id':'criss','style':'stroke:none;fill:black;fill-rule:evenodd'}))
docu.append(buildUse('criss', {'transform':'rotate(180)'}))
docu.writeSVG('hemispheric_spikes_crop_circle.svg')
print 'done'