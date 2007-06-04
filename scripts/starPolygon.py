from playsvg.document import *
from playsvg.element import *
from playsvg.path import *
import playsvg.pathshapes

docu = Document()
docu.appendElement(buildPath(docu, playsvg.pathshapes.starPolygon(7, 2 , 100), {'style':'stroke:black;fill:none'} ))
docu.writeSVG('starpolytest.svg')