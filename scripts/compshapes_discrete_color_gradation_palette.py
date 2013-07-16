"""Script for generating example of the output of compshapes.py functions 
See `compshapes.py <https://github.com/cosmo-guffa/play-svg/blob/master/playsvg/compshapes.py>`_ for more info on corresponding functions """

from playsvg.document import *
from playsvg import compshapes

docu = Document()
docu.append(compshapes.buildDiscreteColorGrad(20, "#ff0000", "#0000ff", 400))
docu.writeSVG("compshapes_discrete_color_gradation_palette.svg")



