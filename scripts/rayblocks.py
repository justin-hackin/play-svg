from playsvg.document import *
from playsvg.element import *
from playsvg.path import *
import playsvg.pathshapes

docu = Document()
docu.appendElement(buildPath(docu, playsvg.pathshapes.rayBlocks(8, 100 , 400, 0.1, 0.1,  1, 0.5), {'style':'stroke:black;fill:none'} ))
docu.writeSVG('rayblockstest.svg')


