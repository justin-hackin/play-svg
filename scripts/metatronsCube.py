"""Generates a Metatron's Cube, more info on the shape here: http://en.wikipedia.org/wiki/Flower_of_Life"""
from playsvg import document
import playsvg.pathshapes
from playsvg.path import *
from playsvg.geom import *
from playsvg.element import *

docu = document.Document()
circleCentreArray = []

def buildMetatronCube(docu):
    level = 5
    radius = 50
    lineAttrs = {'style':'stroke:black;fill:none'}
    circleAttrs = {'style':'stroke:black;fill:none'}
    
    #define color ring array
    containerGroup = etree.Element('g')
    circlesGroup = etree.Element('g')
    linesGroup = etree.Element('g')
    cubeGroup = etree.Element('g')
    distFromHex = radius*math.sin((0.5-1.0/6)*2*math.pi)/math.sin(1.0/12*2*math.pi)
    
    #creates a co-ordinate grid based on flower of life pattern
    for i in range(1,level):
        circleCentreArray.append([])
        
        #corners of an invisible hexagon on which the concentric hexagons will be centred on
        hexagonFrame = []
        
        for j in range(6):
            hexagonFrame.append(PolerPoint(i*radius , float(j)/6).convertToCartesian()) 
           
        #each line of the invisible hexagon is equally divided into n points where n is the layer number
        #hexagons are plotted on these points
        for j in range(6):
            latticePath = PathData()
            sidePoints = []
            circleCentreArray[-1].append(getLineDivisions(hexagonFrame[j], hexagonFrame[(j+1)%6], i+1)[0:-1])
    
    metatronCoord = [(1,0,0),(1,1,0),(1,2,0),(1,3,0),(1,4,0), (1,5,0), (3,0,0),(3,1,0),(3,2,0),(3,3,0),(3,4,0), (3,5,0)]
    metatronPoints = []
    metatronLines = etree.Element('g')
    for (i,j,k) in metatronCoord:
        metatronPoints.append(circleCentreArray[i][j][k])
    metatronPoints.append(Point(0,0))
    
    
    
    for i in range(len(metatronPoints)):
        circlesGroup.append(buildCircle( metatronPoints[i], radius, circleAttrs))
        for j in range(i):
            linesGroup.append(buildLine( metatronPoints[i], metatronPoints[j], lineAttrs)  )
    
    
    cubeGroup.append(circlesGroup)
    cubeGroup.append(linesGroup)   
    return cubeGroup



docu.append(buildMetatronCube(docu))

docu.writeSVG('metatrons_cube.svg')
print "done"

