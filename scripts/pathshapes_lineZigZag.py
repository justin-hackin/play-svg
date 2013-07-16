"""Script for generating examples of the output of compshapes.py functions
Code at `pathshapes.py <https://github.com/cosmo-guffa/play-svg/blob/master/playsvg/compshapes.py>`_
 """

from playsvg.document import *
from playsvg.element import *
from playsvg import pathshapes

lineStretch = 600
docu = Document()
for i in range(5, 30):
    docu.append(buildPath(pathshapes.lineZigZag(Point(-lineStretch,0), Point(lineStretch,0), i*0.1, 20 ), {'style':'stroke:black;fill:none'} ))
docu.writeSVG("pathshapes_lineZigZag.svg")
