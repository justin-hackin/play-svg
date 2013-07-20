"""Script for generating example of the output of compshapes.py functions 
See `compshapes.py <https://github.com/cosmo-guffa/play-svg/blob/master/playsvg/compshapes.py>`_ for more info on corresponding functions """

from playsvg.document import *
from playsvg import compshapes

docu = Document()
for i in range(0,10,2):
    docu.append(compshapes.buildFlowerOfLife(7, 80, 0.5+i*.1))
docu.writeSVG("compshapes_flower_of_life.svg")

