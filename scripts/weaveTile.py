from playsvg.document import *
from playsvg.element import *
from playsvg.path import *
import playsvg.pathshapes
import os
import string



def buildWeaveTile( boxSize, stripWidthRatio):
    weaveGroup = etree.Element('g', id='weavetile')
    fillGroup = etree.Element('g', id='filling')
    lineGroup = etree.Element('g', id='lines')
    fillAttr = {'style':'fill:red; stroke: none'}
    lineAttrs = {'style':'stroke: black;stroke-linecap:none'}
    guideRatios = [0.25-0.25*stripWidthRatio,0.25+0.25*stripWidthRatio,  0.75-0.25*stripWidthRatio,0.75+0.25*stripWidthRatio ]
    #add filling
    
    #short flaps
    stripBoxPoints = [Point(guideRatios[0]*boxSize, 0), Point(guideRatios[1]*boxSize, 0),\
    Point(guideRatios[1]*boxSize, guideRatios[0]*boxSize), Point(guideRatios[0]*boxSize, guideRatios[0]*boxSize) ]
    fillerPath = PathData().makeHull(stripBoxPoints)
    fillGroup.append(buildPath( fillerPath, fillAttr))
    lineGroup.append(buildLine( stripBoxPoints[0], stripBoxPoints[3], lineAttrs))
    lineGroup.append(buildLine( stripBoxPoints[1], stripBoxPoints[2], lineAttrs))
    
    stripBoxPoints = [Point(boxSize, guideRatios[0]*boxSize),Point(boxSize, guideRatios[1]*boxSize), \
    Point(guideRatios[3]*boxSize, guideRatios[1]*boxSize), Point(guideRatios[3]*boxSize, guideRatios[0]*boxSize)]
    fillerPath = PathData().makeHull(stripBoxPoints)
    fillGroup.append(buildPath( fillerPath, fillAttr))
    lineGroup.append(buildLine( stripBoxPoints[0], stripBoxPoints[3], lineAttrs))
    lineGroup.append(buildLine( stripBoxPoints[1], stripBoxPoints[2], lineAttrs))
    
    stripBoxPoints = [Point(guideRatios[3]*boxSize, boxSize), Point(guideRatios[2]*boxSize, boxSize), \
    Point(guideRatios[2]*boxSize, guideRatios[3]*boxSize),Point(guideRatios[3]*boxSize, guideRatios[3]*boxSize)]
    fillerPath = PathData().makeHull(stripBoxPoints)
    fillGroup.append(buildPath( fillerPath, fillAttr))
    lineGroup.append(buildLine( stripBoxPoints[0], stripBoxPoints[3], lineAttrs))
    lineGroup.append(buildLine( stripBoxPoints[1], stripBoxPoints[2], lineAttrs))
    
    stripBoxPoints = [Point(0,guideRatios[3]*boxSize), Point(0,guideRatios[2]*boxSize), \
    Point(guideRatios[0]*boxSize, guideRatios[2]*boxSize), Point(guideRatios[0]*boxSize, guideRatios[3]*boxSize)]
    fillerPath = PathData().makeHull(stripBoxPoints)
    fillGroup.append(buildPath( fillerPath, fillAttr))
    lineGroup.append(buildLine( stripBoxPoints[0], stripBoxPoints[3], lineAttrs))
    lineGroup.append(buildLine( stripBoxPoints[1], stripBoxPoints[2], lineAttrs))
    
    #draw long strips 
    
    stripBoxPoints = [Point(guideRatios[0]*boxSize, guideRatios[1]*boxSize), Point(guideRatios[1]*boxSize, guideRatios[1]*boxSize),\
    Point(guideRatios[1]*boxSize, boxSize), Point(guideRatios[0]*boxSize, boxSize) ]
    fillerPath = PathData().makeHull(stripBoxPoints)
    fillGroup.append(buildPath( fillerPath, fillAttr))
    lineGroup.append(buildLine( stripBoxPoints[0], stripBoxPoints[3], lineAttrs))
    lineGroup.append(buildLine( stripBoxPoints[1], stripBoxPoints[2], lineAttrs))
    
    stripBoxPoints = [Point(guideRatios[2]*boxSize, guideRatios[0]*boxSize),Point(guideRatios[2]*boxSize, guideRatios[1]*boxSize), \
    Point(0, guideRatios[1]*boxSize), Point(0, guideRatios[0]*boxSize)]
    fillerPath = PathData().makeHull(stripBoxPoints)
    fillGroup.append(buildPath( fillerPath, fillAttr))
    lineGroup.append(buildLine( stripBoxPoints[0], stripBoxPoints[3], lineAttrs))
    lineGroup.append(buildLine( stripBoxPoints[1], stripBoxPoints[2], lineAttrs))
    
    stripBoxPoints = [Point(guideRatios[3]*boxSize, guideRatios[2]*boxSize), Point(guideRatios[2]*boxSize, guideRatios[2]*boxSize), \
    Point(guideRatios[2]*boxSize, 0),Point(guideRatios[3]*boxSize, 0)]
    fillerPath = PathData().makeHull(stripBoxPoints)
    fillGroup.append(buildPath( fillerPath, fillAttr))
    lineGroup.append(buildLine( stripBoxPoints[0], stripBoxPoints[3], lineAttrs))
    lineGroup.append(buildLine( stripBoxPoints[1], stripBoxPoints[2], lineAttrs))
    
    stripBoxPoints = [Point(guideRatios[1]*boxSize,guideRatios[3]*boxSize), Point(guideRatios[1]*boxSize,guideRatios[2]*boxSize), \
    Point(boxSize, guideRatios[2]*boxSize), Point(boxSize, guideRatios[3]*boxSize)]
    fillerPath = PathData().makeHull(stripBoxPoints)
    fillGroup.append(buildPath( fillerPath, fillAttr))
    lineGroup.append(buildLine( stripBoxPoints[0], stripBoxPoints[3], lineAttrs))
    lineGroup.append(buildLine( stripBoxPoints[1], stripBoxPoints[2], lineAttrs))
    
    
    #add both groups tile
    
    weaveGroup.append(fillGroup)
    weaveGroup.append(lineGroup)
    
    return weaveGroup

    

docu = document.Document()
docu.append( buildWeaveTile(100, 0.5 ))
docu.append( buildWeaveTile(100, 0.3 ))
docu.append( buildWeaveTile(100, 0.1 ))
docu.writeSVG("weave_tile.svg" )
print "done"


