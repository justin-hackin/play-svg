from playsvg.document import *
from playsvg.element import *
from playsvg.path import *
import playsvg.pathshapes
import os
import string


def recursiveMagenStar(docu, radius, levels):
    starGroup = docu.makeGroup()
 
    
    for i in range(1, 2*(levels+1)):    
        triPathDown = PathData().moveTo(Point().polerInit(float(i)/levels*radius, 1.0/6)).lineTo(Point().polerInit(float(i)/levels*radius, 1.0/2)).lineTo(Point().polerInit(float(i)/levels*radius, 5.0/6)).closePath()
        hexPath = PathData().moveTo(Point().polerInit(float(i)/levels*radius, 0))
        for j in range(1,6):
            hexPath.lineTo(Point().polerInit(float(i)/levels*radius, float(j)/6))
        hexPath.closePath()
        starGroup.appendChild(buildPath(docu, triPathDown, {'style':'stroke:black; fill:none'}))
        starGroup.appendChild(buildPath(docu, hexPath, {'style':'stroke:black; fill:none'}))
    for i in range(1, levels+1):
        triPathUp = PathData().moveTo(Point().polerInit(float(i)/levels*radius, 0)).lineTo(Point().polerInit(float(i)/levels*radius, 1.0/3)).lineTo(Point().polerInit(float(i)/levels*radius, 2.0/3)).lineTo(Point().polerInit(float(i)/levels*radius, 0)).closePath()
        starGroup.appendChild(buildPath(docu, triPathUp, {'style':'stroke:black; fill:none'}))
    return starGroup
docu = document.Document()
docu.appendElement( recursiveMagenStar(docu,200, 6 ))

docu.writeSVG("magenOctFace.svg" )
print "done"


