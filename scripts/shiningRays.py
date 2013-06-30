from playsvg.document import *
from playsvg.element import *
from playsvg.path import *
import playsvg.pathshapes
import os
import string

def makeCentredBox( size):
    boxPath = PathData().moveTo(Point(size, size)).\
            lineTo(Point(size, -1*size)).\
            lineTo(Point(-1*size, -1*size)).\
            lineTo(Point(-1*size, size)).closePath()
    return boxPath

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
docu.append(makeShiningRays(64, 200 ))

docu.writeSVG("shiningRays.svg" )
print "done"

