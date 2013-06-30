#python libraries
import math
from playsvg import pathshapes

#local libraries
from playsvg.geom import *
from playsvg.element import *
from playsvg.gradient import *
from playsvg import document
from playsvg import gradshape

docu = document.Document()
startPoint = Point(0,0)
levels = 6
#length of one side of one triangle in the grid
sideLength = 80 

#distance from center of a tile to one of its corners
trigridRadius = sideLength /  (math.sin(1.0/3*tewpi)*math.sin(1.0/12*tewpi)*4.0) 

tetractysArray = []
abraGroup = docu.makeGroup()
tetractysArray = createTriangularGrid(Point(0,0), sideLength, levels)
#upGradientColors = [ '#fd00ff','#67ff00','#1e00ff']
upGradientColors = [ '#a500ff', '#ff009e']
upGradient = Gradient('grade000')
upGradient.createBalancedGradient(upGradientColors)
upGradientColors.reverse()
#upGradients order becomes reversed
downGradientColors = upGradientColors
downGradient = Gradient('grade000')
downGradient.createBalancedGradient(downGradientColors)
    
upTriangles = docu.makeGroup('upsies')
for i in range(levels-1):
    for j in range(i+1):
        upGradient.id = 'upgrade' + str(i*11+j)
        docu.appendDefinition(upGradient.createDefinition(docu))
        points = []
        points = [tetractysArray[i][j],  tetractysArray[i+1][j+1],  tetractysArray[i+1][j] ]
        upTriangles.append(gradshape.polygonGradient( points, upGradient, id ='up'+str(i*11+j)))
abraGroup.append(upTriangles)

downTriangles = docu.makeGroup('downsies')
for i in range(1, levels-1):
    for j in range(i):
        downGradient.id = 'downgrade' + str(i*11+j)
        docu.appendDefinition(downGradient.createDefinition(docu))
        points = []
        points = [tetractysArray[i][j],  tetractysArray[i+1][j+1], tetractysArray[i][j+1]]
        downTriangles.append(gradshape.polygonGradient( points, downGradient, id ='down'+str(i*11+j) ))
abraGroup.append(downTriangles)
 
docu.append(abraGroup)

###create shaded overlay
##SupGradientColors = [ '#ff009e', '#a500ff']
##SupGradient = Gradient('sgrade000')
##SupGradient.createBalancedGradient(SupGradientColors)
##SupGradient.id = 'supgrade'
##docu.appendDefinition(SupGradient.createDefinition(docu))
##points = [tetractysArray[0][0],  tetractysArray[5][0],  tetractysArray[5][5] ]
##docu.append(gradshape.polygonGradient( points, SupGradient, id ='supgrade'))
##

#innerTriangleCorners = ((0,0), (6,6), (0,6)),((10, 6), (0,6),(6,6)), ((10,0), ())

docu.writeSVG('platonicFire.svg')

print "done01"

