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
docu.appendElement(buildCircle(docu, Point(), rad, {'style':'stroke:black;fill:none'}))
docu.appendElement(buildPath(docu, square, {'style':'stroke:black;fill:none'}))

docu.writeSVG('circle_squared.svg')
