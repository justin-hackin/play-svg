'''This module builds composite shapes and returns xml nodes containing them'''

from playsvg.geom import *
from playsvg.element import *
import playsvg.pathshapes
from playsvg.path import *
import playsvg.color



def buildFlowerOfLife(docu, level, radius):
    centre = Point(0,0)
    flowerGroup = docu.makeGroup('floweroflife')
    
    #add centre hexagon
    circleAttributes = {'style':'stroke:black;fill:none'}
    flowerGroup.appendChild(buildCircle(docu,centre, radius, circleAttributes))
    distFromHex = radius*math.sin((0.5-1.0/6)*2*math.pi)/math.sin(1.0/12*2*math.pi)
    
    #creates a set of concentric hexagons
    for i in range(1,level):
        
        flowerLayerGroup = docu.makeGroup('flowerlayer'+str(i))
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
                flowerLayerGroup.appendChild(buildCircle(docu,sidePoints[k], radius, circleAttributes))
             
        flowerGroup.appendChild(flowerLayerGroup)
    return flowerGroup
    

def buildHexagonLattice(docu,level, radius):
    #add centre hexagon
    
    distFromHex = radius*math.sin((0.5-1.0/6)*2*math.pi)/math.sin(1.0/12*2*math.pi)
    latticeGroup = docu.makeGroup('hexagonlattice')
    hexAttr = {'style':'stroke:black;fill:none'}
    latticeGroup.appendChild(buildPath(docu, playsvg.pathshapes.hexagon( Point(0,0),radius), hexAttr))
    #creates a set of concentric hexagons
    for i in range(1,level):
        #corners of an invisible hexagon on which the concentric hexagons will be centred on
        hexagonFrame = []
        levelGroup = docu.makeGroup('level'+str(i))
        for j in range(6):
            
            hexagonFrame.append(PolerPoint(i*distFromHex , float(j)/6+1.0/12).convertToCartesian()) 
            #FIXME: do trig to figure out the perfect ratio for the angle in the PolerPoint     
        
        #each line of the invisible hexagon is equally divided into n points where n is the layer number
        #hexagons are plotted on these points
        for j in range(6):
            sidePoints = []
            sidePoints.extend(getLineDivisions(hexagonFrame[j], hexagonFrame[(j+1)%6], i+1))
            for k in range(len(sidePoints)-1):
                levelGroup.appendChild(buildPath(docu, playsvg.pathshapes.hexagon(sidePoints[k], radius),hexAttr  ))
        latticeGroup.appendChild(levelGroup)
        
    return latticeGroup

def buildMetcalfeStar(docu, numVertices, radius):
    '''Named after Metcalfe's Law, this function draws a fully connected graph with vertices equally spaced from each other and equidistant from the centre point'''
    starGroup = docu.makeGroup('metcalfestar')
    lineAttrs = {'style':'stroke:black;fill:none'}
    #define vertices
    vertices = []
    for i in range(numVertices):
        vertices.append(Point().polerInit(radius, float(i)/numVertices))
    #connect each vertex to every other vertex
    for i in range(numVertices):
        for j in range(numVertices):
            if i != j : starGroup.appendChild(buildLine(docu, vertices[i], vertices[j], lineAttrs))
    return starGroup
    
def buildTriangularGrid(docu, levels, sideLength):
    '''creates a triangular grid bounded by a large triangle, grouped into upward pointing and downward pointing triangles '''
    gridPoints = createTriangularGrid(Point(0,0), sideLength, levels)
    gridGroup = docu.makeGroup('triangulargrid')
    triAttrs = {'style':'stroke:black;fill:none'}
    
    upwardTriangles = docu.makeGroup('upwardtriangles')
    for i in range(levels-1):
        for j in range(i+1):
            triangulatePath = PathData()
            apex = gridPoints[i][j]
            leftBase = gridPoints[i+1][j]
            rightBase = gridPoints[i+1][j+1]
            triangulatePath.moveTo(apex).lineTo(leftBase).lineTo(rightBase).closePath()
            upwardTriangles.appendChild(buildPath(docu, triangulatePath, triAttrs))
    gridGroup.appendChild(upwardTriangles)
    
    downwardTriangles = docu.makeGroup('downwardtriangles')
    for i in range(1, levels-1):
        for j in range(i):
            triangulatePath = PathData()
            leftArm = gridPoints[i][j]
            rightArm = gridPoints[i][j+1]
            balance = gridPoints[i+1][j+1]
            triangulatePath.moveTo(leftArm).lineTo(rightArm).lineTo(balance).closePath()
            downwardTriangles.appendChild(buildPath(docu, triangulatePath, triAttrs))
    gridGroup.appendChild(downwardTriangles)
    contPath = PathData().moveTo(Point(0,0)).lineTo(gridPoints[-1][0]).lineTo(gridPoints[-1][-1]).closePath()
    gridGroup.appendChild(buildPath(docu, contPath, triAttrs ))
    gridGroup.setAttribute('transform', 'rotate(180)')
    return gridGroup

