from playsvg.document import *
from playsvg.element import *
from playsvg.path import *
from playsvg import compshapes

def buildCrosshatchGrid(docu, numPoints, size):
    gridGroup = docu.makeGroup()
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
            gridGroup.appendChild(buildLine(docu, sidePoints[i][j],sidePoints[(i+2)%4][numPoints-1-j], lineAtts))
    
    for i in range(4):
        for j in range(numPoints):
    
            #draws lines angled at 45 degrees
            gridGroup.appendChild(buildLine(docu, sidePoints[i][j],sidePoints[(i+1)%4][numPoints-1-j], lineAtts))
            
    return gridGroup

docu = Document()
docu.appendElement(buildCrosshatchGrid(docu, 10,100))
docu.writeSVG("crosshatch_grid.svg")


