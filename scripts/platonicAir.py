#python libraries
import math
import pathshapes

#local libraries
from playsvg.geom import *
from playsvg.element import *
from playsvg.gradient import *
from playsvg.path import *
from playsvg import document
from playsvg import gradshape

radius = 260
gridSize = 11
docu = document.Document()
trianglePoints = createRadialPlots(Point(0,0), radius, 3)
baselinePoints = getLineDivisions(trianglePoints[1], trianglePoints[2], gridSize)

#upGradientColors = [  '#E60066', '#33FF00', '#E60066']
checkerColors = [ '#7cff00', '#00b7ff' ]

perspectiveGrid = [] 
ratios = perspectiveDistanceRatioArray(1.0/5, gridSize)

print ratios
for i in range(gridSize):
    perspectiveGrid.append(getLineDivisionsWithRatios(baselinePoints[i],trianglePoints[0], ratios) )


faceGroup = docu.makeGroup()
for i in range(gridSize-1):
    for j in range(gridSize-2):
        boxPoints = [perspectiveGrid[i][j], perspectiveGrid[i+1][j], perspectiveGrid[i+1][j+1], perspectiveGrid[i][j+1]]
        faceGroup.appendChild(buildPath(docu, PathData().makeHull(boxPoints),{'style':'stroke:black;stroke-width:1;fill:'+checkerColors[(i+j)%2]} ))
j = gridSize-2
for i in range(gridSize-1):
##        boxPath = PathData().moveTo(perspectiveGrid[i][j]).\
##        lineTo(perspectiveGrid[i][j+1]).lineTo(perspectiveGrid[i+1][j+1]).lineTo(perspectiveGrid[i+1][j]).closePath()
        triPoints = [trianglePoints[0],perspectiveGrid[i][j], perspectiveGrid[i+1][j] ]
        faceGroup.appendChild(buildPath(docu, PathData().makeHull(triPoints),{'style':'stroke:black;stroke-width:1;fill:'+checkerColors[(i+j)%2]} ))
        
docu.appendElement(faceGroup)
docu.writeSVG('platonicAir.svg')
