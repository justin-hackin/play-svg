'''This module builds composite shapes and returns xml nodes containing them'''

from playsvg.geom import *
from playsvg.element import *
import playsvg.pathshapes
from playsvg.path import *
import playsvg.color
from lxml import etree



def buildFlowerOfLife( level, radius):
    centre = Point(0,0)
    flowerGroup = etree.Element('g', id="hexagonlattice")
    
    #add centre hexagon
    circleAttributes = {'style':'stroke:black;fill:none'}
    flowerGroup.append(buildCircle(centre, radius, circleAttributes))
    distFromHex = radius*math.sin((0.5-1.0/6)*2*math.pi)/math.sin(1.0/12*2*math.pi)
    
    #creates a set of concentric hexagons
    for i in range(1,level):
        
        flowerLayerGroup = etree.Element('g', id='flowerlayer'+str(i))
        #corners of an invisible hexagon on which the concentric hexagons will be centred on
        hexagonFrame = []
        
        for j in range(6):
            hexagonFrame.append(Point().polerInit(i*radius , float(j)/6+1.0/12)) 
            
        #each line of the invisible hexagon is equally divided into n points where n is the layer number
        #hexagons are plotted on these points
        for j in range(6):
            sidePoints = []
            sidePoints.extend(getLineDivisions(hexagonFrame[j], hexagonFrame[(j+1)%6], i+1))
            for k in range(len(sidePoints)-1):
                flowerLayerGroup.append(buildCircle(sidePoints[k], radius, circleAttributes))
             
        flowerGroup.append(flowerLayerGroup)
    return flowerGroup
    

def buildHexagonLattice(level, radius):
    #add centre hexagon
    
    distFromHex = radius*math.sin((0.5-1.0/6)*2*math.pi)/math.sin(1.0/12*2*math.pi)
    latticeGroup = etree.Element('g', id="hexagonlattice")
    hexAttr = {'style':'stroke:black;fill:none'}
    latticeGroup.append(buildPath( playsvg.pathshapes.hexagon( Point(0,0),radius), hexAttr))
    #creates a set of concentric hexagons
    for i in range(1,level):
        #corners of an invisible hexagon on which the concentric hexagons will be centred on
        hexagonFrame = []
        levelGroup = etree.Element('g', id='level'+str(i))
        for j in range(6):
            
            hexagonFrame.append(PolerPoint(i*distFromHex , float(j)/6+1.0/12).convertToCartesian()) 
            #FIXME: do trig to figure out the perfect ratio for the angle in the PolerPoint     
        
        #each line of the invisible hexagon is equally divided into n points where n is the layer number
        #hexagons are plotted on these points
        for j in range(6):
            sidePoints = []
            sidePoints.extend(getLineDivisions(hexagonFrame[j], hexagonFrame[(j+1)%6], i+1))
            for k in range(len(sidePoints)-1):
                levelGroup.append(buildPath(playsvg.pathshapes.hexagon(sidePoints[k], radius),hexAttr  ))
        latticeGroup.append(levelGroup)
        
    return latticeGroup

def buildMetcalfeStar(numVertices, radius):
    '''Named after Metcalfe's Law, this function draws a fully connected graph with vertices equally spaced from each other and equidistant from the centre point'''
    starGroup = etree.Element('g', id='metcalfestar')
    lineAttrs = {'style':'stroke:black;fill:none'}
    #define vertices
    vertices = []
    for i in range(numVertices):
        vertices.append(Point().polerInit(radius, float(i)/numVertices))
    #connect each vertex to every other vertex
    for i in range(numVertices):
        for j in range(numVertices):
            if i != j : starGroup.append(buildLine( vertices[i], vertices[j], lineAttrs))
    return starGroup
    
