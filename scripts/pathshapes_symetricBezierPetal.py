"""Script for generating examples of the output of compshapes.py functions
Code at `pathshapes.py <https://github.com/cosmo-guffa/play-svg/blob/master/playsvg/compshapes.py>`_
 """

from playsvg.document import *
from playsvg.element import *
from playsvg import pathshapes

petalRadius = 600
numPetals = 30
flowerID = "petalspin"
docu = Document()

aPetal = buildPath(pathshapes.symetricBezierPetal(Point(-petalRadius,0), Point(petalRadius,0),(0.5,0.1) ), {'id':flowerID, 'style':'stroke:black;fill:none'} )
docu.append(aPetal)

for i in range(1,numPetals):
    thisClone = buildUse(flowerID, {'transform':'rotate('+str(float(i)/numPetals*360)+')'})
    docu.append(thisClone)

docu.writeSVG("pathshapes_symetricBezierPetal.svg")
