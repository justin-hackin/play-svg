from playsvg.document import *
from playsvg.element import *
from playsvg.path import *


    
def pairUpperToLower(points):
    if (len(points) != 2 ): return False
    else: 
        if points[0].y > points[1].y : return points
        else : return [points[1], points[0] ]   

def pairLeftToRight(points):
    if (len(points) != 2 ): return False
    else: 
        if points[0].x < points[1].x : return points
        else : return [points[1], points[0] ]   

def vectorListToPointList(pointlist):
   return [Point(i[0], i[1]) for i in pointlist]

docu = Document()

center = Point()
c1c = center
c1r = 100
docu.append(buildCircle( c1c, c1r, {'style':' stroke:black ;fill:none'}))

c2r = 2*c1r
c2c = Point(-1*c1r,0)
docu.append(buildCircle( c2c, c2r, {'style':' stroke:green ;fill:none'}))

c3r = 2*c1r
c3c = Point(c1r,0)
docu.append(buildCircle( c3c, c3r, {'style':' stroke:green ;fill:none'}))

c4c = Point(0,c1r)
c4r = c2r
docu.append(buildCircle( c4c, c4r, {'style':' stroke:orange ;fill:none'}))

c5c = Point(0,-1*c1r)
c5r = c2r
docu.append(buildCircle( c5c, c5r, {'style':' stroke:orange ;fill:none'}))
c4c5ints = pairUpperToLower( vectorListToPointList(  cc_int(c4c.getVector(), c4r, c5c.getVector(), c5r) ) ) 
pP =   c4c5ints[0]
pS = Point(pP.x, c4c.y)
c6r = distanceBetween(pS,c5c )
c6c = c5c
docu.append(buildCircle( c6c, c6r, {'style':' stroke:cyan ;fill:none'}))
c7c = c4c5ints[1]
c7r = c6r
docu.append(buildCircle( c7c, c7r, {'style':' stroke:yellow ;fill:none'}))
  
c8r = c1r+c4r
c8c = c1c
docu.append(buildCircle( c8c, c8r, {'style':' stroke:blue ;fill:none'}))

c9c = Point(0, c8r+c1r)
c9r = c1r
docu.append(buildCircle( c9c, c9r, {'style':' stroke:red ;fill:none'}))

c10c = c1c
c10r = c8r+c1r
docu.append(buildCircle( c10c, c10r, {'style':' stroke:magenta ;fill:none'}))
 


c10c = 2*math.pi*c10r
c8sqc = 8*c8r

csqdiff = abs(c10c - c8sqc)
accuracy = csqdiff/c8sqc


print "Circumference of circle: " + str(c10c)
print "Circumference of square: " + str(c8sqc)
print "Difference: " + str(csqdiff)
print "Accuracy %: " + str(accuracy*100)



docu.writeSVG("vesica_squaring.svg")




