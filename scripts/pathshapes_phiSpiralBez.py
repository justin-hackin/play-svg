"""Script for generating examples of the output of compshapes.py functions
Code at `pathshapes.py <https://github.com/cosmo-guffa/play-svg/blob/master/playsvg/compshapes.py>`_
 """

from playsvg.document import *
from playsvg.element import *
from playsvg import pathshapes


docu = Document()
spanSize = 150
docu.append(buildPath(pathshapes.phiSpiralBez(Point(-spanSize,0), Point(spanSize,0), 10), {'style':'stroke:black;fill:none'} ))
docu.writeSVG("pathshapes_phiSpiralBez.svg")



