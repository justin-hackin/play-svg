"""Script for generating example of the output of compshapes.py functions 
See `compshapes.py <https://github.com/cosmo-guffa/play-svg/blob/master/playsvg/compshapes.py>`_ for more info on corresponding functions """

from playsvg.document import *
from playsvg import compshapes

docu = Document()
docu.append(compshapes.buildSymetricPetalFlower( 32,20, 600, (0.3, 0.1), insideOut = 0))
docu.writeSVG("compshapes_symetric_petal_flower.svg")



