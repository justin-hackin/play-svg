from playsvg.document import *
from playsvg.element import *
from playsvg.path import *
import playsvg.pathshapes
import os
import string

sideLength = 50
gridPoints = createTriangularGrid(Point(0,0), sideLength, 11)

def buildTriangularGrid(docu, levels):
    '''creates a triangular grid bounded by a large triangle, grouped into upward pointing and downward pointing triangles '''
    
    gridGroup = docu.makeGroup('triangulargrid')
    triAttrs = {'style':'stroke:black;fill:none'}
    
    upwardTriangles = docu.makeGroup('upwardtriangles')
    for i in range(levels-1):
        for j in range(i+1):
            triangulatePath = PathData()
            apex = gridPoints[i][j]
            leftBase = gridPoints[i+1][j]
            rightBase = gridPoints[i+1][j+1]
            triangulatePath.moveTo(apex).lineTo(leftBase).lineTo(rightBase).closePath()
            upwardTriangles.appendChild(buildPath(docu, triangulatePath, triAttrs))
    gridGroup.appendChild(upwardTriangles)
    
    downwardTriangles = docu.makeGroup('downwardtriangles')
    for i in range(1, levels-1):
        for j in range(i):
            triangulatePath = PathData()
            leftArm = gridPoints[i][j]
            rightArm = gridPoints[i][j+1]
            balance = gridPoints[i+1][j+1]
            triangulatePath.moveTo(leftArm).lineTo(rightArm).lineTo(balance).closePath()
            downwardTriangles.appendChild(buildPath(docu, triangulatePath, triAttrs))
    gridGroup.appendChild(downwardTriangles)
    contPath = PathData().moveTo(Point(0,0)).lineTo(gridPoints[-1][0]).lineTo(gridPoints[-1][-1]).closePath()
    gridGroup.appendChild(buildPath(docu, contPath, triAttrs ))
    return gridGroup
    
    
docu = document.Document()
docu.appendElement( buildTriangularGrid(docu,11))
heavenBox = PathData().moveTo(gridPoints[0][0]).lineTo(gridPoints[2][0]).lineTo(gridPoints[2][2]).closePath()
docu.appendElement(buildPath(docu, heavenBox, {'style':'stroke:orange;fill:white'}))
humanBox = PathData().moveTo(gridPoints[4][0]).lineTo(gridPoints[4][4]).lineTo(gridPoints[6][6]).lineTo(gridPoints[6][0]).closePath()
docu.appendElement(buildPath(docu, humanBox, {'style':'stroke:orange;fill:grey'}))
earthBox = PathData().moveTo(gridPoints[8][0]).lineTo(gridPoints[8][8]).lineTo(gridPoints[10][10]).lineTo(gridPoints[10][0]).closePath()
docu.appendElement(buildPath(docu, earthBox, {'style':'stroke:orange;fill:black'}))

docu.writeSVG("trigramgrid.svg" )
print "done"
