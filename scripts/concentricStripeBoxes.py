from playsvg.document import *
from playsvg.element import *
from playsvg.path import *
import playsvg.pathshapes
import os
import string

def makeCentredBox(docu, size):
    boxPath = PathData().moveTo(Point(size, size)).\
            lineTo(Point(size, -1*size)).\
            lineTo(Point(-1*size, -1*size)).\
            lineTo(Point(-1*size, size)).closePath()
    return boxPath

def makeStripeBox(docu, layers, layerSize):
    stripeBoxGroup = docu.makeGroup()
    for i in range(layers,0, -1):
        if i%2 == 0:
            stripeBoxGroup.appendChild(buildPath(docu, makeCentredBox(docu, i*layerSize),{'style': 'stroke:none;fill:black'})) 
        else:
            stripeBoxGroup.appendChild(buildPath(docu, makeCentredBox(docu, i*layerSize),{'style': 'stroke:none;fill:white'})) 
    return stripeBoxGroup    

docu = document.Document()
docu.appendElement(makeStripeBox(docu,20, 20 ))

docu.writeSVG("concentricStripeBox.svg" )
print "done"

