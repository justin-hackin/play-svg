"""generates a circular wave pattern"""
import playsvg.document
import playsvg.pathshapes
from playsvg.geom import *
from playsvg.element import *
from playsvg.path import *
import math

sqPi = math.sqrt(math.pi)
rad = 200
square = PathData().moveTo(Point(sqPi/-2*rad,sqPi/2*rad )).\
lineTo(Point(sqPi/2*rad,sqPi/2*rad )).\
lineTo(Point(sqPi/2*rad,sqPi/-2*rad )).\
lineTo(Point(sqPi/-2*rad,sqPi/-2*rad )).\
lineTo(Point(sqPi/-2*rad,sqPi/2*rad )).closePath()

docu = document.Document()
docu.append(buildCircle(Point(), rad, {'style':'stroke:black;fill:none'}))
docu.append(buildPath(square, {'style':'stroke:black;fill:none'}))

docu.writeSVG('circleSquared.svg')
