"""Script for generating example of the output of compshapes.py functions 
See `compshapes.py <https://github.com/cosmo-guffa/play-svg/blob/master/playsvg/compshapes.py>`_ for more info on corresponding functions """

from playsvg.document import *
from playsvg import compshapes

docu = Document()

fillsAttr = {'style':'stroke:none; fill:red; fill-opacity:0.1'}
fills = compshapes.buildCircledCircles(20,300,100, attrs = fillsAttr)
docu.append(fills)


outlinesAttr = {'style':'stroke:black; fill:none; stroke-width:2'}
outlines = compshapes.buildCircledCircles(20,300,100, attrs = outlinesAttr)
docu.append(outlines)

docu.writeSVG("compshapes_circled_circles.svg")
print "done"
