"""
WARNING: requires sympy installation
A script to generate the Sri Yantra using Patrick Flanagan's method seen 'here <http://www.sriyantraresearch.com/Construction/Flanagan/patrick_flanagan_method.htm>`_
Originally t1heightRatio was defined as math.sqrt(phi) as in Flanagan's methods.  
This ratio was altered to optimize for the final t10 triangle being an equalateral triangle through trial and error
"""

from playsvg.document import *
from playsvg.element import *
from playsvg.path import *
from sympy.geometry import *

import math
from copy import copy

def labelPoint(circle, pointCol, text, textOff ):
    labelGroup = buildGroup(id=text+"_marker")
    
    dot = makeCircle(circle, {'style': 'fill-opacity:0.6;fill:' + pointCol  } )
    labelGroup.append(dot)
    text = makeText(text, Point(circle.center.x+textOff.x, circle.center.y+textOff.y), { 'style': "fill:black;stroke:none;font-size:12;"})
    labelGroup.append(text)
    return labelGroup

def mirrorPoint(point):
    return Point(point.x*-1, point.y)
#search: (\w+)(\=.+\n)
#replace: $1$2 docu\.append\( labelPoint\( $1 , pointRad, \"red\", \"$1\" , plotOffPt,   \n    

docu = Document()
def centerOfTriangle(p1, p2, p3):
    return intersectLineLine(p1, getMidpoint(p2, p3), p2, getMidpoint(p1, p3)  )

#variable conventions t(triangle) # (triangle number)[l,r,a](left base, right base, apex)

scale = 400
#t1heightRatio = math.sqrt(phi)
t1heightRatio = 1.3281978

print "t1"
t1l = Point(-1*scale, 0 )
t1r = Point(scale, 0 )
t1height = scale*t1heightRatio
t1a = Point(0, t1height)
t1 = Triangle(t1a, t1r, t1l)
#print t1.angles
c1 = t1.circumcircle
docu.append(makeCircle(c1))
docu.append(makeTriangle(t1))
print "t2"
t2a = Point(0, c1.center.y - c1.radius)
t2baseCent = Point(0,2*scale*4)
t2r = t2a + Point(2*scale*3,2*scale*4)
xLine = Line(t2a, t2r)
t2r = xLine.intersection(c1)[-1]
t2l = Point(t2r.x*-1, t2r.y)
t2 = Triangle(t2a, t2r, t2l)
docu.append(makeTriangle(t2))

l1diaDist = t2r.distance(Point(0, t2r.y ) )
t3a = Point(0,t1r.y + l1diaDist)


l2diaDist = t1r.distance(Point(0, t1r.y ) )
t4a = Point(0,t2r.y - l2diaDist)

print "t3"
 
t3rRayCross = Segment(t2a, t2r).intersection(Segment(t1l, t1r))[0]
t3rRay = Ray(t3a, t3rRayCross) 
docu.append(makeLine(t3rRay))
t3lRay = Ray(t3a, Point(-1*t3rRayCross.x, t3rRayCross.y ))
docu.append(makeLine(t3lRay))

print "t4"

t4rRayCross = Segment(t2l, t2r).intersection(Segment(t1a, t1r))[0]
t4rRay = Ray(t4a, t4rRayCross)
docu.append(makeLine(t4rRay))
t4lRay = Ray(t4a, Point(-1*t4rRayCross.x, t4rRayCross.y ))
docu.append(makeLine(t4lRay))

print "t5"

t5a = Point(0, t2l.y)
t5rRay = Line(t5a,  Line(t1r, t1l).intersection(t4rRay)[0] )
#docu.append(makeLine(t5rRay))
t5r = Ray(t4a, Point(scale*3, t4a.y)).intersection(t5rRay)[0]
#print t5r
t5l = Point(t5r.x*-1 , t5r.y)
t5 = Triangle(t5a, t5r, t5l)
docu.append(makeTriangle(t5))

t3Baser = Line(t2a, t2r).intersection(Line(t5a, t5r))[0]
t3BaserToRight = t3Baser + Point(scale*2, 0)

