from playsvg.document import *
from playsvg.element import *
from playsvg.path import *
import playsvg.pathshapes

    
centreCircRad = 40
concentricRingDistance = 40
concentricRings = 4
sections = 6
    
docu = Document()
docu.appendElement(buildCircle(docu, Point(), centreCircRad,  {'style':'stroke:black; stroke-width:1'}))

for i in range(1,concentricRings+2):
    docu.appendElement(buildCircle(docu, Point(), i*concentricRingDistance+centreCircRad,  {'style':'stroke:black; stroke-width:1'}))
for i in range(sections):
    docu.appendElement(buildLine(docu, Point().polerInit(centreCircRad+concentricRingDistance,float(i)/sections),Point().polerInit(centreCircRad+(concentricRings+1)*concentricRingDistance,float(i)/sections) ,  {'style':'stroke:black; stroke-width:1'}))

docu.writeSVG('concentric_intersection.svg')
print "done"
