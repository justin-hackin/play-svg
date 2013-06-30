from playsvg.document import *
from playsvg.element import *
from playsvg.path import *
from playsvg import compshapes
starRadius = 50
polygonRadius = 200
starPoints = 11
polygonPoints = createRadialPlots(Point(), polygonRadius, starPoints)
starTips = createRadialPlots(Point(), starRadius, starPoints)
valleyRadiusRatio =  intersectLineLine(starTips[0], starTips[3], starTips[4], starTips[1]).convertToPoler()[0]/starRadius
print valleyRadiusRatio
starValleys = createRadialPlots(Point(), valleyRadiusRatio*starRadius, starPoints, passive=1)
starPathPoints = []
for i in range(starPoints):
    starPathPoints.append(starTips[i])
    starPathPoints.append(starValleys[i])


docu = Document()
docu.append(buildPath( PathData().makeHull(starPathPoints), {'style':'stroke:black;fill:none'}))
docu.append(buildPath( PathData().makeHull(polygonPoints), {'style':'stroke:black;fill:none'}))
docu.append
docu.writeSVG("starToPoly11.svg")
