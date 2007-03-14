"""Makes a closed polygon representing the tracing of the numbers from 1-9 on the Lo Shu Square, 
a magic square of size 3""" 

import playsvg.document
import math
from playsvg.geom import *
from playsvg.element import *
from playsvg.path import *
docu = document.Document()

gridSize = 50
numberPositions = [Point(0,gridSize), Point(-1*gridSize,   -1*gridSize), Point(gridSize, 0),\
                            Point(gridSize, -1*gridSize), Point(0, 0), Point(-1*gridSize, gridSize), \
                            Point(-1*gridSize, 0), Point(gridSize, gridSize), Point(0, -1*gridSize)]
cronoPath = PathData().moveTo(numberPositions[0])
for i in range(1,9):
    cronoPath.lineTo(numberPositions[i])
cronoPath.closePath()
docu.appendElement(buildPath(docu, cronoPath, {u'style':u'stroke:black; fill:none'}))

docu.writeSVG('cronoLoShu.svg')
print "done01"

