from playsvg.document import *
from playsvg.element import *
from playsvg.path import *
import math

equiTriHeightToWidth =  1 # 2*1.154441135

def convertValueToPair(value):
    valuePair = []
    val = value
    for i in range(6):
        valuePair.append(val%2)
        val = val >>1
    return valuePair
    

def makeHexagramGem(docu,pos, value, width):
    hexagramGemGroup = docu.makeGroup()
    valuePair = convertValueToPair(value)
    binToColorDict = {0:"black",1:"white"}
    for i in range(2,-1,-1):
        triPath = PathData().moveTo(Point(float(i+1)/-3*width+pos.x , pos.y)).lineTo(Point(float(i+1)/3*width+pos.x , pos.y)).lineTo(Point(pos.x  , pos.y+float(i+1)/3*width*equiTriHeightToWidth )).closePath() 
        hexagramGemGroup.appendChild(buildPath(docu, triPath,
        {'style':"stroke:orange;stroke-width:4;stroke-linejoin:round;fill:"+binToColorDict[valuePair[i]]}))
    for i in range(2,-1,-1):
        triPath = PathData().moveTo(Point(float(i+1)/-3*width+pos.x , pos.y)).lineTo(Point(float(i+1)/3*width+pos.x , pos.y)).lineTo(Point(pos.x  , pos.y+float(i+1)/-3*width*equiTriHeightToWidth )).closePath() 
        hexagramGemGroup.appendChild(buildPath(docu, triPath,
        {'style':"stroke:orange;stroke-width:4;stroke-linejoin:round;fill:"+binToColorDict[valuePair[i+3]]}))
    
    return hexagramGemGroup
    
def makeHexagramGemGrid(docu,  gemWidth):
    cellBlockGroup = docu.makeGroup()
    spacingRatio = 1.0/6
    for y in range(8):
        for x in range(8):
            cellBlockGroup.appendChild(makeHexagramGem(docu,\
            Point(2*(x+spacingRatio)*gemWidth*equiTriHeightToWidth, 2*(y+spacingRatio)*gemWidth*equiTriHeightToWidth), x+y*8,gemWidth ))
    return cellBlockGroup
   
if   __name__ == '__main__':
    #makeBigrams()

    docu = document.Document()
    docu.appendElement(makeHexagramGemGrid(docu, 50 ))
    docu.writeSVG('hexagramGemGrid.svg')
 