def buildDiscreteColorGrad(docu,intervals, startColor, endColor,  size):
    """creates a series of vertically-stacked boxes with a fill color changing incrementally from one color to another"""
    colorGradation = playsvg.color.tupleGradient(playsvg.color.hexToRGB(startColor), playsvg.color.hexToRGB(endColor),intervals )
    gradBoxGroup = docu.makeGroup('discrete_gradation')
    boxSize = float(size)/intervals
    for i in range(intervals):
        gradBoxGroup.appendChild(buildRect(docu, Point(0,i*boxSize), boxSize, boxSize, {'style':'stroke:black;fill:'+colorGradation[i]} ))
    return gradBoxGroup
    
    
def buildOffsetRadialGrid(docu, layers, spokes, layerSpacing, startRadius):
    """creates a grid similar to the pattern made in a dreamcatcher"""
    plots = createOffsetRadialGrid(layers+2, spokes, startRadius, layerSpacing)
    
    paths = []
    gridGroup = docu.makeGroup('offsetradialgrid')
    diamondEvenGroup = docu.makeGroup('even')
    diamondOddGroup = docu.makeGroup('odd')
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
            diamondGroup.appendChild(buildPath(docu, diamondPath, {'style':'fill:none;stroke:black'}))
            
    gridGroup.appendChild(diamondEvenGroup)
    gridGroup.appendChild(diamondOddGroup)
    return gridGroup

def buildRadialGrid(docu, layers, spokes, layerSpacing, startRadius):
    """creates a shape similar to a radial grid, but with intersections having only straight lines in between them"""
    
    plots = createRadialGrid(layers+1, spokes, startRadius, layerSpacing)
    
    paths = []
    gridGroup = docu.makeGroup('radialgrid')
    boxEvenGroup = docu.makeGroup('even')
    boxEvenGroup = docu.makeGroup('odd')
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
            diamondGroup.appendChild(buildPath(docu, boxPath, {'style':'fill:none;stroke:black'}))
            
    gridGroup.appendChild(boxEvenGroup)
    gridGroup.appendChild(boxEvenGroup)
    return gridGroup
    
#FIXME: test this
def buildHexagonalCube(docu, radius):
    """creates an image of a cube with 1 corner in the centre, forming a hexagon outline""" 
    outerCorners = createRadialPlots(Point(0, 0), radius,  6)
    hexBoxGroup = docu.makeGroup("hexbox")
    boxFace1 = PathData().moveTo(outerCorners[5]).lineTo(outerCorners[0]).lineTo(outerCorners[1]).lineTo(Point(0,0)).closePath()
    boxFace2 = PathData().moveTo(outerCorners[1]).lineTo(outerCorners[2]).lineTo(outerCorners[3]).lineTo(Point(0,0)).closePath()
    boxFace3 = PathData().moveTo(outerCorners[3]).lineTo(outerCorners[4]).lineTo(outerCorners[5]).lineTo(Point(0,0)).closePath()
    boxStyle = {'style':'fill:white; stroke:black; stroke-width:6'}
    hexBoxGroup.appendChild(buildPath(docu,boxFace1,boxStyle ))
    hexBoxGroup.appendChild(buildPath(docu,boxFace2, boxStyle))
    hexBoxGroup.appendChild(buildPath(docu,boxFace3, boxStyle))
    return hexBoxGroup


