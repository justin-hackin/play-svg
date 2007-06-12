"""generates a circular wave pattern"""
import playsvg.document
import playsvg.pathshapes
from playsvg.geom import *
from playsvg.element import *
from playsvg.path import *
docu = document.Document()
gridSize = 200
squareSizeRatio = []
numSquaresHalf = 22
perspectiveAngal = 0.1
checkerGroup = docu.makeGroup("sphericheckers")
darkGroup = docu.makeGroup("darkbox")
lightGroup = docu.makeGroup("lightbox")



def pathRect(corner1, corner2):
    rectPath = PathData().moveTo(corner1).lineTo(Point(corner2.x, corner1.y)).\
    lineTo(corner2).lineTo(Point(corner1.x, corner2.y)).closePath()
    return rectPath
###concave version    
##firstHalf = perspectiveDistanceRatioArray(perspectiveAngal, numSquaresHalf)
##secondHalf = [1+ (1- i) for i in perspectiveDistanceRatioArray(perspectiveAngal, numSquaresHalf)[:-1]]
##secondHalf.reverse()
##squareSizeRatio.extend(firstHalf)
##squareSizeRatio.extend(secondHalf)
#convex version
firstHalf = [1- i for i in perspectiveDistanceRatioArray(perspectiveAngal, numSquaresHalf)]
firstHalf.reverse()
secondHalf = [1+i for i in perspectiveDistanceRatioArray(perspectiveAngal, numSquaresHalf)[1:]]

squareSizeRatio.extend(firstHalf)
squareSizeRatio.extend(secondHalf)

print squareSizeRatio
squarePosition = [i*gridSize for i in squareSizeRatio] 
for x in range(len(squarePosition)-1):
    for y in range(len(squarePosition)-1):
        thisRect = pathRect(Point(squarePosition[x], squarePosition[y]),\
        Point(squarePosition[x+1], squarePosition[y+1]))
        if (x+y)%2 == 1 :
            darkGroup.appendChild(buildPath(docu, thisRect\
            , {'style':'fill:black; stroke:none'}))
        else:
            lightGroup.appendChild(buildPath(docu, thisRect\
            , {'style':'fill:white; stroke:none'}))
        
checkerGroup.appendChild(lightGroup)
checkerGroup.appendChild(darkGroup)
docu.appendElement(checkerGroup)
docu.writeSVG('checkerd_box.svg')

