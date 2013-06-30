from playsvg.document import *
from playsvg.element import *
from playsvg.path import *

numCircles = 20
radius = 50
docu = document.Document()
for i in range(numCircles):
    docu.append(buildCircle(Point().polerInit(radius, float(i)/numCircles),radius,{'style':'stroke:black;fill:none'})) 
docu.writeSVG("coincident_rings20.svg" )
print "done"

