from playsvg.document import *
from playsvg.element import *
from playsvg.path import *
import playsvg.pathshapes
squareSize = 400

#start top, go clockwise
outerSquare = [Point(0, squareSize), Point(squareSize, 0), Point(0, -1*squareSize), Point(-1*squareSize,0)]
innerSquare = []
for i in range(0,4):
    innerSquare.append(getMidpoint(outerSquare[i], outerSquare[(i+1)%4]))

def makeSplay(docu, points, divs):
    ticks = [getLineDivisions(points[0], points[1], divs),getLineDivisions(points[1], points[2], divs)]
    
    splayPath = PathData().moveTo(ticks[0][0])
        
    for i in range(divs-1):
        splayPath.lineTo( ticks[(i+1)%2][i]).lineTo(ticks[(i+1)%2][i+1]) 
    splayPath.closePath()
    return splayPath
  
docu = Document()
starRadius = 300
starPoints = 6
divs = 64
hexPoints = createRadialPlots(Point(), starRadius,starPoints)
for i in range(6):
    docu.appendElement(buildPath(docu, makeSplay(docu,[hexPoints[i],Point(),hexPoints[(i+1)%starPoints]], divs ), {'style':'stroke:black; stroke-width:1'}))

docu.writeSVG('hexsplay64.svg')
print "done"
