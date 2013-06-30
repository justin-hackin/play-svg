from playsvg import document
from playsvg import pathshapes
import math
from playsvg.geom import *
from playsvg.element import *
from playsvg.path import *
from playsvg.gradient import *
from playsvg import gradshape

docu = document.Document()
outerRadius = 260
borderWidth = 20
borderSlices = 12
borderPoints = createRadialPlots(Point(0,0), outerRadius+borderWidth, 5)
outerStarPoints = createRadialPlots(Point(0,0), outerRadius, 5)
midRadius = intersectLineLine(outerStarPoints[0], outerStarPoints[3], outerStarPoints[4], outerStarPoints[1]).convertToPoler().r
midStarPoints = createRadialPlots(Point(0,0), midRadius, 5, passive = 1)
innerRadius =  intersectLineLine(midStarPoints[0], midStarPoints[3], midStarPoints[4], midStarPoints[1]).convertToPoler().r
innerStarPoints = createRadialPlots(Point(0,0), innerRadius, 5)

upGradientColors = [  '#a500ff', '#faff00']
upGradient = Gradient('upgrad000')
upGradient.createBalancedGradient(upGradientColors)
docu.append(upGradient.createDefinition(docu))
upGradientColors.reverse()
#upGradients order becomes reversed
downGradientColors = upGradientColors
downGradient = Gradient('downgrad000')
downGradient.createBalancedGradient(downGradientColors)
docu.append(downGradient.createDefinition(docu))

#starBackground
##backing = PathData().makeHull(innerStarPoints)
##docu.append( buildPath( backing, {u'fill':u'black'}))


#outer star rays
starRaysGroup = docu.makeGroup()
#outerRayAttributes = {u'style':u'fill: white; stroke:none'}
for i in range(5):
    ##starPointData = PathData().moveTo(outerStarPoints[i]).lineTo(midStarPoints[i]).lineTo(midStarPoints[(i-1)%5]).closePath()
    ##outerStarRaysGroup.append(buildPath( starPointData,  outerRayAttributes))
    points = [outerStarPoints[i], midStarPoints[i], midStarPoints[(i-1)%5]]
    starRaysGroup.append(gradshape.polygonGradient( points, upGradient, 'outspire'+str(i)))

# inner star rays

innerRayAttributes = {u'style':u'fill: white; stroke:none'}
for i in range(5):
    ##starPointData = PathData().moveTo(midStarPoints[i]).lineTo(innerStarPoints[i]).lineTo(innerStarPoints[(i+1)%5]).closePath()
    ##outerStarRaysGroup.append(buildPath( starPointData,  innerRayAttributes))
    points = [midStarPoints[i], innerStarPoints[i], innerStarPoints[(i+1)%5] ]
    starRaysGroup.append(gradshape.polygonGradient( points, upGradient, 'inspire'+str(i)))

docu.append(starRaysGroup)

#surrounding triangles
betweenTrianglesGroup = docu.makeGroup()
innerRayAttributes = {u'style':u'fill: black; stroke:none'}
for i in range(5):
    ##starPointData = PathData().moveTo(outerStarPoints[i]).lineTo(midStarPoints[i]).lineTo(outerStarPoints[(i+1)%5]).closePath()
    ##betweenTrianglesGroup.append(buildPath( starPointData, innerRayAttributes))
    points =  [outerStarPoints[i], midStarPoints[i], outerStarPoints[(i+1)%5] ]
    betweenTrianglesGroup.append(gradshape.polygonGradient( points, downGradient, 'outback'+str(i)))
for i in range(5):
##    starPointData = PathData().moveTo(midStarPoints[i]).lineTo(innerStarPoints[(i+1)%5]).lineTo(midStarPoints[(i+1)%5]).closePath()
##    betweenTrianglesGroup.append(buildPath( starPointData,  innerRayAttributes))
    points = [midStarPoints[i], innerStarPoints[(i+1)%5], midStarPoints[(i+1)%5] ]
    betweenTrianglesGroup.append(gradshape.polygonGradient( points, downGradient, 'inback'+str(i)))
    
docu.append(betweenTrianglesGroup)

#inner pentagon
betweenTrianglesGroup.append(gradshape.polygonGradient( innerStarPoints, downGradient, 'center'+str(i)))

###border
##borderAttributes = {u'style':u'fill: black; stroke:white'}
##borderBoxesGroup = docu.makeGroup()
##
##for i in range(5):
##    outerBorderPoints = getLineDivisions(borderPoints[i], borderPoints[(i+1)%5], borderSlices)
##    innerBorderPoints =  getLineDivisions(outerStarPoints[i], outerStarPoints[(i+1)%5], borderSlices)
##    for i in range(borderSlices -1):
##        boxPath = PathData().moveTo(outerBorderPoints[i]).lineTo(outerBorderPoints[i+1]).lineTo(innerBorderPoints[i+1]).lineTo(innerBorderPoints[i]).closePath()
##        borderBoxesGroup.append(buildPath( boxPath,  borderAttributes))
##docu.append(borderBoxesGroup)
##
###inward drawing lines
##vortexAttributes = {u'style':u'fill: none; stroke:yellow; stroke-opacity:0.4'}
##vortexBoxesGroup = docu.makeGroup()
##for i in range(5):
##    leftVortexPoints = getLineDivisions(outerStarPoints[i], innerStarPoints[i], borderSlices)
##    rightVortexPoints =  getLineDivisions(outerStarPoints[(i+1)%5], innerStarPoints[(i+1)%5], borderSlices)
##    for i in range(borderSlices -1):
##        boxPath = PathData().moveTo(leftVortexPoints[i]).lineTo(leftVortexPoints[i+1]).lineTo(rightVortexPoints[i+1]).lineTo(rightVortexPoints[i]).closePath()
##        vortexBoxesGroup.append(buildPath( boxPath,  vortexAttributes))
##docu.append(vortexBoxesGroup)

