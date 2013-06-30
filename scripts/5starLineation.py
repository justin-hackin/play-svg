"""outline for Image of a crop circle design found at T+0:49 in http://video.google.ca/videoplay?docid=2560466181031386448&q=sacred+geometry&total=308&start=0&num=10&so=0&type=search&plindex=9 """
from playsvg.document import *
from playsvg.element import *
from playsvg.path import *
import playsvg.pathshapes

thickness = 60
width = 100
angal = 30.0/360

def makeSectionizedCentrelessPie(docu,sections, innerRadius, outerRadius):
    pieNode = docu.makeGroup()
    pieNode.appendChild(buildCircle(docu, Point(), innerRadius,  {'style':'stroke:black;fill:none'}))
    pieNode.appendChild(buildCircle(docu, Point(), outerRadius,  {'style':'stroke:black;fill:none'}))
    linePath = PathData()
    for i in range(sections):
        linePath.moveTo(Point().polerInit(innerRadius, float(i)/sections))\
        .lineTo(Point().polerInit(outerRadius, float(i)/sections))
    pieNode.appendChild(buildPath(docu, linePath, {'style':'stroke:black;fill:none'}))
    return pieNode

def makeCircularCircincirc(docu, numCirc, placementRadius, insideRadius, outsideRadius):
    allNode = docu.makeGroup()
    innerCirc = docu.makeGroup()
    outerCirc = docu.makeGroup()
    
    for i in range(numCirc):
        outerCirc.appendChild(buildCircle(docu, Point().polerInit(placementRadius, float(i)/numCirc), outsideRadius, {'style':'stroke:black;fill:none'}))
        innerCirc.appendChild(buildCircle(docu, Point().polerInit(placementRadius+(outsideRadius-insideRadius), float(i)/numCirc), insideRadius, {'style':'stroke:black;fill:none'}))
    allNode.appendChild(outerCirc)
    allNode.appendChild(innerCirc)
    
    
    return allNode

def makeStar(docu, starRadius):
    starPoints =5
    starTips = createRadialPlots(Point(), starRadius, starPoints)
    valleyRadiusRatio =  intersectLineLine(starTips[0], starTips[2], starTips[1], starTips[3]).convertToPoler()[0]/starRadius
    print valleyRadiusRatio
    starValleys = createRadialPlots(Point(), valleyRadiusRatio*starRadius, starPoints, passive=1)
    starPathPoints = []
    for i in range(starPoints):
        starPathPoints.append(starTips[i])
        starPathPoints.append(starValleys[i])
    return buildPath(docu, PathData().makeHull(starPathPoints), {'style':'stroke:black;fill:none'} ) 



docu = Document()
docu.appendElement(makeSectionizedCentrelessPie(docu,5, 50, 300))
docu.appendElement(makeStar(docu,300 ))
docu.appendElement(makeCircularCircincirc(docu,5, 270, 69,100 ))
docu.writeSVG('5star.svg')
