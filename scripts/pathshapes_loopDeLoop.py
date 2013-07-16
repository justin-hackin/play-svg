"""Script for generating examples of the output of compshapes.py functions
Code at `pathshapes.py <https://github.com/cosmo-guffa/play-svg/blob/master/playsvg/compshapes.py>`_
 """

from playsvg.document import *
from playsvg.element import *
from playsvg import pathshapes

stretch = 600
docu = Document()
for i in range(10,60):
    docu.append(buildPath(pathshapes.loopDeLoop(Point(-stretch,0), Point(stretch,0), 10, 20, i*0.1), {'style':'stroke:black;fill:none'} ))
docu.writeSVG("pathshapes_loopDeLoop.svg")
print "done"

