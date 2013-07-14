"""Script for generating example of the output of compshapes.py functions 
See `compshapes.py <https://github.com/cosmo-guffa/play-svg/blob/master/playsvg/compshapes.py>`_ for more info on corresponding functions """

from playsvg.document import *
from playsvg import compshapes

docu = Document()
docu.append(compshapes.buildCircleCardioid( 169, 300))
docu.writeSVG("compshapes_cardiod_circles.svg")


docu = Document()
docu.append(compshapes.buildCircularWeave( 16, 300, 0.1, 0.5))
docu.writeSVG("compshapes_circular_weave.svg")



docu = Document()
docu.append(compshapes.buildDiscreteColorGrad(20, "#ff0000", "#0000ff", 20))
docu.writeSVG("compshapes_discrete_color_gradation_palette.svg")

docu = Document()
docu.append(compshapes.buildFlowerOfLife(7, 50))
docu.writeSVG("compshapes_flower_of_life.svg")

docu = Document()
docu.append(compshapes.buildHexagonalCube(200))
docu.writeSVG("compshapes_hexagonal_cube.svg")

docu = Document()
docu.append(compshapes.buildHexagonLattice(8, 30))
docu.writeSVG("hexagonal_lattice.svg")

docu = Document()
docu.append(compshapes.buildOffsetRadialGrid(12, 6, 50, 50))
docu.writeSVG("compshapes_offset_radial_grid.svg")

docu = Document()
docu.append(compshapes.buildOpenBox( 100, 300))
docu.writeSVG("compshapes_open_box.svg")

docu = Document()
docu.append(compshapes.buildStringArt( 20, 100))
docu.writeSVG("compshapes_string_art.svg")

docu = Document()
docu.append(compshapes.buildSubunitWheel(((4,8), (4, 4), (8,1)),((2,4), (2,2)), 50, 200))
docu.writeSVG("compshapes_custom_compass.svg")

docu = Document()
docu.append(compshapes.buildSymetricPetalFlower( 16,70, 200, (0.3, 0.1), insideOut = 0))
docu.writeSVG("compshapes_bezierFlower.svg")


docu = Document()
docu.append(compshapes.buildTriangularGrid( 11,30))
docu.writeSVG("compshapes_triangular_grid.svg")