def buildTriangularGrid( levels, sideLength):
    '''creates a triangular grid bounded by a large triangle, grouped into upward pointing and downward pointing triangles '''
    gridPoints = createTriangularGrid(Point(0,0), sideLength, levels)
    gridGroup = etree.Element('g', id='triangulargrid')
    triAttrs = {'style':'stroke:black;fill:none'}
    
    upwardTriangles = etree.Element('g', id='upwardtriangles')
    for i in range(levels-1):
        for j in range(i+1):
            triangulatePath = PathData()
            apex = gridPoints[i][j]
            leftBase = gridPoints[i+1][j]
            rightBase = gridPoints[i+1][j+1]
            triangulatePath.moveTo(apex).lineTo(leftBase).lineTo(rightBase).closePath()
            upwardTriangles.append(buildPath( triangulatePath, triAttrs))
    gridGroup.append(upwardTriangles)
    
    downwardTriangles = etree.Element('g', id='downwardtriangles')
    for i in range(1, levels-1):
        for j in range(i):
            triangulatePath = PathData()
            leftArm = gridPoints[i][j]
            rightArm = gridPoints[i][j+1]
            balance = gridPoints[i+1][j+1]
            triangulatePath.moveTo(leftArm).lineTo(rightArm).lineTo(balance).closePath()
            downwardTriangles.append(buildPath(triangulatePath, triAttrs))
    gridGroup.append(downwardTriangles)
    contPath = PathData().moveTo(Point(0,0)).lineTo(gridPoints[-1][0]).lineTo(gridPoints[-1][-1]).closePath()
    gridGroup.append(buildPath(contPath, triAttrs ))
    gridGroup.set('transform', 'rotate(180)')
    return gridGroup

def buildDiscreteColorGrad(intervals, startColor, endColor,  size):
    """creates a series of vertically-stacked boxes with a fill color changing incrementally from one color to another"""
    colorGradation = playsvg.color.tupleGradient(playsvg.color.hexToRGB(startColor), playsvg.color.hexToRGB(endColor),intervals )
    gradBoxGroup = etree.Element('g', id='discrete_gradation')
    boxSize = float(size)/intervals
    for i in range(intervals):
        gradBoxGroup.append(buildRect(Point(0,i*boxSize), boxSize, boxSize, {'style':'stroke:black;fill:'+colorGradation[i]} ))
    return gradBoxGroup
    
    
def buildOffsetRadialGrid(layers, spokes, layerSpacing, startRadius):
    """creates a grid similar to the pattern made in a dreamcatcher"""
    plots = createOffsetRadialGrid(layers+2, spokes, startRadius, layerSpacing)
    
    paths = []
    gridGroup = etree.Element('g', id='offsetradialgrid')
    diamondEvenGroup = etree.Element('g', id='even')
    diamondOddGroup = etree.Element('g', id='odd')
    for ring in range(layers+1,1,-1):
        diamondPath = PathData()
        
        if ring % 2 == 0:
            diamondGroup = diamondEvenGroup
        else:
            diamondGroup = diamondOddGroup
    
        
        for spoke in range(spokes):
            diamondPath = PathData()
            diamondPath.moveTo(plots[ring][spoke])
            diamondPath.lineTo(plots[ring-1][(spoke+1)%spokes])
            diamondPath.lineTo(plots[ring-2][(spoke+1)%spokes])
            diamondPath.lineTo(plots[ring-1][spoke])
            diamondPath.closePath()
            diamondGroup.append(buildPath( diamondPath, {'style':'fill:none;stroke:black'}))
            
    gridGroup.append(diamondEvenGroup)
    gridGroup.append(diamondOddGroup)
    return gridGroup

def buildRadialGrid( layers, spokes, layerSpacing, startRadius):
    """creates a shape similar to a radial grid, but with intersections having only straight lines in between them"""
    
    plots = createRadialGrid(layers+1, spokes, startRadius, layerSpacing)
    
    paths = []
    gridGroup = etree.Element('g', id='radialgrid')
    boxEvenGroup = etree.Element('g', id='even')
    boxEvenGroup = etree.Element('g', id='odd')
    for ring in range(layers,0,-1):
        boxPath = PathData()
        
        if ring % 2 == 0:
            diamondGroup = boxEvenGroup
        else:
            diamondGroup = boxEvenGroup
    
        
        for spoke in range(spokes):
            boxPath = PathData()
            boxPath.moveTo(plots[ring][spoke])
            boxPath.lineTo(plots[ring-1][spoke])
            boxPath.lineTo(plots[ring-1][(spoke+1)%spokes])
            boxPath.lineTo(plots[ring][(spoke+1)%spokes])
            boxPath.closePath()
            diamondGroup.append(buildPath( boxPath, {'style':'fill:none;stroke:black'}))
            
    gridGroup.append(boxEvenGroup)
    gridGroup.append(boxEvenGroup)
    return gridGroup
    
