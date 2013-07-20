from playsvg.document import *
from playsvg.element import *
from playsvg.path import *


def buildCrosshatchGrid(numPoints, size):
    gridGroup = buildGroup(id='grid')
    corners = [Point(-1*size, size), Point(size, size), Point(size, -1*size), Point(-1*size, -1*size)]
    sidePoints = []
    lineAtts = {'style':'stroke:black;fill:none'}
    #append array of points along each side for top, right, bottom, left
    for i in range(4):
        sidePoints.append(getLineDivisions(corners[i], corners[(i+1)%4], numPoints))
    
    for i in range(4):
        for j in range(numPoints+1):
            print str(i) +','+str(j)
            #print sidePoints[i][numPoints-j]
        
    
    for i in range(2):
        for j in range(numPoints):
          
            #draws vertical and horizontal lines
            gridGroup.append(buildLine( sidePoints[i][j],sidePoints[(i+2)%4][numPoints-1-j], lineAtts))
    
    for i in range(4):
        for j in range(numPoints):
    
            #draws lines angled at 45 degrees
            gridGroup.append(buildLine( sidePoints[i][j],sidePoints[(i+1)%4][numPoints-1-j], lineAtts))
            
    return gridGroup

docu = Document()
docu.append(buildCrosshatchGrid(100,600))
docu.writeSVG("crosshatchGrid.svg")


