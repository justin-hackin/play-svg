"""functions for generating path objects or a particular shape"""

from playsvg.geom import *
from playsvg.element import *
from playsvg.path import *
from copy import deepcopy


def arcSpire(cornerA, cornerB, bottomCtrlHeight, topCtrlHeight):
    """a closed shaped formed by two quadradic bezier curves of varing height stacked on top of on another""" 
    spirePathData = PathData().moveTo(cornerA).QRVBD(bottomCtrlHeight, cornerB ).QRVBD(topCtrlHeight, cornerA, flipped = 1).closePath()
    return spirePathData
    
##def magneticField(pointA, pointB, layers,layerSpacing,angle):
##    fieldGroup = base.dok.xml_element(u'g')
##    for layer in range(1,layers+1):
##        bottomCtrlPt1 = extendBendPoint(pointB, pointA,  layer*layerSpacing, angle)
##        bottomCtrlPt2 = extendBendPoint(pointA, pointB, layer*layerSpacing, 1-angle)
##        topCtrlPt1 = extendBendPoint(pointA, pointB,  layer*layerSpacing, angle)
##        topCtrlPt2 = extendBendPoint(pointB, pointA, layer*layerSpacing, 1-angle)
##        fieldLayerPathData = PathData().moveTo(pointA).cubicBezier(bottomCtrlPt1, bottomCtrlPt2, pointB).cubicBezier(topCtrlPt1, topCtrlPt2, pointA).closePath()
##    return fieldLayerPathData
    
def starPolygon(x, n, radius):
    '''see Star Polygon in wikipedia for a description of the shape generated'''
    currentPoint = 0
    centrePoint = Point(0,0)
    points = []
      
    for i in range(0,x):
        points.append(Point().polerInit(radius,float(i)/x))
        
    
    starPathData = PathData().moveTo(points[0])
    while 1:
        currentPoint = (currentPoint+n) % x
        starPathData.lineTo(points[currentPoint])
        if currentPoint == 0: 
            break
            
    starPathData.closePath()
    return starPathData
    
def phiSpiralBez(pointA, pointB, iter, reverseDirection=0, expanding=0):
    '''creates a Phi spiral inside a rectangle with short side AB, and rectangle existing
    on the right side of AB when travelling from A to B (or the opposite if reverseDirection = 1).
    iter defines the number of iterations.  Composed with a series of cubic beziers. '''
    phi = (1 + math.sqrt(5)) / 2.0
    if reverseDirection: 
        angle = 0.25
    else: angle = 0.75
    if expanding : multVal = 1.0 +phi
    else: multVal = phi -1
    
    spiralPath = PathData().moveTo(pointA)
    currentPoint = deepcopy(pointA)
    adjacentCorner = deepcopy(pointB)
    sideLength = distanceBetween(currentPoint, adjacentCorner)
    destinationPoint = extendBendPoint(currentPoint, adjacentCorner,  sideLength,angle)
    for i in range(iter):
        sideLength = distanceBetween(currentPoint, adjacentCorner)
        ctrlDistanceRatio = float(4)/8
        ctrlPt1 = getLineDivision(currentPoint,adjacentCorner,ctrlDistanceRatio)
        ctrlPt2 = getLineDivision(adjacentCorner,destinationPoint, ctrlDistanceRatio)
        spiralPath.cubicBezier(ctrlPt1, ctrlPt2, destinationPoint)
        currentPoint = deepcopy(destinationPoint)
        adjacentCorner= extendBendPoint(adjacentCorner,destinationPoint , float(sideLength)*(multVal),0)
        sideLength = distanceBetween(currentPoint, adjacentCorner)
        destinationPoint = extendBendPoint(currentPoint, adjacentCorner, sideLength,angle)
    
    return spiralPath

