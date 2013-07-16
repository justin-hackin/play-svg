"""Script for generating example of the output of compshapes.py functions 
See `compshapes.py <https://github.com/cosmo-guffa/play-svg/blob/master/playsvg/compshapes.py>`_ for more info on corresponding functions """

from playsvg.document import *
from playsvg import compshapes

docu = Document()
newNode = compshapes.buildTriangularGrid( 11,30)
newNode.set("transform", "rotate(0)")
docu.append(newNode)
docu.writeSVG("compshapes_triangular_grid.svg")





