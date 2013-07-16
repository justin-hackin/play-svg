"""Script for generating examples of the output of compshapes.py functions
Code at `pathshapes.py <https://github.com/cosmo-guffa/play-svg/blob/master/playsvg/compshapes.py>`_
 """

from playsvg.document import *
from playsvg.element import *
from playsvg import pathshapes

docu = Document()
arcRingRadius= [300,200,100]
numArcs = 12
for h in range(len(arcRingRadius)):
    radialPlots = createRadialPlots(Point(), arcRingRadius[h], numArcs)
    ringGroup = buildGroup()
    for i in range(numArcs):
        thisArc = buildPath(pathshapes.arcSpire(radialPlots[i], radialPlots[(i+1)%numArcs], 2, 4), {'style':'stroke:none;fill:black'} )
        ringGroup.append(thisArc)
    docu.append(ringGroup)

docu.writeSVG("pathshapes_arcSpire.svg")