#FIXME: test this
def buildHexagonalCube(radius):
    """creates an image of a cube with 1 corner in the centre, forming a hexagon outline""" 
    outerCorners = createRadialPlots(Point(0, 0), radius,  6)
    hexBoxGroup = etree.Element('g', id='hexbox')
    boxFace1 = PathData().moveTo(outerCorners[5]).lineTo(outerCorners[0]).lineTo(outerCorners[1]).lineTo(Point(0,0)).closePath()
    boxFace2 = PathData().moveTo(outerCorners[1]).lineTo(outerCorners[2]).lineTo(outerCorners[3]).lineTo(Point(0,0)).closePath()
    boxFace3 = PathData().moveTo(outerCorners[3]).lineTo(outerCorners[4]).lineTo(outerCorners[5]).lineTo(Point(0,0)).closePath()
    boxStyle = {'style':'fill:white; stroke:black; stroke-width:6'}
    hexBoxGroup.append(buildPath(boxFace1,boxStyle ))
    hexBoxGroup.append(buildPath(boxFace2, boxStyle))
    hexBoxGroup.append(buildPath(boxFace3, boxStyle))
    return hexBoxGroup


def buildOpenBox(outerSize, innerSize):
    """returns an image of looking down into a box in 3D """
    openBoxGroup = etree.Element('g', id='openbox')
    innerCorners = [Point(innerSize, innerSize), Point(innerSize*-1, innerSize), Point(innerSize*-1, innerSize*-1), Point(innerSize, innerSize*-1)]
    outerCorners = [Point(outerSize, outerSize), Point(outerSize*-1, outerSize), Point(outerSize*-1, outerSize*-1), Point(outerSize, outerSize*-1)]
    paths = []
    paths.append(PathData().moveTo(outerCorners[0]).lineTo(outerCorners[1]).lineTo(innerCorners[1]).lineTo(innerCorners[0]).closePath())
    paths.append(PathData().moveTo(outerCorners[1]).lineTo(outerCorners[2]).lineTo(innerCorners[2]).lineTo(innerCorners[1]).closePath())
    paths.append(PathData().moveTo(outerCorners[2]).lineTo(outerCorners[3]).lineTo(innerCorners[3]).lineTo(innerCorners[2]).closePath())
    paths.append(PathData().moveTo(outerCorners[3]).lineTo(outerCorners[0]).lineTo(innerCorners[0]).lineTo(innerCorners[3]).closePath())
    for i in range(len(paths)):
        openBoxGroup.append(buildPath( paths[i], {'style':'fill:none;stroke:black;stroke-width:2'}))
    return openBoxGroup
    
def buildCircleCardioid(circles, radius):
    '''Creates a series of circles whose envelope forms a cartoid.\
    Inspired by http://mathworld.wolfram.com/Cardioid.html. '''
    
    cardioidGroup = etree.Element('g', id='cardiod')
        
    centrePoint = Point(0,0)
    focusPoint = Point().polerInit(radius,0)
    
    for i in range(circles):
        currentPoint = Point().polerInit(radius, float(i)/circles)
        distance = distanceBetween(focusPoint, currentPoint)
        cardioidGroup.append(buildCircle( currentPoint, distance, {u'fill':u'none',u'style':u'fill:none;stroke:black;stroke-width:3;'}))
    return cardioidGroup

def buildStringArt( divs, size):
    stringArtGroup =etree.Element('g', id='stringart')
    corners = []
    corners.append(Point(size,size))
    corners.append(Point(size, -1*size))
    corners.append(Point(-1*size, -1*size))
    corners.append(Point(-1*size, size))
    points = []
    
    for i in range(0,4):
        points = []
        points.append(getLineDivisions(corners[i], corners[(i+1)%4],divs) )
        points.append(getLineDivisions(corners[(i+1)%4], corners[(i+2)%4], divs))
        
        for j in range(0, int(math.floor(divs/2.0))):
            stringArtGroup.append(buildLine(points[0][j+int(math.ceil(divs/2.0))], points[1][j+1], {'style':'stroke:black;fill:none'}))
    
    return stringArtGroup