def buildOpenBox(docu, outerSize, innerSize):
    """returns an image of looking down into a box in 3D """
    openBoxGroup = docu.makeGroup("openbox")
    innerCorners = [Point(innerSize, innerSize), Point(innerSize*-1, innerSize), Point(innerSize*-1, innerSize*-1), Point(innerSize, innerSize*-1)]
    outerCorners = [Point(outerSize, outerSize), Point(outerSize*-1, outerSize), Point(outerSize*-1, outerSize*-1), Point(outerSize, outerSize*-1)]
    paths = []
    paths.append(PathData().moveTo(outerCorners[0]).lineTo(outerCorners[1]).lineTo(innerCorners[1]).lineTo(innerCorners[0]).closePath())
    paths.append(PathData().moveTo(outerCorners[1]).lineTo(outerCorners[2]).lineTo(innerCorners[2]).lineTo(innerCorners[1]).closePath())
    paths.append(PathData().moveTo(outerCorners[2]).lineTo(outerCorners[3]).lineTo(innerCorners[3]).lineTo(innerCorners[2]).closePath())
    paths.append(PathData().moveTo(outerCorners[3]).lineTo(outerCorners[0]).lineTo(innerCorners[0]).lineTo(innerCorners[3]).closePath())
    for i in range(len(paths)):
        openBoxGroup.appendChild(buildPath(docu, paths[i], {'style':'fill:none;stroke:black;stroke-width:2'}))
    return openBoxGroup
    
def buildCircleCardioid(docu, circles, radius):
    '''Creates a series of circles whose envelope forms a cartoid.\
    Inspired by http://mathworld.wolfram.com/Cardioid.html. '''
    
    cardioidGroup = docu.makeGroup()
        
    centrePoint = Point(0,0)
    focusPoint = Point().polerInit(radius,0)
    
    for i in range(circles):
        currentPoint = Point().polerInit(radius, float(i)/circles)
        distance = distanceBetween(focusPoint, currentPoint)
        cardioidGroup.appendChild(buildCircle(docu, currentPoint, distance, {u'fill':u'none',u'style':u'fill:none;stroke:black;stroke-width:3;'}))
    return cardioidGroup

def buildStringArt(docu, divs, size):
    stringArtGroup = docu.makeGroup()
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
            stringArtGroup.appendChild(buildLine(docu,points[0][j+int(math.ceil(divs/2.0))], points[1][j+1], {'style':'stroke:black;fill:none'}))
    
    return stringArtGroup


def buildSubunitWheel(docu, pssSpoke, pssLayer, axleRadius, wheelRadius, attrList=()):
    '''Builds a wheel with spokes of varying widths to represent subunit division i.e. ruler ticks.  
    pss is represented as a list of (division, width) pairs (division being > 1).  The first division divides the wheel 
    into any number of sections.  Every subsequent division divides all sections into the 
    specified number of subsections.'''
    wheelGroup = docu.makeGroup()
    wheelGroup.appendChild(buildCircle(docu,Point(0,0), axleRadius,{u'fill':u'none', u'stroke-width':u'13', u'stroke':u'black', u'stroke-opacity':u'1'}))
    wheelGroup.appendChild(buildCircle(docu,Point(0,0), wheelRadius,{u'fill':u'none', u'stroke-width':u'13', u'stroke':u'black', u'stroke-opacity':u'1'}))
    
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
                wheelGroup.appendChild( \
                buildLine(docu, \
                    Point().polerInit(axleRadius, float(j)/toDivideInto), \
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
                wheelGroup.appendChild( \
                buildCircle(docu, \
                    Point(0,0), \
                    (axleRadius + totalRadius*(float(j)/toDivideInto)) , \
                    {'style':'fill:none;stroke:black;stroke-width:'+str(pssLayer[i][1])})) 
        dividedInto=toDivideInto
                
    
    return wheelGroup 

def buildCircularWeave(docu, numPoints, radius, gap, extent):
    """creates a pattern of two interlocking waves moving around a circle"""
    weaveGroup = docu.makeGroup()
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
    weaveGroup.appendChild(buildPath(docu, path1, {'style':'stroke:black;fill:none'}))
    weaveGroup.appendChild(buildPath(docu, path2, {'style':'stroke:black;fill:none'}))
    return weaveGroup

def buildSymetricPetalFlower(docu, petals, centreHoopRadius, flowerRadius, rvbdVector, insideOut=0):
    """creates a flower pattern with petals formed by two mirrored bezier curves of a given RVBD (see path methods for more details on RVBD)"""
    flowerGroup = docu.makeGroup()
    #insideOut determines whether the petal from the centreHoop moves toward the centre of the CentreHoop (if == 1)/
    #or away from the centre (when insideOut == 0)
    if insideOut : offsetAngle = 0.5
    else: offsetAngle = 0
    for i in range(0, petals):
        innerPt = Point().polerInit(centreHoopRadius,float(i)/petals)
        outerPt = Point().polerInit(flowerRadius,(float(i)/petals+offsetAngle))
        flowerGroup.appendChild(buildPath(docu,playsvg.pathshapes.symetricBezierPetal(innerPt, outerPt, rvbdVector), {'style':'fill:none;stroke:black'}))
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
   