def phiFlower(centerRadius,rays, spiralWidth, spiralIter):
    """a flower-like shape formed by phi spirals"""
    flowerPath = PathData()
    for i in range(rays):
        startPoint = PolerPoint(centerRadius,float(i)/rays).convertToCartesian()
        rightSidePoint = extendBendPoint(Point(0,0), startPoint, spiralWidth, 0.25)
        leftSidePoint = extendBendPoint(Point(0,0), startPoint, spiralWidth, 0.75)
        flowerPath.appendPath(phiSpiralBez(startPoint, leftSidePoint, spiralIter, reverseDirection=1))
        flowerPath.appendPath(phiSpiralBez(startPoint, rightSidePoint, spiralIter))
    return flowerPath

def phiLattice(centerRadius,rays, spiralIter):
    """a latticework of interlocking phi spirals"""
    latticePath = PathData()
    for i in range(rays):
        radPt = PolerPoint(centerRadius,float(i)/rays).convertToCartesian()
        center = Point(0,0)
        latticePath.append(pathshapes.phiSpiralBez(radPt,center, spiralIter, reverseDirection=1, expanding=1))
        latticePath.append(pathshapes.phiSpiralBez(radPt,center, spiralIter, expanding = 1))
    return latticePath

##def buildVesicaFlower(petals, centreHoopRadius, flowerRadius, insideOut=0):
##    pathData = PathData()
##    #insideOut determines whether the petal from the centreHoop moves toward the centre of the CentreHoop (if == 1)/
##    #or away from the centre (when insideOut == 0)
##    if insideOut : offsetAngle = 0.5
##    else: offsetAngle = 0
##    for i in range(0, petals):
##        innerPt = PolerPoint(centreHoopRadius,float(i)/petals).convertToCartesian()
##        outerPt = PolerPoint(flowerRadius,(float(i)/petals+offsetAngle)).convertToCartesian()
##        for clockwise in range(0,2):
##            if clockwise == 0 : bendAngle = 0.25
##            else: bendAngle = 0.75
##            ctrlPt = extendBendPoint(innerPt, getMidpoint(innerPt, outerPt),  centreHoopRadius*3, bendAngle)
##            pathData.moveTo(innerPt).quadradicBezier(ctrlPt, outerPt)
##    return pathData
def symetricBezierPetal(pointA, pointB, rbdVector):
    """a petal shaped formed by 2 symetric RVBD beziers mirrored (see path.py for more details on RVBD)"""
    petalPath = PathData().moveTo(pointA).SCRVBD(rbdVector, pointB).SCRVBD(rbdVector, pointA).closePath()
    return petalPath
    
def lotusPetalFlower(petals, baseRadius, tipRadius, ctrlDistanceRatio):
    """a flower shape similar to the lotus flower mandalas in Hindu/Yogic iconography"""
    petalFraction = 1.0/petals
    petalWidth = tipRadius - baseRadius
    pathData = PathData()
    pathData.moveTo(Point().polerInit(baseRadius,0.0))
    for i in range(petals):
        tipPoint = Point().polerInit(tipRadius, (i+0.5)*petalFraction)
        endPoint = Point().polerInit(baseRadius,(i+1)*petalFraction)
        ctrlPt1 = Point().polerInit(baseRadius+petalWidth*ctrlDistanceRatio, i*petalFraction)
        ctrlPt2 = Point().polerInit(baseRadius+petalWidth*(1-ctrlDistanceRatio), (i+0.5)*petalFraction)
        ctrlPt3 = Point().polerInit(baseRadius+petalWidth*ctrlDistanceRatio, (i+1)*petalFraction)
        pathData.cubicBezier(ctrlPt1,ctrlPt2, tipPoint)
        pathData.cubicBezier(ctrlPt2, ctrlPt3, endPoint)
          
    pathData.closePath()
    return pathData
    
