"""Script for generating examples of the output of compshapes.py functions
Code at `pathshapes.py <https://github.com/cosmo-guffa/play-svg/blob/master/playsvg/compshapes.py>`_
 """

from playsvg.document import *
from playsvg.element import *
from playsvg import pathshapes


docu = Document()
docu.append(buildPath(pathshapes.spikeyPolygon(6,8, 300,600), {'style':'stroke:none;fill:black'} ))
docu.writeSVG("pathshapes_spikeyPolygon.svg")


