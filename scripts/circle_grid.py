"""Creates a staggered circle grid for efficient packing of circles.  
Used to create cut lines for circular vinyl stickers used in packaging The Playful Geometer's Illumined Stellations. """
from playsvg import document
import playsvg.pathshapes
from playsvg.path import *
from playsvg.geom import *
from playsvg.element import *

docu = document.Document()



docu.writeSVG('circle_grid.svg')
print "done"

