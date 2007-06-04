"""Script for generating examples of the output of compshapes.py functions """

from playsvg.document import *
from playsvg.element import *
from playsvg.path import *
from playsvg import compshapes

docu = Document()
docu.appendElement(compshapes.buildCircleCardioid(docu, 20, 300))
docu.writeSVG("cardiod_circles.svg")

docu = Document()
docu.appendElement(compshapes.buildCircularWeave(docu, 16, 300, 0.1, 0.5))
docu.writeSVG("circular_weave.svg")



docu = Document()
docu.appendElement(compshapes.buildDiscreteColorGrad(docu, 20, "#ff0000", "#0000ff", 20))
docu.writeSVG("discrete_color_gradation_palette.svg")

docu = Document()
docu.appendElement(compshapes.buildFlowerOfLife(docu, 7, 50))
docu.writeSVG("flower_of_life.svg")

docu = Document()
docu.appendElement(compshapes.buildHexagonalCube(docu, 200))
docu.writeSVG("hexagonal_cube.svg")

docu = Document()
docu.appendElement(compshapes.buildHexagonLattice(docu, 8, 30))
docu.writeSVG("hexagonal_lattice.svg")

docu = Document()
docu.appendElement(compshapes.buildOffsetRadialGrid(docu, 12, 6, 50, 50))
docu.writeSVG("offset_radial_grid.svg")

docu = Document()
docu.appendElement(compshapes.buildOpenBox(docu, 100, 300))
docu.writeSVG("open_box.svg")

docu = Document()
docu.appendElement(compshapes.buildStringArt(docu, 20, 100))
docu.writeSVG("string_art.svg")

docu = Document()
docu.appendElement(compshapes.buildSubunitWheel(docu, ((4,8), (4, 4), (8,1)),((2,4), (2,2)), 50, 200))
docu.writeSVG("custom_compass.svg")

docu = Document()
docu.appendElement(compshapes.buildSymetricPetalFlower(docu, 16,70, 200, (0.3, 0.1), insideOut = 0))
docu.writeSVG("bezierFlower.svg")


docu = Document()
docu.appendElement(compshapes.buildTriangularGrid(docu, 11,30))
docu.writeSVG("triangular_grid.svg")





