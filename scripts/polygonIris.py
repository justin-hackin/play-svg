from playsvg import document
import playsvg.pathshapes
from playsvg.path import *
from playsvg.geom import *
from playsvg.element import *
from playsvg import color


def polygonGradientIris( position,sides, radius, divisionOfPieRotation, sideTurnings, reverse=0, passive=0):
    gradientIrisGroup = etree.Element("g")
    #calculate creepRatio from rotationAngle,
    #where rotationAngle is the angle each polygon is rotated
    #and creepRatio is the percentage of the polygon side to move from one corner to the other
    rotations = divisionOfPieRotation*sideTurnings/2
    colorGradation = color.tupleGradient((150.0/255,0,212.0/255), (1,0,212.0/255),rotations )
    pieCornerAngle = 1.0/sides*tewpi
    rotationAngle = 1.0/divisionOfPieRotation*pieCornerAngle
    
    polygonCornerAngle =  (sides-2)*math.pi/(2*sides)
    adjacentAngle = math.pi - rotationAngle - polygonCornerAngle
    
    adjacentSide = math.sin(rotationAngle)/math.sin(adjacentAngle)*radius
    innerSide = math.sin(rotationAngle)*radius/math.sin(adjacentAngle)
    outerSegmentLength = math.sin(pieCornerAngle)*radius/math.sin(polygonCornerAngle)
    print "%%%%%%%%%%%%%%%%%%%%%%%%" + str(2-2*math.cos(tewpi*1.0/sides))
    creepRatio = innerSide/outerSegmentLength
    if reverse : creepRatio = 1 - creepRatio
    
    print ">>>>>>>>>>>>>>>>>>>>"+ str(creepRatio)
    print colorGradation
    linePoints = createRadialPlots(position, radius, sides, passive=passive )
    print linePoints
    for i in range(rotations+1):
        polygonAttributes = {u'style':u'stroke:black;stroke-width:1;fill:' + unicode(colorGradation[i])}
        print str(linePoints[0])
        trianglePath = PathData().moveTo(linePoints[0])
        for j in range(1,sides):
            trianglePath.lineTo(linePoints[j])
        trianglePath.closePath()
        gradientIrisGroup.append(buildPath( trianglePath, polygonAttributes))
        newLinePoints = []
        for j in range(sides):
            newLinePoints.append(getLineDivision(linePoints[j], linePoints[(j+1)%sides], creepRatio))
        linePoints = newLinePoints
    return gradientIrisGroup

# docu = document.Document()
# docu.append(polygonGradientIris(Point(0,0),4,100, 16, 2 ))
# docu.writeSVG('squareIris.svg')

docu = document.Document()
docu.append(polygonGradientIris(Point(0,0),6,600, 16, 6 ))
docu.writeSVG('polygonIris.svg')
print "done01"