# docu.append(labelPoint(Circle(t3Baser, 2), "red", "t3Baser", Point(10,10)))
# docu.append(labelPoint(Circle(t4a, 2), "blue", "t4a", Point(10,10)))
# docu.append(makeLine(t5rRay))
t3r = t3rRay.intersection(Ray( t3Baser, t3BaserToRight ) )[0]
t3l = Point(t3r.x*-1, t3r.y)
t3 = Triangle(t3a, t3l, t3r)
docu.append(makeTriangle(t3))

print "t6"


t6cLineP1 = Line(t2a, t2r).intersection(Line(t1r, t1l))[0]
t6cLineP2 = Line(t3a, t3l).intersection(Line(t2l,t2r))[0]
t6ar = Line(t6cLineP1, t6cLineP2).intersection(t4rRay)[0]
t6a = Point(0,t6ar.y)


t6r = Line(t2r,  t2l).intersection(Line(t3a, t3r))[0]
t3aToRight = t3a + Point(scale*2, 0)
t6r = Line(t3a, t3aToRight).intersection(Line(t6a, t6r))[0]
t6l = Point(-1*t6r.x, t6r.y)

t6 = Triangle(t6a, t6r, t6l)
docu.append(makeTriangle(t6))

t4Baser = Line(t1a, t1r).intersection(Line(t6a, t6r))[0]
t4BaserToRight = t4Baser  + Point(scale*2, 0)
t4r = Ray(t4Baser, t4BaserToRight).intersection(t4rRay)[0]
t4l = mirrorPoint(t4r)
t4 = Triangle(t4a, t4r, t4l)
docu.append(makeTriangle(t4))

print "t7"


t7a = Point(0, t4r.y)
t6aToRight = t6a+Point(2*scale, 0)
t7r = t4rRay.intersection(Line(t6a, t6aToRight) )[0]
t7l = mirrorPoint(t7r)
t7 = Triangle(t7a, t7r, t7l)
docu.append(makeTriangle(t7))

print "t8"

t8a = Point(0,t3r.y)
t8rInt = Line(t6a, t6r).intersection(Line(t7a, t7r))[0]
t8rIntToRight = t8rInt + Point(scale*2, 0)
t8r = Ray(t8rInt, t8rIntToRight).intersection(Line(t3a, t3r))[0]

t8l = mirrorPoint(t8r)
t8 = Triangle(t8a, t8r, t8l)
docu.append(makeTriangle(t8))

print "t9"

t9a = Point(0,t1r.y)
t9rInt = Line(t5a, t5r).intersection(Line(t6a, t6r))[0]
t9rIntToRight = t9rInt  + Point(scale*2, 0)
t9r = Ray(t9rInt, t9rIntToRight).intersection(Line(t7a,t7r))[0]
t9l = mirrorPoint(t9r)
t9 = Triangle(t9a, t9r, t9l)
docu.append(makeTriangle(t9))

print "t10"

t10a = t6a
t10r = Line(t9r, t9l).intersection(Line(t5a, t5r))[0]
t10l = Line(t9r, t9l).intersection(Line(t5a, t5l))[0]
t10 = Triangle(t10a, t10r, t10l)

print "Angle t10a:" + str(t10.angles[t10a].n()/math.pi*180)
print "Angle t10r:" + str(t10.angles[t10r].n()/math.pi*180)
print "Angle t10l:" + str(t10.angles[t10l].n()/math.pi*180)


# 
# docu.append(labelPoint(Circle(t1a, 2), "red", "t1", Point(10,5)))
# docu.append(labelPoint(Circle(t2a, 2), "red", "t2", Point(10,5)))
# docu.append(labelPoint(Circle(t3a, 2), "red", "t3", Point(10,5)))
# docu.append(labelPoint(Circle(t4a, 2), "red", "t4", Point(10,5)))
# docu.append(labelPoint(Circle(t5a, 2), "red", "t5", Point(10,5)))
# docu.append(labelPoint(Circle(t6a, 2), "red", "t6", Point(10,5)))
# docu.append(labelPoint(Circle(t7a, 2), "red", "t7", Point(10,5)))
# docu.append(labelPoint(Circle(t8a, 2), "red", "t8", Point(10,5)))
# docu.append(labelPoint(Circle(t9a, 2), "red", "t9", Point(10,5)))


 
 
docu.writeSVG("sri_yantra.svg")
print "done"

