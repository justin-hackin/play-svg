#python libraries
import math
from playsvg import pathshapes

#local libraries
from playsvg.geom import *
from playsvg.element import *
from playsvg.gradient import *
from playsvg.path import *
from playsvg import document


lineHeightToWidth = 1.0/6
lineSpacing = 0



def buildToneLine(docu, value,position, width):
        lineGroup = docu.makeGroup()
        if value == 0:
            lineGroup.appendChild(buildRect(docu,Point(position.x - 0.5*width,position.y),lineHeightToWidth*width, width, {u'fill':u'black', u'stroke':u'none'}))
        elif value == 1:
            lineGroup.appendChild(buildRect(docu,Point(position.x - 0.5*width,position.y),lineHeightToWidth*width, width, {u'fill':u'white', u'stroke':u'none'}))
        
        return lineGroup
    


def buildTieredGram(docu, valuePair, position, width):
    gramGroup = docu.makeGroup()
    currentPosition = position
    for i in range(len(valuePair)):
        gramGroup.appendChild(buildToneLine(docu, valuePair[i], currentPosition, width))
        currentPosition = currentPosition + Point(0, lineHeightToWidth*width*(1+lineSpacing))
    return gramGroup
    


def convertValueToPair(value):
    valuePair = []
    val = value
    for i in range(6):
        valuePair.append(val%2)
        val = val >>1
    return valuePair
    
def digramCentred(docu,value, centrePoint, width):
    gramGroup = docu.makeGroup()
    bottomLine = (value-1) % 3 
    topLine = ((value-1) - ((value-1)%3))/3
    gramGroup.appendChild(buildTriLine(docu, topLine, centrePoint + Point(0,0.5*lineHeightToWidth*width*lineSpacing), width))
    gramGroup.appendChild(buildTriLine(docu, bottomLine, centrePoint - Point(0,0.5*lineHeightToWidth*width*lineSpacing+lineHeightToWidth*width), width))
    return gramGroup


    
if   __name__ == '__main__':
    docu = Document()
    gramSize = 50
    
    for y in range(8):
        for x in range(8):
            docu.appendElement(buildTieredGram(docu, convertValueToPair(y*8 + x), Point(x*gramSize, y*gramSize), gramSize))
    docu.writeSVG('ichinggrid.svg')
    print 'done'