def buildSubunitWheel( pssSpoke, pssLayer, axleRadius, wheelRadius, attrList=()):
    '''Builds a wheel with spokes of varying widths to represent subunit division i.e. ruler ticks.  
    pss is represented as a list of (division, width) pairs (division being > 1).  The first division divides the wheel 
    into any number of sections.  Every subsequent division divides all sections into the 
    specified number of subsections.'''
    wheelGroup = etree.Element('g', id='wheelgroup')
    wheelGroup.append(buildCircle(Point(0,0), axleRadius,{u'fill':u'none', u'stroke-width':u'13', u'stroke':u'black', u'stroke-opacity':u'1'}))
    wheelGroup.append(buildCircle(Point(0,0), wheelRadius,{u'fill':u'none', u'stroke-width':u'13', u'stroke':u'black', u'stroke-opacity':u'1'}))
    
    #Spoke subdivision
    dividedInto=1
    print len(pssSpoke)
    for i in range(0,len(pssSpoke)):
        if i != 0: 
            divdedInto = dividedInto*pssSpoke[i-1][0]
        toDivideInto = dividedInto*pssSpoke[i][0]
        
        for j in range(0, toDivideInto):
            if j % (toDivideInto/dividedInto)  != 0 or i==0 :  #if there is no division made at j or we're in the first round of divisions make one
                print j
                wheelGroup.append( \
                buildLine(Point().polerInit(axleRadius, float(j)/toDivideInto), \
                    Point().polerInit(wheelRadius, float(j)/toDivideInto), \
                    {u'style' :'stroke:black;fill:none; stroke-width:'+str(pssSpoke[i][1])})) 
        dividedInto=toDivideInto
    
    # Layer subdivision
    dividedInto=1
    totalRadius = wheelRadius - axleRadius
    for i in range(0,len(pssLayer)):
        if i != 0: 
            divdedInto = dividedInto*pssLayer[i-1][0]
        toDivideInto = dividedInto*pssLayer[i][0]
        for j in range(0, toDivideInto):
            if j % (toDivideInto/dividedInto)  != 0 or i==0 :  #if there is no division made at j or we're in the first round of divisions make one
                print j
                wheelGroup.append( \
                buildCircle(Point(0,0), \
                    (axleRadius + totalRadius*(float(j)/toDivideInto)) , \
                    {'style':'fill:none;stroke:black;stroke-width:'+str(pssLayer[i][1])})) 
        dividedInto=toDivideInto
                
    
    return wheelGroup 

def buildCircularWeave(numPoints, radius, gap, extent):
    """creates a pattern of two interlocking waves moving around a circle"""
    weaveGroup = etree.Element('g', id='weavegroup') 
    centrePoint = Point(0,0)
    #extent = 0.5
    #gap = 0.1
    tilt = 1.0/numPoints + gap 
    otherTilt = 1- gap
       
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
    weaveGroup.append(buildPath( path1, {'style':'stroke:black;fill:none'}))
    weaveGroup.append(buildPath( path2, {'style':'stroke:black;fill:none'}))
    return weaveGroup

def buildSymetricPetalFlower(petals, centreHoopRadius, flowerRadius, rvbdVector, insideOut=0):
    """creates a flower pattern with petals formed by two mirrored bezier curves of a given RVBD (see path methods for more details on RVBD)"""
    flowerGroup = etree.Element('g', id='flower') 
    #insideOut determines whether the petal from the centreHoop moves toward the centre of the CentreHoop (if == 1)/
    #or away from the centre (when insideOut == 0)
    if insideOut : offsetAngle = 0.5
    else: offsetAngle = 0
    for i in range(0, petals):
        innerPt = Point().polerInit(centreHoopRadius,float(i)/petals)
        outerPt = Point().polerInit(flowerRadius,(float(i)/petals+offsetAngle))
        flowerGroup.append(buildPath(playsvg.pathshapes.symetricBezierPetal(innerPt, outerPt, rvbdVector), {'style':'fill:none;stroke:black'}))
    return flowerGroup







     

