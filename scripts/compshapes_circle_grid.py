"""Creates a staggered circle grid for efficient packing of circles.  
Used to create cut lines for circular vinyl stickers used in packaging The Playful Geometer's Illumined Stellations. """
from playsvg.document import *
from playsvg import compshapes
from playsvg.path import *
from playsvg.geom import *
from playsvg.element import *




columns = 24
rows = 21 
radius = 30
startPoint = Point(radius, radius)
spacingRatio = 0
docu = document.Document(notCentered=True)
docu.append(compshapes.buildCircleGrid(startPoint,columns, rows, radius, spacingRatio))

docu.writeSVG('compshapes_circle_grid.svg')
print "done"

