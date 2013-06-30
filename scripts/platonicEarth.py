from playsvg import document
from playsvg.geom import *
from playsvg.element import *
from playsvg.path import *

docu = document.Document()
centre = Point(0,0)

squares = 11
size = 300
boxSize = float(size)/squares
corners = [] #defined in order of top-left, top-right, bottom-right, bottom left
quadSize = -1*size/2.0
upperCorner = Point(quadSize,quadSize)
checkerGrid = []
for i in range(squares+1):
    checkerGrid.append([])
    for j in range(squares+1):
        checkerGrid[-1].append(Point(quadSize + i*boxSize, quadSize +j*boxSize))



lightBoxPath = PathData()
darkBoxPath = PathData()
squareLength = float(size)/squares


for i in range(squares):
    for j in range(squares):
        if (i+j)%2 == 1:
            darkBoxPath.moveTo(checkerGrid[i][j]).lineTo(checkerGrid[i+1][j]).lineTo(checkerGrid[i+1][j+1]).lineTo(checkerGrid[i][j+1]).lineTo(checkerGrid[i][j])
        else:
            lightBoxPath.moveTo(checkerGrid[i][j]).lineTo(checkerGrid[i+1][j]).lineTo(checkerGrid[i+1][j+1]).lineTo(checkerGrid[i][j+1]).lineTo(checkerGrid[i][j])



#4 quadrants    
innerSize = 300
outerSize = 800

innerCorners = []
outerCorners = []
innerCorners.append(Point(1*innerSize/2.0, 1*innerSize/2.0))
outerCorners.append(Point(outerSize/2.0, outerSize/2.0))
innerCorners.append(Point(1*innerSize/2.0, -1*innerSize/2.0))
outerCorners.append(Point(outerSize/2.0, -1*outerSize/2.0))
innerCorners.append(Point(-1*innerSize/2.0, -1*innerSize/2.0))
outerCorners.append(Point(-1*outerSize/2.0, -1*outerSize/2.0))
innerCorners.append(Point(-1*innerSize/2.0, 1*innerSize/2.0))
outerCorners.append(Point(-1*outerSize/2.0, outerSize/2.0))
ratios = perspectiveDistanceRatioArray(1.0/8, squares+1)

for corner in range(len(innerCorners)):
    innerMarks = getLineDivisions(innerCorners[corner], innerCorners[(corner+1)%4], squares+1)
    outerMarks = getLineDivisions(outerCorners[corner], outerCorners[(corner+1)%4],squares+1)
    for j in range(squares): 
        leftMarks = getLineDivisionsWithRatios( outerMarks[j], innerMarks[j], ratios)
        rightMarks = getLineDivisionsWithRatios( outerMarks[j+1],innerMarks[j+1], ratios)
        for k in range(squares):
            if (j+k)%2 == 1 :
                lightBoxPath.moveTo(leftMarks[k]).lineTo(rightMarks[k]).lineTo(rightMarks[k+1]).lineTo(leftMarks[k+1]).lineTo(leftMarks[k])
            else:
                darkBoxPath.moveTo(leftMarks[k]).lineTo(rightMarks[k]).lineTo(rightMarks[k+1]).lineTo(leftMarks[k+1]).lineTo(leftMarks[k])

docu.append(buildPath( lightBoxPath, {'style':'fill:#7cff00; stroke:black; stroke-width:3'}))
docu.append(buildPath( darkBoxPath, {'style':'stroke:black; stroke-width:3;fill:#faff00'}))

    
docu.writeSVG('platonicEarth.svg')

