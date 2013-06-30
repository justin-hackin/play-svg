"""outline for Image of a crop circle design found at T+0:49 in http://video.google.ca/videoplay?docid=2560466181031386448&q=sacred+geometry&total=308&start=0&num=10&so=0&type=search&plindex=9 """
from playsvg.document import *
from playsvg.element import *
from playsvg.path import *
import playsvg.pathshapes

thickness = 60
width = 100
angal = 30.0/360
starRadius = 100

docu = Document()
starPoints =5
starTips = createRadialPlots(Point(), starRadius, starPoints)
valleyRadiusRatio =  intersectLineLine(starTips[0], starTips[2], starTips[1], starTips[3]).convertToPoler()[0]/starRadius
print valleyRadiusRatio
starValleys = createRadialPlots(Point(), valleyRadiusRatio*starRadius, starPoints, passive=1)
starPathPoints = []
for i in range(starPoints):
    starPathPoints.append(starTips[i])
    starPathPoints.append(starValleys[i])

docu.append( buildPath(PathData().makeHull(starPathPoints),  {'style':'stroke:black;fill:none'}))
docu.append( buildPath(PathData().makeHull(starValleys),  {'style':'stroke:black;fill:none'}))
docu.append( buildPath(PathData().makeHull(starTips),  {'style':'stroke:black;fill:none'}))
print "what"
docu.writeSVG('5star_crissing.svg')