def rayBlocks(rays, innerRadius, outerRadius, innerSpacingRatio, outerSpacingRatio, roundedEnds=0, roundingCtrlDistanceRatio=0.1):
    """radially-tiled shape similar to a slice of pie with the crust and tip cut off with a straight line"""
    slice = float(1)/rays
    allBlocks = PathData()
    outerBezAngal = None
    innerBezAngal = None
   
    for i in range(rays):
        innerOffsetDistance = 0.5*innerSpacingRatio*slice
        outerOffsetDistance = 0.5*outerSpacingRatio*slice        
        leftInnerAngle = i*slice -innerOffsetDistance
        rightInnerAngle = i*slice + innerOffsetDistance
        leftOuterAngle = i*slice -outerOffsetDistance
        rightOuterAngle = i*slice + outerOffsetDistance
        if roundedEnds ==0:
            allBlocks.moveTo(Point().polerInit(innerRadius, leftInnerAngle)).\
            lineTo(Point().polerInit(innerRadius, rightInnerAngle)).\
            lineTo(Point().polerInit(outerRadius, rightOuterAngle)).\
            lineTo(Point().polerInit(outerRadius, leftOuterAngle)).closePath()
        else:
            if i == 0:
                outerBezAngal = 1.0- angalBetween(Point().polerInit(outerRadius +10, leftOuterAngle),\
                        Point().polerInit(outerRadius , leftOuterAngle), Point().polerInit(outerRadius, rightOuterAngle))
                innerBezAngal = 1.0- angalBetween(extendBendPoint(Point().polerInit(outerRadius, leftOuterAngle),  Point().polerInit(innerRadius, leftInnerAngle), 10, 0), 
                        Point().polerInit(innerRadius , leftInnerAngle), Point().polerInit(innerRadius, rightInnerAngle))

            allBlocks.moveTo(Point().polerInit(innerRadius, leftInnerAngle))
            allBlocks.SCRVBD( (roundingCtrlDistanceRatio, innerBezAngal) , Point().polerInit(innerRadius, rightInnerAngle) )
            allBlocks.lineTo(Point().polerInit(outerRadius, rightOuterAngle))
            allBlocks.SCRVBD( (roundingCtrlDistanceRatio, outerBezAngal) , Point().polerInit(outerRadius, leftOuterAngle) )
            allBlocks.closePath()

    return allBlocks
    
def tomsensFigure(radius, insetRatio):
    '''generates a Tomsens Figure, see : http://mathworld.wolfram.com/ThomsensFigure.html '''
    triangleCorners = []
    
    #pointPositions represents the order that the points of the Tomsens figure path follows,
    #each pair represents a point along the path.  The point itself is (insetRatio*(length of side)) far 
    #on the line from the first corner to the second corner 
    pointPositions = [[0,1], [2,1],[2,3],[1,0],[1,2],[3,2]]
    
    #create corners of triangle
    for i in range(0,3):
        triangleCorners.append(PolerPoint(radius, float(i)/3).convertToCartesian())
    
    #create the Tompsens figure path
    thisPath = PathData()
    pointArray = []
    
    #create the array of points to follow from pointPositions
    for k,j in pointPositions:
        pointArray.append(getLineDivision(triangleCorners[(i+k)%3], triangleCorners[(i+j)%3], insetRatio))
        
    #create PathData for path
    thisPath.moveTo(pointArray[0])
    for x in range(1,len(pointArray)):
        thisPath.lineTo(pointArray[x])
    thisPath.closePath()
    
    return thisPath
    
