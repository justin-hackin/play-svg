"""generates a circular wave pattern"""
import playsvg.document
import playsvg.pathshapes
from playsvg.geom import *
from playsvg.element import *
from playsvg.path import *
centreBoxRatio = 1.0/3
spacerRatio = 1.0/16
cornerInsetRatio =  (1-centreBoxRatio)/2 - spacerRatio
elBoxRatio = cornerInsetRatio - spacerRatio
size = 300
#draw corner-chipped box
docu = document.Document()
corneredBox = PathData().moveTo(Point(cornerInsetRatio*size, 0)).lineTo(Point(size, 0)).\
                        lineTo(Point(size, (1-cornerInsetRatio)*size)).lineTo(Point((1-cornerInsetRatio)*size, (1-cornerInsetRatio)*size)).\
                        lineTo(Point((1-cornerInsetRatio)*size, size)).lineTo(Point(0,size)).\
                        lineTo(Point(0, cornerInsetRatio*size)).lineTo(Point(cornerInsetRatio*size, cornerInsetRatio*size)).closePath()
docu.append(buildPath( corneredBox , {'style':'stroke:black;fill:none'}))

darkBlocks = PathData().moveTo(Point((cornerInsetRatio + spacerRatio)*size, spacerRatio*size)).lineTo(Point((1-spacerRatio)*size, spacerRatio*size)).lineTo(Point((1-spacerRatio)*size, (1-cornerInsetRatio-spacerRatio)*size)).\
                                        lineTo(Point((1-cornerInsetRatio+spacerRatio)*size, (1-cornerInsetRatio-spacerRatio)*size)).lineTo(Point((1-cornerInsetRatio+spacerRatio)*size, (cornerInsetRatio-spacerRatio)*size)).lineTo(Point((cornerInsetRatio+spacerRatio)*size,(cornerInsetRatio-spacerRatio)*size)).closePath()
                                        
                                        
docu.append(buildPath( darkBlocks , {'style':'stroke:none;fill:black'}))


darkBlocks = PathData().moveTo(Point( spacerRatio*size, (cornerInsetRatio + spacerRatio)*size)).lineTo( Point( spacerRatio*size, (1-spacerRatio)*size )).lineTo(Point( (1-cornerInsetRatio-spacerRatio)*size, (1-spacerRatio)*size)).\
                                        lineTo(Point((1-cornerInsetRatio-spacerRatio)*size, (1-cornerInsetRatio+spacerRatio)*size)).lineTo(Point((cornerInsetRatio-spacerRatio)*size, (1-cornerInsetRatio+spacerRatio)*size)).lineTo(Point((cornerInsetRatio-spacerRatio)*size, (cornerInsetRatio+spacerRatio)*size)).closePath()
docu.append(buildPath( darkBlocks , {'style':'stroke:none;fill:black'}))
darkBlocks = PathData().moveTo(Point( cornerInsetRatio*size, cornerInsetRatio*size)).lineTo( Point( (1-cornerInsetRatio)*size, cornerInsetRatio*size)).lineTo(Point( (1- cornerInsetRatio)*size, (1-cornerInsetRatio)*size)).lineTo(Point( cornerInsetRatio*size, (1-cornerInsetRatio)*size)).closePath()
docu.append(buildPath( darkBlocks , {'style':'stroke:none;fill:black'}))
docu.writeSVG('cornerdbox.svg')
