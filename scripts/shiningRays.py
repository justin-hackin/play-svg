from playsvg.document import *
from playsvg.element import *
from playsvg.path import *

import os
import string

def makeShiningRays( spokes, radius):
    rayGroup = etree.Element('g')
    for i in range(spokes):
        rayPath = PathData().moveTo(Point(0,0)).\
        lineTo(Point().polerInit(radius, float(i)/spokes)).\
        lineTo(Point().polerInit(radius, float((i+1)%spokes)/spokes)).closePath()
        if i%2 == 0:
            rayGroup.append(buildPath( rayPath,{'style': 'stroke:none;fill:black'})) 
        else:
            rayGroup.append(buildPath( rayPath,{'style': 'stroke:none;fill:white'})) 
    return rayGroup    

docu = document.Document()
docu.append(makeShiningRays(64, 560 ))

docu.writeSVG("shiningRays.svg" )
print "done"

