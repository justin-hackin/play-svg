"""generates a circular wave pattern """
import playsvg.document
import playsvg.pathshapes
from playsvg.geom import *
from playsvg.element import *

docu = document.Document()

numPoints = 16
radius = 400
controlOffsetTotal = 300
controlInsetRatio = 0.33
centrePoint = Point(0,0)
levels = 6
gap = 0.1
tilt = 1.0/16 + gap 
otherTilt = 1- gap
extent = 0.5
    
path1 = PathData().moveTo(Point().polerInit(radius, 0))
path2 = PathData().moveTo(Point().polerInit(radius, 0))
for i in range(numPoints):
    if i%2 ==0 :
        path1.SCRVBD((extent, tilt), Point().polerInit( radius, float((i+1)%numPoints)/numPoints))
        path2.SCRVBD((extent, otherTilt), Point().polerInit( radius, float((i+1)%numPoints)/numPoints))
    else:
        path2.SCRVBD((extent, tilt), Point().polerInit( radius, float((i+1)%numPoints)/numPoints))
        path1.SCRVBD((extent, otherTilt), Point().polerInit( radius, float((i+1)%numPoints)/numPoints))
path1.closePath()
path2.closePath()
docu.appendElement(buildPath(abase, path1, {'style':'stroke:black;fill:none'}))
docu.appendElement(buildPath(abase, path2, {'style':'stroke:black;fill:none'}))

abase.writeSVG('timeWeaveE.svg')
print "done01"

