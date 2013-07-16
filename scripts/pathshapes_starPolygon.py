"""Script for generating examples of the output of compshapes.py functions
Code at `pathshapes.py <https://github.com/cosmo-guffa/play-svg/blob/master/playsvg/compshapes.py>`_
 """

from playsvg.document import *
from playsvg.element import *
from playsvg import pathshapes


docu = Document()
docu.append(buildPath(pathshapes.starPolygon(20,7, 600), {'style':'stroke:black;stroke-width:2;fill:none'} ))
docu.writeSVG("pathshapes_starPolygon.svg")
