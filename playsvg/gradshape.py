import document
from gradient import *
from geom import *
from element import *
from path import *
"""module for generating SVG objects with gradients in them
    in most cases, if the method is used more than once with the same gradient and id (or none), fault will occur  
"""

def polygonMidpoint(vertices):
    """calculates the "center" of a polygon defined by points in vertices, 
    works only for equilateral polygons and all quadrilaterals """
    midpoint = None
    numPoints = len(vertices)
    if len(vertices) % 2 == 0 :
        midpoint = intersectLineLine(vertices[0], vertices[numPoints/2], vertices[1], vertices[numPoints/2+1])
    else:
        baseMidpoint1 = getMidpoint(vertices[int(math.floor(0.5*numPoints))], vertices[int(math.floor(0.5*numPoints))+1])
        baseMidpoint2 = getMidpoint(vertices[int(math.floor(0.5*numPoints))+1], vertices[(int(math.floor(0.5*numPoints))+2)%numPoints])
        midpoint =  intersectLineLine(vertices[0], baseMidpoint1, vertices[1], baseMidpoint2)
    return midpoint

def triangleGradient(docu, points, gradient, id = '' ):
    """given a triangle defined by points and a Gradient object, triangle
    with linear gradients running away from first point towards its projection  on the line formed by the other 2 points
    if the method is used more than once with the same gradient and id (or none), fault will occur  """
    if len(points) != 3:
        raise Exception, "points must be of length 3"
    
    projectionPoint = projectionPointOnLine(points[0], points[1], points[2])
    triLinGrad = LinearGradient('triGrad-'  + id , gradient, (projectionPoint, points[0])) 
    docu.appendDefinition(triLinGrad.createDefinition(docu))
    innerTriangle = PathData().makeHull(points)
    return buildPath(docu, innerTriangle, \
        {u'style':u'fill:url(#triGrad-'+ id +u');stroke:none;opacity:1;fill-opacity:1'})

def quadGradient(docu,points, gradient, id=''):
    '''returns a quadrilateral with a linear gradient running from the middle of first 2 points to the middle of last 2 points'''
    if len(points) != 4:
        raise Exception, "points must be of length 4"
    controls = (getMidpoint(points[0], points[1]), getMidpoint(points[2], points[3]))
    
    quadGrad = LinearGradient('quadGrad-'  + id , gradient, controls) 
    docu.appendDefinition(quadGrad.createDefinition(docu))
    quadPath = PathData().makeHull(points)
    return buildPath(docu, quadPath, \
        {u'style':u'fill:url(#quadGrad-'+ id +u');stroke:none;opacity:1;fill-opacity:1'})

def verticalQuadGradient(docu,points, gradient, id=''):
    """returns a quadrilateral with a linear gradient running from the midpoint of first 2 points to it's projection onto the line formed by last 2 points"""
    if len(points) != 4:
        raise Exception, "points must be of length 4"
    
    ctrl1 = getMidpoint(points[0], points[1])
    ctrl2 = projectionPointOnLine(ctrl1, points[2], points[3])
    quadGrad = LinearGradient('quadGrad-'  + id , gradient, (ctrl1, ctrl2)) 
    docu.appendDefinition(quadGrad.createDefinition(docu))
    quadPath = PathData().makeHull(points)
    return buildPath(docu, quadPath, \
        {u'style':u'fill:url(#quadGrad-'+ id +u');stroke:none;opacity:1;fill-opacity:1'})

def polygonGradient(docu, points, gradient, id=''):
    """given a polygon defined by points and a Gradient object, returns a 
    group of "pizza slices" with linear gradients running away from the middle of the polygon"""
    #triangle = PathData().moveTo(Point(0,0)).lineTo(Point(-100, -100)).lineTo(Point(200, -200)).closePath()
    numPoints = len(points)
    midPoint = polygonMidpoint(points)
    innerTriGroup = docu.makeGroup()
        
    for i in range(numPoints):
        triPoints = [midPoint, points[i], points[(i+1)%numPoints]]
        triangleId = id + str(i).zfill(3)
        innerTriGroup.appendChild(triangleGradient(docu, triPoints, gradient, triangleId))
        
    return innerTriGroup       
    
if __name__ == "__main__":
    docu  = Document()
##    startColor = '#0000ff'
##    endColor = '#10ff00'
##    gradient =  Gradient('gradient000').appendStop(GradientStop(startColor, 0)).appendStop(GradientStop(endColor, 1))
    gradientColors = ('#67ff00', '#fd00ff', '#1e00ff')
    gradient = Gradient('grad000')
    gradient.createBalancedGradient(gradientColors)
    docu.appendDefinition(gradient.createDefinition(docu))
    docu.appendElement(polygonGradient(docu,createRadialPlots(Point(100,100), 100, 16, passive=1),gradient ))
    docu.writeSVG('gradientient.svg')
print "done01"

