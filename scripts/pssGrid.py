from playsvg.document import *
from playsvg.element import *
from playsvg.path import *
import playsvg.pathshapes
import os
import string


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
docu = document.Document()
docu.appendElement( buildSubunitGrid(docu,((2,8), (2,4), (2,2), (2,1)),200))

docu.writeSVG("subunitgrid.svg" )
print "done"


