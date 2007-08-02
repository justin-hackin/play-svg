from playsvg.document import *
from playsvg.element import *
from playsvg.path import *
from playsvg import compshapes
docu = Document()
levels = 22
startSize = 200
currentSize = startSize
for i in range(levels):
    docu.appendElement(buildRect(docu, Point(-1*currentSize, -1*currentSize), 2*currentSize, 2*currentSize, {'style':'stroke:none; fill:white'}))
    docu.appendElement(buildCircle(docu, Point(), currentSize, {'style':'fill:black; stroke:none'}))
    currentSize = Point().polerInit(currentSize,1.0/8).x

docu.writeSVG("circle_squared_rev.svg")




