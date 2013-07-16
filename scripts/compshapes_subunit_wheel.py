"""Script for generating example of the output of compshapes.py functions 
See `compshapes.py <https://github.com/cosmo-guffa/play-svg/blob/master/playsvg/compshapes.py>`_ for more info on corresponding functions """

from playsvg.document import *
from playsvg import compshapes

docu = Document()
docu.append(compshapes.buildSubunitWheel(((4,8), (4, 4), (8,1)),((2,4), (2,2)), 50, 600))
docu.writeSVG("compshapes_subunit_wheel.svg")

