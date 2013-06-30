import math
import numbthy
from geosolver.intersections import *
from geosolver.vector import *


tewpi = math.pi*2
phi = (1 + math.sqrt(5)) / 2.0
from copy import *

class Point:
    def __init__(self, xval=0, yval=0, fromVector=None):
        if (fromVector != None):
            if (len(fromVector) == 2): 
                self.x = fromVector[0]
                self.y = fromVector[1]
            else:
                raise Exception, "Vector not length 2"
        else:           
            self.x = float(xval)
            self.y = float(yval)
    def getX(self):
        return float(self.x)
    def getY(self):
        return float(self.y)
    def setX(self,xval):
        self.x = float(xval)
    def setY(self,yval):
        self.y = float(yval)
    def polerInit(self, radius,angal):
        self.x = math.sin(angal*tewpi)*radius
        self.y = math.cos(angal*tewpi)*radius
        return self
    def __str__(self):
        return aNum(self.x)+","+aNum(self.y)
    def __unicode__(self):
        return unicode(aNum(self.x)) + u','+ unicode(aNum(self.y)) 
    def __add__(self, point):
        return Point(self.getX() + point.getX(), self.getY() + point.getY())
    def __sub__(self, point):
        return Point(self.getX() - point.getX(), self.getY() - point.getY())
    def __mul__(self, mult):
        return self.x*mult.x + self.y*mult.y
    def __div__(self, divisor):
        return Point(self.x/divisor, self.y/divisor)
    def __cmp__(self,other):
        return cmp(self.convertToPoler().getT(), other.convertToPoler().getT())
    def getMultiple(self,scalar):  ##not able to use __mult__ with point * value ???
        return Point(self.getX()*scalar, self.getY()*scalar)
    def convertToPoler(self):
        existingAngal = Angal(0)
        existingAngal.setByRadianValue(math.atan2(self.y, self.x))
        #return PolerPoint(math.sqrt(self.x**2+ self.y**2), getattr(existingAngal, "value"))
        return (math.sqrt(self.x**2+ self.y**2), getattr(existingAngal, "value"))
    def unitVector(self):
        return self.scale(1/self.vectorLength())
    def vectorLength(self):
        return distanceBetween(Point(0,0), self)
    def scale(self, mult):
        return Point(self.x*mult, self.y*mult)
    def getVector(self):
        return vector([self.x, self.y])
    
