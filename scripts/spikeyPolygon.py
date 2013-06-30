from playsvg.document import *
from playsvg.element import *
from playsvg.path import *
from playsvg import pathshapes


docu = Document()
#docu.append(buildPath(pathshapes.spikeyPolygon(6,8, 100,300), {'style':'stroke:none;fill:black'} ))
docu.append(buildPath(pathshapes.spikeyPolygon(6,7, 200,300), {'style':'stroke:none;fill:black'} ))
docu.writeSVG("spikey_polygon.svg")

