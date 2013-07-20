"""creates a circle in a rectangle in a circle in a rectangle in a.... """
from playsvg.document import *
from playsvg.element import *

docu = Document()
levels = 22
startSize = 600
currentSize = startSize
for i in range(levels):
    docu.append(buildRect(Point(-1*currentSize, -1*currentSize), 2*currentSize, 2*currentSize, {'style':'stroke:none; fill:white'}))
    docu.append(buildCircle(Point(), currentSize, {'style':'fill:black; stroke:none'}))
    currentSize = Point().polerInit(currentSize,1.0/8).x

docu.writeSVG("circleInRectangleRecusion.svg")




