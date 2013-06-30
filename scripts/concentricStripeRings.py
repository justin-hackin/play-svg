from playsvg.document import *
from playsvg.element import *
from playsvg.path import *
import playsvg.pathshapes
import os
import string



def makeStripeRings(docu, layers, layerSize):
    stripeRingGroup = docu.makeGroup()
    for i in range(layers, 0, -1):
        if i%2 == 1:
            stripeRingGroup.append(buildCircle(Point(0,0),i*layerSize ,{'style': 'stroke:none;fill:black'})) 
        else:
            stripeRingGroup.append(buildCircle(Point(0,0),i*layerSize ,{'style': 'stroke:none;fill:white'})) 
    return stripeRingGroup    

docu = document.Document()
docu.append(makeStripeRings(20, 20 ))

docu.writeSVG("concentricStripeRings_rev.svg" )
print "done"