#FIXME: consider variations on this 
def loopDeLoop(pointA, pointB, width, loops, loopStretchRatio):
    """simulates a loop-de-loop from one point to another"""
    ticks = getLineDivisions(pointA,pointB, loops+1)
    points = []
    bendAngle = 0.25
    #points.append(extendBendPoint(pointB, pointA,width, bendAngle))
    
    for i in range(1,loops+1):
        if i %2 == 0: bendAngle = 0.25
        else: bendAngle = 0.75
        points.append(extendBendPoint(pointA, ticks[i], width, bendAngle))
        
    gapDistance = distanceBetween(ticks[0], ticks[1])
    ctrlVectors = [(extendBendPoint(points[2], points[1], loopStretchRatio*gapDistance, 0.25) - points[1] ),  (extendBendPoint(points[2], points[1], loopStretchRatio*gapDistance, 0.75) - points[1]) ] 
    path = PathData().moveTo(points[0])
            
    for i in range(0, loops - 2):
        loopParity = i %2
        
        #redundancy for clarity
        ctrlPt1 = ctrlVectors[loopParity] + points[i] 
        ctrlPt2 = ctrlVectors[loopParity] + points[i+1] 
        #produces different pattern, somewhat interesting, but results in deviance from a loopdeloop with different variables
        ##ctrlPt1 = extendBendPoint(ticks[i], points[i], loopStretch*gapDistance, 0.75)
        ##ctrlPt2 = extendBendPoint(ticks[i+1], points[i+1], loopStretch*gapDistance,  0.25)
        path.cubicBezier(ctrlPt1, ctrlPt2, points[i+1])
        
    return path
    
##def buildArcSpire(spokes, distanceFromCentre, spireWidth, spireHeight, baseCurveRatio, sideCurveRatio):    
##    centrePoint = Point(0,0)
##    spirePath = PathData()
##    for i in range(0,spokes):
##        midBasePoint = Point().polerInit(distanceFromCentre, float(i)/spokes)
##        leftBasePoint = extendBendPoint(centrePoint, midBasePoint, spireWidth/2.0, 0.75)
##        rightBasePoint = extendBendPoint(centrePoint, midBasePoint, spireWidth/2.0, 0.25)
##        apex = PolerPoint(spireHeight+distanceFromCentre, float(i)/spokes).convertToCartesian()
##        leftControlPoint = extendBendPoint(leftBasePoint, getMidpoint(leftBasePoint, apex), sideCurveRatio*(distanceBetween(leftBasePoint, apex)),0.75) 
##        rightControlPoint = extendBendPoint(rightBasePoint, getMidpoint(rightBasePoint, apex), sideCurveRatio*(distanceBetween(rightBasePoint, apex)),0.25) 
##        baseControlPoint = Point().polerInit(distanceFromCentre + baseCurveRatio*(distanceBetween(leftBasePoint, rightBasePoint)), float(i)/spokes)
##        spirePath.moveTo(leftBasePoint).quadradicBezier(leftControlPoint,apex).quadradicBezier(rightControlPoint,rightBasePoint).quadradicBezier(baseControlPoint, leftBasePoint)
##    return spirePath
##    

def frillCurveLine(pointA, pointB, rvbdVector,numCurves):
    """forms a line of symetric bezier curves, like the path of a bouncing ball with no gravity""" 
    tickMarks = getLineDivisions(pointA, pointB, numCurves)
    frillPath = PathData().moveTo(tickMarks[0])
    for i in range(1,numCurves):
        frillPath.SCRVBD(rvbdVector, tickMarks[i])
    return frillPath
    
def regularPolygon(sides, radius):
    fraction = 1.0/sides
    path = PathData().moveTo(Point().polerInit(radius, 0.5*fraction))
    for i in range(1,sides):
        path.lineTo(Point().polerInit(radius, (float(i) + 0.5)*fraction))
    path.closePath()
    return path
    
def regularPolygonSideLength(sides, sideLength):
    radius = 2*math.sin(math.pi/sides)/sides
    return regularPolygon(sides, radius)
  

def lineZigZag( pointA, pointB, heightRatio, reps):
    ticks = getLineDivisions(pointA,pointB, reps)
    points = []
    bendAngle = 0.25
    height = heightRatio*distanceBetween(ticks[0], ticks[1])
    points.append(extendBendPoint(pointB, pointA, height, bendAngle))
    
    for i in range(1,reps):
        if i %2 == 0: bendAngle = 0.25
        else: bendAngle = 0.75
        points.append(extendBendPoint(pointA, ticks[i], height, bendAngle))
    
    path = PathData().moveTo(points[1])
        
    for i in range(1, reps):
        path.lineTo(points[i])
    
    return path
  
