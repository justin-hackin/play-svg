from playsvg.document import *
from playsvg.element import *
from playsvg.path import *
import playsvg.pathshapes

thickness = 60
width = 600
angal = 30.0/360

length = width/math.cos(angal*tewpi)
chevPoints = []
chevPoints.append(Point(0,0))
topLeft = extendBendPoint(Point(100, 0), Point(0,0), length, angal)
chevPoints.append(topLeft)
chevPoints.append(Point(topLeft.x, topLeft.y-thickness))
chevPoints.append(Point( 0, -1*thickness))
chevPoints.append(Point(-1*topLeft.x, topLeft.y-thickness))
chevPoints.append(Point(-1*topLeft.x, topLeft.y))
chevPoints.append(Point())
docu = Document()
docu.append(buildPath(PathData().makeHull(chevPoints), {'style':'stroke:black;fill:none'} ))
docu.writeSVG('chevron.svg')
