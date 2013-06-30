from playsvg.document import *
from playsvg.element import *
from playsvg.path import *

def intersectCircleCircle(cAc, cAr, cBc, cBr ):

        
    d = distanceBetween(cAc, cBc)
    a = (cAr*cAr - cBr*cBr + d*d)/(2*d)
    h = math.sqrt(cAr*cAr - a*a)
    i = cBc - cAc
    cCc = (cBc - cAc).scale(a/d) + cAc
    x3 = cCc.x + h*(cBc.y - cAc.y)/d
    y3 = cCc.y - h*(cBc.x - cAc.x)/d
    x4 = cCc.x - h*(cBc.y - cAc.y)/d
    y4 = cCc.y + h*(cBc.x - cAc.x)/d
    return [Point(x3,y3), Point(x4, y4)]
    
    
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

docu = Document()

center = Point()
c1rad = 100
c1center = Point(-0.5*c1rad, 0)
c2center = Point(c1rad*0.5, 0)
#Step 1
docu.append(buildCircle(c1center, c1rad, {'style':' stroke:black ;fill:none'}))
# Step 2
docu.append(buildCircle(c2center, c1rad, {'style':' stroke:black; fill:none'}))
# Step 5
c3rad =  c1rad/2
docu.append(buildCircle(center, c3rad, {'style':' stroke:red; fill:none'}))
topc1c2int = pairUpperToLower(intersectCircleCircle(c1center, c1rad, c2center, c1rad))[0]
c4c = Point(0, c3rad)
c4r = distanceBetween(topc1c2int, c4c)
docu.append(buildCircle(c4c, c4r, {'style':' stroke:green ; fill:none'}))
c5c = pairLeftToRight(intersectCircleCircle(c4c, c4r, center, c3rad))[0]
c5r = distanceBetween(c5c, center)
docu.append(buildCircle( c5c, c5r, {'style':' stroke:blue ; fill:none'}))
c6c = pairUpperToLower(intersectCircleCircle(c5c, c5r, center, c3rad))[1]
c6r = distanceBetween(c6c, c4c)
docu.append(buildCircle( c6c, c6r, {'style':' stroke:purple ; fill:none'}))
c7c = pairUpperToLower(intersectCircleCircle(c6c, c6r, center, c3rad))[1]
c7r = distanceBetween(c6c, c7c)
docu.append(buildCircle( c7c, c7r, {'style':' stroke:purple ; fill:none'}))
degrees2over7 = 360*angalBetween(c6c, center, c7c)
print "Degrees 2/7 estimated"+ str(degrees2over7 )
degreesact = (2.0/7)*360 
print "Degrees 2/7 actual "+ str(degreesact)
diffratio = (degrees2over7 - degreesact) / degreesact
print "difference ratio %" + str(diffratio*100)
docu.writeSVG("heptagon_vesica.svg")




