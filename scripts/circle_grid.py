"""Generates a Metatron's Cube, more info on the shape here: http://en.wikipedia.org/wiki/Flower_of_Life"""
from playsvg import document
import playsvg.pathshapes
from playsvg.path import *
from playsvg.geom import *
from playsvg.element import *

docu = document.Document()
circleCentreArray = []

def buildCircleGrid(columns, rows, radius, radiusSpacingRatio):
    spacing = radiusSpacingRatio*radius
    radiusAndSpace = radius + spacing
    circlesGroup = etree.Element('g')

    circleAttrs = {'style':'stroke:blue;fill:blue; fill-opacity:0'}
    
    for i in range(columns):
        yStart = 0
        thisRows = rows
        if (i%2==1): 
            yStart = radiusAndSpace
            thisRows-=1
        xval = i*radiusAndSpace*2*(math.sqrt(3.0)/2.0)       
        for j in range(thisRows):
            yVal = yStart + j*radiusAndSpace*2 
            circlesGroup.append(buildCircle(Point(xval, yVal), radius, circleAttrs) )
    return circlesGroup
        


docu.append(buildCircleGrid(24, 48, 45, 1.0/32))

docu.writeSVG('circle_grid.svg')
print "done"