def equiStar(points, innerRadius, outerRadius):
    starPath = PathData().moveTo(Point().polerInit(outerRadius, 0))
    for i in range(points):
        
        starPath.lineTo(Point().polerInit(innerRadius,float(i)/points+0.5/points ))
        starPath.lineTo(Point().polerInit(outerRadius,float((i+1)%points)/points))
    
    return starPath

#FIXME: test this    
def spikeyPolygon(numSides, spikesPerSide, innerRadius, outerRadius):
    innerPoints = createRadialPlots(Point(0, 0), innerRadius,  numSides)
    outerPoints = createRadialPlots(Point(0, 0), outerRadius,  numSides)
    spikeyPath = PathData().moveTo(innerPoints[0])
        
    for i in range(numSides):
        innerTicks = getLineDivisions(innerPoints[i], innerPoints[(i+1)%numSides], spikesPerSide*2+1)
        outerTicks = getLineDivisions(outerPoints[i], outerPoints[(i+1)%numSides], spikesPerSide*2+1)
        
        for j in range(spikesPerSide):
            spikeyPath.lineTo(outerTicks[j*2+1]).lineTo(innerTicks[(j+1)*2])
    spikeyPath.closePath()
    return spikeyPath


def regularPolygon(sides, radius):
    fraction = 1.0/sides
    path = PathData().moveTo(Point().polerInit(radius, 0.5*fraction))
    for i in range(1,sides):
        path.lineTo(Point().polerInit(radius, (float(i) + 0.5)*fraction))
    path.closePath()
    return path
    
def regularPolygonSideLength(sides, sideLength):
    radius = 2*math.sin(math.pi/sides)/sides
    return regularPolygon(sides, radius)
    
def hexagon(point, radius):
    path = PathData().moveTo(point+PolerPoint(radius, 0).convertToCartesian())
    for i in range(1,6):
        path.lineTo(point+PolerPoint(radius, float(i)/6).convertToCartesian())
    path.closePath()
    return path


##def phiSpiralArc(pointA, pointB, iter, reverseDirection=0, expanding=0):
##    '''creates a Phi spiral inside a rectangle with short side AB, and rectangle existing
##    on the right side of AB when travelling from A to B (or the opposite if reverseDirection = 1).
##    iter defines the number of iterations.  Composed with a series of arcs. '''
##    phi = (1 + math.sqrt(5)) / 2.0
##    if reverseDirection: 
##        angle = 0.25
##    else: angle = 0.75
##    sweepValue = int((not reverseDirection) ^ (not expanding))
##    if expanding : multVal = 1.0 +phi
##    else: multVal = phi -1
##    
##    spiralPath = PathData().moveTo(pointA)
##    currentPoint = deepcopy(pointA)
##    adjacentCorner = deepcopy(pointB)
##    sideLength = distanceBetween(currentPoint, adjacentCorner)
##    destinationPoint = extendBendPoint(currentPoint, adjacentCorner,  sideLength,angle)
##    for i in range(iter):
##        spiralPath.elipticalArc(Point(sideLength, sideLength), destinationPoint, sweepFlag=sweepValue)
##        currentPoint = deepcopy(destinationPoint)
##        adjacentCorner= extendBendPoint(adjacentCorner,destinationPoint , float(sideLength)*(multVal),0)
##        sideLength = distanceBetween(currentPoint, adjacentCorner)
##        destinationPoint = extendBendPoint(currentPoint, adjacentCorner, sideLength,angle)
##    return spiralPath
##    

  
##def lineSawWave(pointA, pointB, heightRatio, reps):
##    ticks = getLineDivisions(pointA,pointB, reps)
##    points = []
##    path = PathData()
##    
##    height = heightRatio*distanceBetween(ticks[0], ticks[1])
##    points.append(pointA)
##    
##    for i in range(1,reps-1):
##        path.lineTo(extendBendPoint(pointA, points[i], height, 0.75)).lineTo(extendBendPoint(pointA, points[i], height, 0.25))
##    path.lineTo(pointB)   
##    
##    return path
##    