##Code not compatible with new Document to replace Base
###FIXME: create method for creating true vesica pisces shapes
##

##    
##def buildSubunitTicks(base, pss, startX, endX,  height):
##    '''Builds a wheel with spokes of varying widths to represent subunit division i.e. ruler ticks.  
##    pss is represented as a list of (division, width) pairs (division being > 1).  The first division divides the wheel 
##    into any number of sections.  Every subsequent division divides all sections into the 
##    specified number of subsections.'''
##    tickGroup = base.dok.xml_element(u'g')
##    start = Point(startX,0)
##    end = Point(endX, 0)
##    dividedInto=1
##    print len(pss)
##    for i in range(0,len(pss)):
##        print "ieeee" + str(i)
##        if i != 0: 
##            divdedInto = dividedInto*pss[i-1][0]
##        toDivideInto = dividedInto*pss[i][0]
##        print "dividedinto"+str(dividedInto)
##        print "todividedinto:" + str(toDivideInto)
##        for j in range(0, toDivideInto):
##            if j % (toDivideInto/dividedInto)  != 0 or i==0 :  #if there is no division made at j or we're in the first round of divisions make one
##                print j
##                basePoint = getLineDivision(start, end, float(j)/toDivideInto)
##                tickGroup.xml_append(buildLine(base, basePoint,  Point(basePoint.x, pss[i][1]*height) ) )
##        dividedInto=toDivideInto
##    tickGroup.xml_append(buildLine(base, Point(endX,0),  Point(endX, pss[0][1]*height) ) )
##    return tickGroup
##
##    
##def buildPolyRadial(base, sides, shapeRadius, spokeRadius, ctrlLengthRatio, ctrlAngle, numSpokes):
##    polyTips = []
##    controlPoints = []
##    spokeRadi = []
##    for i in range(sides):
##        polyTips.append(PolerPoint(shapeRadius, float(i)/sides).convertToCartesian())
##        spokeRadi.append(PolerPoint(spokeRadius, (i+0.5)/sides).convertToCartesian())
##            
##    sideDistance = distanceBetween(polyTips[0], polyTips[1])
##    pathData = PathData().moveTo(polyTips[0])
##        
##    for i in range(sides):
##        startPoint = polyTips[i]
##        endPoint = polyTips[(i+1) % sides]
##        ctrlPt1 = hingePlot(startPoint, endPoint, ctrlLengthRatio*sideDistance, ctrlAngle)
##        ctrlPt2 = hingePlot(endPoint, startPoint, ctrlLengthRatio*sideDistance, -1*ctrlAngle)
##        pathData.cubicBezier(ctrlPt1, ctrlPt2, endPoint)
##        sideTicks = getDiscreteCubicBezier(startPoint, ctrlPt1, ctrlPt2, endPoint, numSpokes)
##        for j in range(len(sideTicks)):
##            spireGroup.xml_append(buildLine(base, sideTicks[j], spokeRadi[i]))
##    
##    spireGroup.xml_append(buildPath(base, pathData))
##    return spireGroup
##    
    
##
##    
##

##    
##def buildCubicBezierLengthTest(base,P1,P2,P3,P4):
##    '''places a bezier only of length estimated by approximation (using stroke-dashoffset atribute) on top of the full bezier to test the accuracy of estimation'''
##    length = cubicBezierLength(P1,P2,P3,P4)
##    print length
##    theNode = base.dok.xml_element(u'g')
##    realPath = PathData()
##    realPath.moveTo(P1)
##    realPath.cubicBezier(P2,P3,P4)
##    clipPath = buildPath(base, realPath, attributes={u'stroke-dasharray':unicode(length),u'stroke-dashoffset': unicode(length), u'stroke':u'red',u'stroke-opacity':u'0.5'} )
##    fullPath = buildPath(base, realPath, attributes={ u'stroke':u'black', u'stroke-opacity':u'0.5'} )
##    theNode.xml_append(clipPath)
##    theNode.xml_append(fullPath)
##    return theNode
##    ##def buildCircleSpiral(base, beginRadius, endRadius, beginCircleSize, endCircleSize    
##
   