###centre spires
##
##
##spireAttributes = {u'style':u'fill: black; stroke:white; stroke-width:0.3'}
##spireGroup = docu.makeGroup()
##for i in range(5):
##    sidePoints = getLineDivisions(innerStarPoints[i], innerStarPoints[(i+1)%5], borderSlices)
##   
##    for i in range(borderSlices -1):
##        boxPath = PathData().moveTo(sidePoints[i]).lineTo(sidePoints[i+1]).lineTo(Point(0,0)).closePath()
##        spireGroup.append(buildPath( boxPath, attributes = spireAttributes))
##docu.append(spireGroup)

##pentagramRadius = 6
##pentagramAttributes = {u'stroke':u'black', u'fill':u'none'}
##pentagramGroup = docu.makeGroup()
##pentagramPath = pathshapes.starPolygon(5,2,pentagramRadius)
##pentagramGroup.append(buildPath( pentagramPath, pentagramAttributes))
##pentagramGroup.append(buildCircle( Point(0,0), pentagramRadius, pentagramAttributes))
##docu.append(pentagramGroup)

#proof that the pentagram does reflect the phi ratio 
spireCorner1 = intersectLineLine(outerStarPoints[0], outerStarPoints[2], outerStarPoints[4], outerStarPoints[1])
spireCorner2 = intersectLineLine(outerStarPoints[0], outerStarPoints[2], outerStarPoints[1], outerStarPoints[3])
spireLength= distanceBetween(outerStarPoints[0], spireCorner1)
traceLength = distanceBetween(outerStarPoints[0], spireCorner2)
spireRatio = traceLength/spireLength
print "Phi is : " + str(spireRatio)

#draw recursive stars on arms
startingStrokeWidth = 3.0
strokeWidth = startingStrokeWidth
#make array of star points : armStars[arm][level][point (ordered as drawn in pentagram)]
levels = 5
recursiveArmStarGroup = docu.makeGroup()
currentArmDistance = distanceBetween(spireCorner1, spireCorner2)
currentArmGapDistance = currentArmDistance
#draw outline of outermost star
outerEdges = PathData().moveTo(outerStarPoints[0])
for i in range(5):
    outerEdges.lineTo(outerStarPoints[i]).lineTo(midStarPoints[i])
outerEdges.closePath()
docu.append(buildPath( outerEdges, {'style':'stroke:black; opacity:0.3; stroke-linejoin:round; fill:none'}))

#draw centre pentagram
innerStar = PathData().moveTo(midStarPoints[0])
for i in range(5):
    innerStar.lineTo(midStarPoints[(i*2)%5])
innerStar.closePath()
docu.append(buildPath(innerStar, {'style':'stroke:black;opacity:0.3; fill:none;stroke-linejoin:round;stroke-width:'+str(strokeWidth)}))
strokeWidth *= 1.0/phi


armStars = []

for arm in range(5):
    armStars.append([])
    nextApex = innerStarPoints[arm]
    currentArmDistance = distanceBetween(spireCorner1, spireCorner2)
    currentArmGapDistance = currentArmDistance
    strokeWidth = startingStrokeWidth*1.0/phi
    for level in range(levels):
         
        leftArm = getLineDivisionDistance(midStarPoints[(arm+1)%5], outerStarPoints[arm%5], currentArmDistance )
        rightArm = getLineDivisionDistance(midStarPoints[(arm+3)%5], outerStarPoints[arm%5], currentArmDistance )
        leftFoot = getLineDivisionDistance(midStarPoints[(arm+1)%5], outerStarPoints[arm%5], currentArmDistance + (1.0/phi)*currentArmGapDistance )
        rightFoot = getLineDivisionDistance(midStarPoints[(arm+3)%5], outerStarPoints[arm%5], currentArmDistance + (1.0/phi)*currentArmGapDistance )
        pentagramPoints = [nextApex, leftFoot, rightArm, leftArm, rightFoot]
        print pentagramPoints
        armStars[-1].append(pentagramPoints)
        starPath = PathData().makeHull(pentagramPoints)
        recursiveArmStarGroup.append(buildPath( starPath, {'style':'stroke:black; fill:none; opacity:0.3; stroke-linejoin:round;stroke-width:'+str(strokeWidth)}))
        nextApex = intersectLineLine(leftArm, rightFoot, rightArm, leftFoot)    
        currentArmGapDistance *= 1.0/phi
        currentArmDistance += currentArmGapDistance
        strokeWidth *= 1.0/phi


docu.append(recursiveArmStarGroup)

mainLineAttrs = {'style':'stroke:black; fill:none; opacity:1; stroke-linejoin:round;stroke-width:5'}

#draw upright pentagram
outerStar = PathData().moveTo(outerStarPoints[0])
for i in range(5):
    outerStar.lineTo(outerStarPoints[(i*2)%5])
outerStar.closePath()
docu.append(buildPath(outerStar,mainLineAttrs))


#draw downward pentagram
innerStar = PathData().moveTo(midStarPoints[0])
for i in range(5):
    innerStar.lineTo(midStarPoints[(i*2)%5])
innerStar.closePath()
docu.append(buildPath(innerStar,mainLineAttrs))


#make border
borderPath = PathData().makeHull(outerStarPoints)
docu.append(buildPath( borderPath, mainLineAttrs))

docu.writeSVG('platonicSpirit.svg')
print "done01"

