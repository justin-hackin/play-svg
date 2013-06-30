from playsvg.document import *
from playsvg.element import *
from playsvg.path import *
import playsvg.pathshapes



lineHeightToWidth = 1.0/8
lineSpacing = 1
singleGapWidthRatio = 1.0/5
doubleGapWidthRatio = 1.0/5
lineAttributes = {u'fill':u'black', u'stroke':u'none'}



def makeBigramCell(docu,pos, value, radius):
    bigramCellGroup = docu.makeGroup()
    valueColorDict = {0: "white", 1:"grey", 2:"black"}
    strokeToRadiusRatio = 1/9.0
    bottomLineVal = (value-1)%3
    topLineVal = int(math.floor(float(value-1)/3.0))
    bigramCellGroup.appendChild(buildCircle(docu, pos, radius,\
    {'style':"stroke:orange;stroke-width:"+str(strokeToRadiusRatio*radius)+";fill:"+valueColorDict[topLineVal]}))
    bigramCellGroup.appendChild(buildCircle(docu, pos, radius/2.0,\
    {'style':"stroke:orange;stroke-width:"+str(strokeToRadiusRatio*radius)+";fill:"+valueColorDict[bottomLineVal]}))
    return bigramCellGroup



    
def makeLoShuCellBlock(docu, pos, arrangement, cellBlockSize):
    spacingRatio = 8.0/9
    cellSize = spacingRatio*cellBlockSize/2
    cellBlockGroup = docu.makeGroup()
    for y in range(3):
        for x in range(3):
            cellBlockGroup.appendChild(makeBigramCell(docu, pos+Point((x-1)*cellBlockSize, -1*(y-1)*cellBlockSize),arrangement[y][x],cellSize ))
    return cellBlockGroup

def makeCellBlockArrangement(docu, arrangementSize):
    cellBlockArrangementGroup = docu.makeGroup()
    arrangements = \
    [[[6,1,8],[7,5,3],[2,9,4]],
    [[8,1,6],[3,5,7],[4,9,2]],
    [[4,9,2],[3,5,7],[8,1,6]],
    [[2,9,4],[7,5,3],[6,1,8]],
    [[8,3,4],[1,5,9],[6,7,2]],
    [[6,7,2],[1,5,9], [8,3,4]],
    [[2,7,6],[9,5,1], [4,3,8]],
    [[4,3,8],[9,5,1], [2,7,6]]]
    arrangementPosDict = {0:(11,18),1:(4,18),2:(11,4), 3:(18,4), 4:(4,11), 5:(4,4), 6:(18,11),7:(18,18)}
    for i in range(8):
        cellBlockArrangementGroup.appendChild(makeLoShuCellBlock(docu, Point(arrangementPosDict[i][0]/22.0*arrangementSize, arrangementPosDict[i][1]/22.0*arrangementSize), arrangements[i], arrangementSize*1.0/11))
    return cellBlockArrangementGroup

def buildSubunitGrid(docu, pss, width):
    '''Builds a wheel with spokes of varying widths to represent subunit division i.e. ruler ticks.  
    pss is represented as a list of (division, width) pairs (division being > 1).  The first division divides the wheel 
    into any number of sections.  Every subsequent division divides all sections into the 
    specified number of subsections.'''
    gridGroup = docu.makeGroup()
    gridGroup.appendChild(buildLine(docu,Point(0,0), Point(0,width) ,{'style':'stroke:black;stroke-width:' + str(pss[0][1])}))
    gridGroup.appendChild(buildLine(docu,Point(width,0), Point(width,width) ,{'style':'stroke:black;stroke-width:' + str(pss[0][1])}))
    gridGroup.appendChild(buildLine(docu,Point(0,0), Point(width,0) ,{'style':'stroke:black;stroke-width:' + str(pss[0][1])}))
    gridGroup.appendChild(buildLine(docu,Point(0,width), Point(width,width) ,{'style':'stroke:black;stroke-width:' + str(pss[0][1])}))
    
    #Spoke subdivision
    dividedInto=1

    for i in range(0,len(pss)):
        if i != 0: 
            divdedInto = dividedInto*pss[i-1][0]
        toDivideInto = dividedInto*pss[i][0]
        
        for j in range(0, toDivideInto):
            if j % (toDivideInto/dividedInto)  != 0 or i==0 :  #if there is no division made at j or we're in the first round of divisions make one
                print j
                theRatio = float(j)/toDivideInto
                gridGroup.appendChild( \
                buildLine(docu, 
                    Point(0,theRatio*width),Point(width, theRatio*width), 
                    {'style':'stroke:black;stroke-width:' + str(pss[i][1])}))
                gridGroup.appendChild( \
                buildLine(docu, 
                    Point(theRatio*width,0),Point(theRatio*width, width), 
                    {'style':'stroke:black;stroke-width:' + str(pss[i][1])}))
        dividedInto=toDivideInto

    return gridGroup 
    
if   __name__ == '__main__':
    #makeBigrams()
##    
##    docu = document.Document()
####    docu.appendElement(buildDigramLine(docu, 2 ,Point(0,0), 40) )
##    
##    docu.appendElement(buildTieredGram(docu, (0,2,1,1,0) ,Point(0,0), 64) )
##    
    docu = document.Document()
    docu.appendElement(makeBigramCell(docu, Point(), 5,200 ))
    docu.writeSVG('trigramCellTest.svg')
    
##    docu = document.Document()
##    docu.appendElement(makeLoShuCellBlock(docu, Point(), arrangements[0], 50))
##    docu.writeSVG('trigramCellBlockTest.svg')

    docu = Document()
    arrangementSize = 550
    
    
    
    docu.appendElement( buildSubunitGrid(docu,((2,1), (11,1)),arrangementSize))
    docu.appendElement(makeCellBlockArrangement(docu,arrangementSize ))
    swastikaCoord = (((9,13), (11,13), (11,9), (13,9)),((13,13),(13,11), (9,11),(9,9)))
    swastikaPath = PathData()
    for line in swastikaCoord:
        swastikaPath.moveTo(Point(line[0][0]/22.0*arrangementSize, line[0][1]/22.0*arrangementSize)) 
        for i in range(1,len(line)):
            swastikaPath.lineTo(Point(line[i][0]/22.0*arrangementSize, line[i][1]/22.0*arrangementSize))
    
    docu.appendElement(buildPath(docu,swastikaPath,  {'style':'fill:none;stroke:black;stroke-width:7'}))
    docu.writeSVG('trigramCellBlockArrangementTest.svg')
