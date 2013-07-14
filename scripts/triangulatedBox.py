from playsvg.document import *
from playsvg.element import *
from playsvg.path import *


def buildTriangulatedBox( size):
    triBoxGroup = docu.makeGroup()
    corners = [Point(-1*size, size), Point(size, size), Point(size, -1*size), Point(-1*size, -1*size)]
    sidePoints = []
    lineAtts = {'style':'stroke:black;fill:none'}
    
    for i in range(4):
        triPath = PathData().moveTo(corners[i]).lineTo(Point(0,0)).lineTo(corners[(i+1)%4]).closePath()
        docu.append(buildPath( triPath, lineAtts))
    return triBoxGroup

docu = Document()
docu.append(buildTriangulatedBox( 100))
docu.writeSVG("tri_box.svg")




