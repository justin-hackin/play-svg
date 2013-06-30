"""Script for generating examples of the output of compshapes.py functions """

from playsvg.document import *
from playsvg.element import *
from playsvg.path import *
from playsvg import pathshapes


docu = Document()
docu.append(buildPath(pathshapes.arcSpire(Point(-100,0), Point(100,0), 2, 4), {'style':'stroke:black;fill:none'} ))
docu.writeSVG("arc_spire.svg")

docu = Document()
docu.append(buildPath(pathshapes.symetricBezierPetal(Point(-100,0), Point(100,0),(0.5,0.1) ), {'style':'stroke:black;fill:none'} ))
docu.writeSVG("bezier_petal.svg")

docu = Document()
docu.append(buildPath(pathshapes.lineZigZag(Point(-100,0), Point(100,0), 1.5, 7 ), {'style':'stroke:black;fill:none'} ))
docu.writeSVG("line_zigzag.svg")

##docu = Document()
##docu.append(buildPath(pathshapes.lineSawWave(Point(-100,0), Point(100,0), 1.5, 7 ), {'style':'stroke:black;fill:none'} ))
##docu.writeSVG("line_sawwave.svg")

docu = Document()
docu.append(buildPath(pathshapes.loopDeLoop(Point(-100,0), Point(100,0), 10, 20, 1), {'style':'stroke:black;fill:none'} ))
docu.writeSVG("line_loopDeLoop.svg")

docu = Document()
docu.append(buildPath(pathshapes.loopDeLoop(Point(-100,0), Point(100,0), 10, 20, 1), {'style':'stroke:black;fill:none'} ))
docu.writeSVG("line_frillcurve.svg")

docu = Document()
docu.append(buildPath(pathshapes.starPolygon(20,7, 200), {'style':'stroke:black;fill:none'} ))
docu.writeSVG("star_polygon-20_7.svg")

##docu = Document()
##docu.append(buildPath(pathshapes.phiSpiralArc(Point(-100,0), Point(100,0), 10), {'style':'stroke:black;fill:none'} ))
##docu.writeSVG("phiSpiralArc.svg")

docu = Document()
docu.append(buildPath(pathshapes.phiSpiralBez(Point(-100,0), Point(100,0), 10), {'style':'stroke:black;fill:none'} ))
docu.writeSVG("phiSpiralBez.svg")

docu = Document()
docu.append(buildPath(pathshapes.spikeyPolygon(6,8, 100,300), {'style':'stroke:none;fill:black'} ))
docu.writeSVG("spikey_polygon.svg")
