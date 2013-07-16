#python libraries
import math
from playsvg import pathshapes

#local libraries
from playsvg.geom import *
from playsvg.element import *
from playsvg.gradient import *
from playsvg.path import *
from playsvg import document


radius = 640
gridSize = 20
docu = document.Document()
trianglePoints = createRadialPlots(Point(0,0), radius, 3)
baselinePoints = getLineDivisions(trianglePoints[1], trianglePoints[2], gridSize)

tickGrid = [] 
for i in range(3):
    tickGrid.append(getLineDivisions(trianglePoints[i], trianglePoints[(i+1)%3], gridSize))

colors = ['#00a6ff','#ff009e'  ]
#colors = ['#67ff00', '#fd00ff', '#1e00ff']
triangleFillGradient = Gradient('triFill').createBalancedGradient(colors)
docu.appendDefinition(triangleFillGradient.createDefinition())
triangleFillRadGradient = RadialGradient('radFill',triangleFillGradient, radius, (Point(0,0),Point(0,0)) )
docu.appendDefinition(triangleFillRadGradient.createDefinition())
colors.reverse()
strokeFillGradient = Gradient('strokeFill').createBalancedGradient(colors)
docu.appendDefinition(strokeFillGradient.createDefinition())
strokeFillRadGradient = RadialGradient('strokeRadFill',strokeFillGradient, radius, (Point(0,0),Point(0,0)) )
docu.appendDefinition(strokeFillRadGradient.createDefinition())


faceGroup = docu.makeGroup()
trianglePath = PathData().makeHull(trianglePoints)
faceGroup.append(buildPath( trianglePath, {'style':'fill:url(#radFill)'}))

for i in range(3):
    crossPath = PathData().moveTo(tickGrid[i][0])
    for j in range(0,gridSize,2):
        crossPath.lineTo(tickGrid[i][j]).lineTo(tickGrid[(i+1)%3][j]).lineTo(tickGrid[(i+1)%3][j+1]).lineTo(tickGrid[i][j+1])
    faceGroup.append(buildPath( crossPath, {u'stroke':u'url(#strokeRadFill)',u'stroke-width':u'16', u'fill':u'none'}))
docu.append(faceGroup)
docu.writeSVG('platonicWater.svg')

print "done01"