#FIXME: use Angal or lose it
class Angal:
    '''an Angal is a fractional representation  of an angle such that (using the clock metaphor) 0 is at 12:00,
    0.25 is at 3:00, 0.5 is at 6:00, and 0.75 is at 9:00.  Angal is always in range |0 - 1( as whole number portions 
   of numbers are truncated in constructors ''' 
    def __init__(self,val):
        if val >=0:
            self.value = val - math.floor(val)
        else:
            self.value = val - math.ceil(val)
    def setByRadianValue(self,rad):
        #wraparound effect for radian values over tewpi
        if rad >= tewpi:
            rad = rad - (rad//tewpi)*tewpi 
        #fractionify rad value    
        value = rad / tewpi
        #change direction of increase from counterclockwise to clockwise
        value = 1-value
        #change starting point 0 from position of 3:00 to 12:00
        value = value + 0.25 - value//1
        self.value = value
    def reflectionInAngle(self, reflector):
        '''returns an Angal such that it is the reflection of the current value in a line 
        drawn through reflector and the middle of a circle'''
        difference = self.value - reflector

#DEPRICATED, use Point polarInit()
class PolerPoint:
#PolerPoints are almost identical to points in the polar co-ordinate system, except they have slightly different conventions (hence the spelling).  Poler points are represented by two values, theyda (t) and radius(r).
    r = 0
    #r represents the radius as in polar co-ordinates
    t = 0
    #theyda represents the angle as theta does in polar co-ordinates. theyda differs in that it's range is [0,1); it represents the percent of the circle traversed.  A theta of 0 is at "12:00" , and theyda increases as the angle moves clockwise.
    def __init__(self, rval, tval):
        self.r = rval
        self.t = tval - math.floor(tval)
    def getR(self):
        return self.r
    def getT(self):
        return self.t
    def setR(self,rval):
        self.r = rval
    def setT(self,tval):
        self.t = tval - math.floor(tval)
    def getString(self):
        return str(self.x)+","+str(self.y)
    def __add__(self, point):
        return PolerPoint(self.r + point.getR(), self.t + point.getT())
    def __str__(self):
        return aNum(self.r) + "r,"+aNum(self.t) +"theyda"
    def convertToCartesian(self):
        return Point(math.sin(self.t*tewpi)*self.r,math.cos(self.t*tewpi)*self.r ) 
    def vertFlip(self):
        self.t = vertFlipThayda(self.t)
    def horizFlip():
        self.t = horizFlipThayda(self.t)

def convertPolarToPoler(angleNum):
    retVal = angleNum + 0.25
    if retVal > 1 :
        retVal -= 1

    retVal = horizFlipThayda(retVal)
    return retVal

def getMidpoint(pointA, pointB):
    return Point( float(pointA.getX()+pointB.getX())/2, float(pointA.getY()+ pointB.getY())/2)

def distanceBetween(pointA, pointB):
    asquared = math.fabs(pointA.x - pointB.x)**2
    bsquared = math.fabs(pointA.y - pointB.y)**2
    return math.sqrt(asquared + bsquared)

#FIXME: used ?    
def distanceBetweenPoints(points):
    totalDistance = 0
    for i in range(len(points) - 1):
        totalDistance += distanceBetween(points[i], points[i+1])
    return totalDistance    
    

def intersectCircleCircle(c1c,c1r,c2c,c2r):
    intersections = cc_int(c1c.getVector(), c1r, c2c.getVector(), c2r) 
    intersections = [Point(i[0], i[1]) for i in intersections]
    return intersections

def getDiscreteCubicBezier(pointA, pointB, pointC, pointD, n):
    """ Accepts 4 CartesianPoint objects which represent a bezier curve as described
    on wikipedia and a number of points n and returns an array of n CartesianPoints 
    equally spaced along that curve"""
    points = [pointA]
    iters = n-2
    for i in range (0,iters):
        t = float(i)/iters
        points.append(pointA.getMultiple((1-t)**3) + pointB.getMultiple(3*t*(1-t)**2) + pointC.getMultiple(3*t**2*(1-t)) + pointD.getMultiple(t**3))    
    
    points.append(pointD)
    return points
    
def getDiscreteQuadradicBezier(pointA, pointB, pointC, n):
    points = [pointA]
    iters = n-2
    for i in range (0,iters):
        t = float(i)/iters
        points.append(pointA.getMultiple((1-t)**2) + pointB.getMultiple(2*t*(1-t)) + pointC.getMultiple(t**2) )    
    
    points.append(pointC)
    return points
    
def getLineDivisions(pointA, pointB, n):
    '''returns an array of n points equally spaced along line AB'''
    points = []
    t = n -1
    xdiff = math.fabs(pointA.getX() - pointB.getX())
    ydiff = math.fabs(pointA.getY() - pointB.getY())
    if pointA.getX() < pointB.getX():
        axOperator = 1
    else:
        axOperator = -1
    
    if pointA.getY() < pointB.getY():
        ayOperator = 1
    else:
        ayOperator = -1
    
    for i in range(0,t):
        fract = float(i)/t
        xval = pointA.getX() +  axOperator*fract*xdiff
        yval = pointA.getY() + ayOperator*fract* ydiff
        points.append(Point(xval, yval))

    points.append(pointB)
    return points
    
def getLineDivision(pointA, pointB, fract):
    '''returns an array of fract number of equally-spaced points along the line from pointA to pointB, inclusive of both'''
        
    if fract < 0:
        #reverse points
        tmpPtA = deepcopy(pointB)
        tmpPtB = deepcopy(pointA)
        #change ratio to extend beyond line
        theFract = math.fabs(fract) +1
    else:
        tmpPtA = deepcopy(pointA)
        tmpPtB = deepcopy(pointB)
        theFract = fract
    
    xdiff = math.fabs(pointA.getX() - pointB.getX())
    ydiff = math.fabs(pointA.getY() - pointB.getY())
    
    if tmpPtA.getX() < tmpPtB.getX(): axOperator = 1
    else: axOperator = -1
    
    if tmpPtA.getY() < tmpPtB.getY():ayOperator = 1
    else: ayOperator = -1
       
    
    return Point(tmpPtA.getX() +  axOperator*theFract*xdiff, tmpPtA.getY() + ayOperator*theFract* ydiff)

def getLineDivisionDistance(pointA, pointB, distance):
    lineLength = distanceBetween(pointA, pointB)
    if distance > lineLength:
        raise Exception, "Requested length longer than distance between points"
    return getLineDivision(pointA, pointB, float(distance)/lineLength)


def getLineDivisionsWithRatios(pointA, pointB, ratios):
    points = []
    for i in range(len(ratios)):
        points.append(getLineDivision(pointA, pointB, ratios[i]))
    return points


def extendBendPoint(pointA, pointB,  length, angle):
    relativeB = pointB - pointA
    bentPoint =  Point().polerInit(length, relativeB.convertToPoler()[1]+angle) + pointB
    return bentPoint

    
def reflectPointInLine(point, lineStart, lineEnd):
    '''Calculation as described in http://mathworld.wolfram.com/Reflection.html'''
    #compute unit vector of line
    lineVector = lineEnd - lineStart
    lineVectorNorm = math.sqrt(float(lineVector*lineVector))
    lineVectorUnit = lineVector*(1/lineVectorNorm)
    print lineVectorUnit
    #projectionPoint = lineStart +((point-lineStart)*lineVectorNorm)*lineVectorNorm
    print ((point - lineStart)*lineVectorUnit)
    reflectionPoint = lineStart*2 - point  + (lineVectorUnit*2)* ((point - lineStart)*lineVectorUnit)
    return reflectionPoint
    
def aNum(theNum):
    return '%.5f'% float(theNum)

#generate a dictionary representing all possible irregular star polygons
def generateStarDict(limit):
    possibleStars = {}
    for pointKey in range(5,limit):
        stepList = []
        for step in range(2, int(math.ceil(float(pointKey)/2))):
            if (numbthy.gcd(pointKey, step) == 1):
                stepList.append(step)
        
        if len(stepList) != 0:
            possibleStars[pointKey] = stepList
    return possibleStars
    
def angalOfPoints(pointA, pointB):
    #wraparound effect for radian values over tewpi
    diffPoint = pointB - pointA
    rad = math.atan2(diffPoint.x, diffPoint.y) 
    if rad >= tewpi:
        rad = rad - (rad//tewpi)*tewpi 
    #fractionify rad value    
    value = rad / tewpi
    #change direction of increase from counterclockwise to clockwise
    value = 1-value
    #change starting point 0 from position of 3:00 to 12:00
    value = value + 0.25 - value//1
    self.value = value



#FIXME:use difference between successive iterations to determine when to stop recursing (instead of # of iterations)
def cubicBezierLength(P1,P2,P3,P4, maxLev=10):
     
    def cubicBezierLengthHelp(P1, P2, P3, P4, level=1):
        if level == maxLev:
            return distanceBetween(P1,P4)
        else:
            L1 = P1
            L2 = getMidpoint(P1, P2)
            H  = getMidpoint(P2, P3)
            R3 = getMidpoint(P3, P4)
            R4 = P4
            L3 = getMidpoint(L2, H)
            R2 = getMidpoint(R3, H)
            L4 = getMidpoint(L3, R2)
            R1 = L4
        return cubicBezierLengthHelp(L1, L2, L3, L4, level+1) + cubicBezierLengthHelp(R1, R2, R3, R4, level+1)
    return cubicBezierLengthHelp(P1, P2, P3, P4)
    
def quadradicBezierLength(P1,P2,P3,maxLev=10):
    def quadradicBezierLengthHelp(P1, P2, P3, level=1):
        if level ==maxLev:
            return distanceBetween(P1,P3)
        else:
            L1 = P1
            L2 = getMidpoint(P1, P2)
            R3 = P3
            R2 = getMidpoint(P2, P3)
            R1 = getMidpoint(L2, P2)
            L3 = R3
        return quadradicBezierLengthHelp(L1, L2, L3, level+1) + quadradicBezierLengthHelp(R1, R2, R3, level+1)
    return quadradicBezierLengthHelp(P1, P2, P3)
    
def intersectLineLine(a1,a2,b1,b2):
    '''returns the itersection point for 2 lines if there exists one, calculations ported from Kevin Lindsey's 2D.js library (switched to Inkscape extensions' summersnight.py algorithm)'''
##    result = None
##    ua_t=(b2.x-b1.x)*(a1.y-b1.y)-(b2.y-b1.y)*(a1.x-b1.x)
##    ub_t=(a2.x-a1.x)*(a1.y-b1.y)-(a2.y-a1.y)*(a1.x-b1.x)
##    u_b=(b2.y-b1.y)*(a2.x-a1.x)-(b2.x-b1.x)*(a2.y-a1.y)
##    if(u_b!=0):
##        ua=ua_t/u_b
##        ub=ub_t/u_b
##        if(0<=ua and ua<=1 and 0<=ub and ub<=1):
##            result = Point(a1.x+ua*(a2.x-a1.x),a1.y+ua*(a2.y-a1.y))
##    return result
    x1 = a1.x
    x2 = a2.x
    x3 = b1.x
    x4 = b2.x
    
    y1 = a1.y
    y2 = a2.y
    y3 = b1.y
    y4 = b2.y
    
    denom = ((y4 - y3) * (x2 - x1)) - ((x4 - x3) * (y2 - y1))
    num1 = ((x4 - x3) * (y1 - y3)) - ((y4 - y3) * (x1 - x3))
    num2 = ((x2 - x1) * (y1 - y3)) - ((y2 - y1) * (x1 - x3))
    num = num1
    if denom != 0: 
        x = x1 + ((num / denom) * (x2 - x1))
        y = y1 + ((num / denom) * (y2 - y1))
        return Point(x, y)
    return Point(NaN, NaN)

 
    
def sideLengthToCornerRadius(sideLength, numSides):
    return 2*math.sin(math.pi/numSides)/sideLength

def cornerRadiusToSideLength(radius, numSides):
    return 2*math.sin(math.pi/numSides)/radius

def cornerRadiusToSideRadius(cornerRadius, sides):
    cornerToSideAngal = 0.5/float(sides)
    sideRadius = math.cos(tewpi*cornerToSideAngal)*cornerRadius
    return sideRadius
    
def angalBetween(ptA, ptB, ptC):
    sideAB = distanceBetween(ptA, ptB)
    sideBC = distanceBetween(ptB, ptC)
    sideCA = distanceBetween(ptC, ptA)
    thetaAng = math.acos((sideCA**2-sideAB**2-sideBC**2)/(-2*sideAB*sideBC))
    return thetaAng/tewpi

# the pattern can be best explained with a picture that uses the grid
# note that the angular position is offset such that the first indexed 
# point at a given layer will move clockwise as the layer increases
def createOffsetRadialGrid(rings, spokes, layerSpacing, beginRadius):
    plots = []
    for ring in range(rings):
        if ring ==0 and float(beginRadius) == 0.0:
            plots.append([Point(0,0)]*spokes)
        else:
            plots.append([])
            for spoke in range(spokes):
                #                                                                                      offset on ring     start point of ring  
                plots[-1].append(Point().polerInit(ring*layerSpacing+beginRadius , (float(spoke)/spokes + ((0.5*ring % spokes)/spokes))))
    return plots
    
def createRadialGrid(rings, spokes, layerSpacing, beginRadius):
    plots = []
    for ring in range(rings):
        if ring ==0 and float(beginRadius) == 0.0:
            plots.append([Point(0,0)]*spokes)
        else:
            plots.append([])
            for spoke in range(spokes):
                plots[-1].append(Point().polerInit(ring*layerSpacing+beginRadius , (float(spoke)/spokes )))
    return plots

def createRadialPlots(position, radius, spokes, passive = 0):
    """returns an array of equidistant points on a circle"""
    plots = []
    if not passive: offset = 0
    else: offset = 1.0/(2*spokes)
    
    for i in range(spokes):
        plots.append(Point().polerInit(radius, float(i)/spokes + offset) + position)
    return plots

def createTriangularGrid(startPoint, sideLength, levels):
    """creates a 2D array representing intersections of a triangular grid bound by a triangle
    first dimension represents height, second dmension represents horizontal position"""
    tetractysArray = []
    apexArray = []
    apexArray.append(startPoint)
    tetractysArray.append(apexArray)
    
    for i in range(1,levels):
        tetractysArray.append([])
        
        for j in range(i):
            overarchPoint = tetractysArray[-2][j]
            leftRef = overarchPoint + Point(-10, 0)
            tetractysArray[-1].append(extendBendPoint(leftRef, overarchPoint, sideLength, 1.0/3.0))   
            
        tetractysArray[-1].append(extendBendPoint( tetractysArray[-2][-1] + Point(-10 ,0) ,tetractysArray[-2][-1], sideLength,1.0/6.0))
    return tetractysArray
    
def createTriangleCentreGrid(startPoint, sideLength, levels):
    """creates a 2D array representing centres of triangles in a triangular grid bound by a triangle
    first dimension represents height second dmension represents horizontal position"""
    tetractysArray = []
    apexArray = []
    apexArray.append(startPoint)
    tetractysArray.append(apexArray)
    trigridRadius = sideLength /  (math.sin(1.0/3*tewpi)*math.sin(1.0/12*tewpi)*4.0)
    middleToBaseDistance = trigridRadius*math.sin(1.0/12*tewpi)
    
    for i in range(1,levels):
        tetractysArray.append([])
        for j in range(i):
            overarchPoint = tetractysArray[-2][j]
            leftRef = overarchPoint + Point(-10, 0)
            tetractysArray[-1].append(deepcopy(extendBendPoint(leftRef, overarchPoint, sideLength, 1.0/3.0)))   
        tetractysArray[-1].append(deepcopy(extendBendPoint( tetractysArray[-2][-1] + Point(-10 ,0) ,tetractysArray[-2][-1], sideLength,1.0/6.0)))
        #insert points for upside down triangle centres
    for i in range(1,levels):
        newInnerArray = deepcopy(tetractysArray[i])
        for j in range(1,i+1):
            midApexPlot = getMidpoint(tetractysArray[i][j], tetractysArray[i][j-1])
            triangleCentre = extendBendPoint(tetractysArray[i][j], midApexPlot, trigridRadius-middleToBaseDistance, 0.25)
            newInnerArray.insert(2*j-1,deepcopy(triangleCentre))
        tetractysArray[i] = newInnerArray
    
    
    return tetractysArray
    
def projectionPointOnLine(pointB, lineA, lineB):
    """returns a point that is the projection of pointB onto line that intersects lineA and lineB""" 
    lineVector = lineB-lineA
    bRelative = pointB - lineA
    projRelative = lineVector.unitVector().scale( ((lineVector*bRelative)/lineVector.vectorLength() ))
    return lineA + projRelative
 
def perspectiveDistanceRatioArray(angal, divisions):
    """in a perspective drawing, things which are equally spaced apart in 3 dimensions, 
    (i.e. mailboxes infront of houses on a road) get closer and closer together
    this algorithm, given a number of divisions and an angle at which the viewer is looking down, 
    returns an array of ratios that represent how far each successive point is along the line towards the origin
    see "The Illusion of Depth" section of http://www.khulsey.com/perspective_basics.html for an illustration"""  
    if angal >= 0.25:
        raise Exception, "angal must be less than 0.25"
    
    origin = Point(0,0)
    unitLength = 100
    #plot point under origin 
    feetPoint = origin - Point(0, unitLength)
    vanishingDistance = unitLength/math.tan(angal*tewpi)
    vanishingPoint = extendBendPoint(origin, feetPoint,  vanishingDistance, 0.75)
    vanishingPointEyelevel = origin + Point(vanishingDistance, 0)
    baseDivisions = getLineDivisions(feetPoint, vanishingPoint, divisions)
    sideIntersections = []
    for i in range(divisions):
        sideIntersections.append( intersectLineLine(feetPoint, vanishingPointEyelevel, baseDivisions[i], origin))
    perspectiveDistanceLength = distanceBetween(feetPoint, sideIntersections[-1])
    ratios = []
    for i in range(divisions):
        ratios.append(distanceBetween(feetPoint, sideIntersections[i])/perspectiveDistanceLength)
    
    return ratios
    
def getAngalBetween(pointA, pointB, pointC):
    angBA = angalBetween(pointB, pointA)
    angBC = angalBetween(pointB, pointC)
    if angAB < angBC: return angAB + angBC
    else: return angBC - angAB


#FIXME:used ?
def vertFlipThayda(number):
        return 1 - number

#FIXME:used ?
def horizFlipThayda(number):
    retVal = 0.5 - number
    if retVal < 0 :
        retVal = retVal + 1 
    
    return retVal

#FIXME:used ?
def convertTanToFract(number):
    if number < 0 :
        retVal = 1+number
    else:
        retVal = number
        
    return retVal

#FIXME:used ?
def radialPlot(angleFraction, radius):
    givenAngleFraction = angleFraction
    if givenAngleFraction >= 1:
        givenAngleFraction = angleFraction - math.floor(angleFraction)
    return Point(math.sin(givenAngleFraction*tewpi)*radius , math.cos(givenAngleFraction*tewpi)*radius)  




##
##def hingePlot(pointA, pointB,  length, angle):
##    '''returns a point that is a plot as described in using a compas metaphor: a compas is open \
##     by the distance of hingRadius with end #1 fixed on axisPoint and end #2 \
##     resting such that it is in line with axisPoint and baselinePoint.  The returned point is the point \
##    obtained by swinging end #2 by the angal angleFraction '''
##    relativeB = pointB - pointA
##    print relativeB
##    print relativeB.convertToPoler().getT()
##    hingePoint =  PolerPoint(length, relativeB.convertToPoler().getT()+angle).convertToCartesian() + pointA
##    return hingePoint


##def hingePlot(axisPoint,baselinePoint, angleFraction, hingeRadius):
##    '''returns a point that is a plot as described in using a compas metaphor: a compas is open 
##     by the distance of hingRadius with end #1 fixed on axisPoint and end #2 
##     resting such that it is in line with axisPoint and baselinePoint.  The returned point is the point 
##    obtained by swinging end #2 by the angal angleFraction '''
##    #determine the existing angle between axisPoint and baselinePoint
##    existingAngle = math.atan2( axisPoint.getY()-baselinePoint.getY(), axisPoint.getX()-baselinePoint.getX() ) / tewpi
##    existingAngle = convertTanToFract(existingAngle)
##    print str(existingAngle)
##    #use radialPlot to make hinge
##    plot = axisPoint + radialPlot(existingAngle+angleFraction, hingeRadius)
##    return plot
##    
