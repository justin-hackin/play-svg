from playsvg.document import *
from playsvg.element import *
from playsvg.path import *

starRadius = 50
starPoints =5
starTips = createRadialPlots(Point(), starRadius, starPoints)
valleyRadiusRatio =  intersectLineLine(starTips[0], starTips[2], starTips[1], starTips[3]).convertToPoler()[0]/starRadius
print valleyRadiusRatio
starValleys = createRadialPlots(Point(), valleyRadiusRatio*starRadius, starPoints, passive=1)
starPathPoints = []
for i in range(starPoints):
    starPathPoints.append(starTips[i])
    starPathPoints.append(starValleys[i])


docu = Document()
docu.appendElement(buildPath(docu, PathData().makeHull(starPathPoints), {'style':'stroke:black;fill:none'}))
docu.appendElement(buildPath(docu, PathData().makeHull(polygonPoints), {'style':'stroke:black;fill:none'}))
docu.appendElement
docu.writeSVG("starToPoly11.svg")
