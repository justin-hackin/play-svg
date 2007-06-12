from playsvg.document import *
from playsvg.element import *
from playsvg.path import *
import playsvg.pathshapes
import os
import string


def triangularCorner(boxSize, ratio):
    """creates a triangle with one right angle that would form the bottom left corner of a box
    ocupies percentage ratio of the box sides""" 
    corners = [Point(-1*boxSize, boxSize), Point(boxSize, boxSize), Point(boxSize, -1*boxSize), Point(-1*boxSize, -1*boxSize)]
    cornerPath = PathData()
    cornerPath.moveTo(corners[0])
    cornerPath.lineTo(getLineDivision(corners[0], corners[1], ratio))
    cornerPath.lineTo(getLineDivision(corners[0], corners[3], ratio))
    cornerPath.closePath()
    return cornerPath

def middleStripe(boxSize, ratio):
    corners = [Point(-1*boxSize, boxSize), Point(boxSize, boxSize), Point(boxSize, -1*boxSize), Point(-1*boxSize, -1*boxSize)]
    stripesPath = PathData()
    stripesPath.moveTo(getLineDivision(corners[1], corners[0], ratio))
    stripesPath.lineTo(corners[1])
    stripesPath.lineTo(getLineDivision(corners[1], corners[2],ratio ))
    stripesPath.lineTo(getLineDivision(corners[3], corners[2],ratio ))
    stripesPath.lineTo(corners[3])
    stripesPath.lineTo(getLineDivision(corners[3], corners[0], ratio))
    stripesPath.closePath()
    return stripesPath
    

def buildAngledStripes(docu, boxSize, numStripes, corneredFlag):
    """builds a box containing stripes on a 45 degree angle that move from bottom left to top right
        numStripes is always odd, if an even number is given, numStripes is incremented by one
        a stripe is centred on the line from bottom left corner to top right corner
        if corneredFlag is true, top left and bottom right corners will contain a triangular stripe
    """
    corners = [Point(-1*boxSize, boxSize), Point(boxSize, boxSize), Point(boxSize, -1*boxSize), Point(-1*boxSize, -1*boxSize)]
    #only works for odd numStripes, if even, add one more stripe
    if numStripes%2 == 0: numStripes +=1
    
    stripesGroup = docu.makeGroup()
    
    #represents what portion of box side a stripe will ocupy
    stripeSizeRatio = 0
    
    stripesPath = PathData()
    stripesAttrs = {'style':'fill:black;stroke:none'}
        
    #odd number of stripes, stripe through middle
    if numStripes%2==1 :
        stripeSizeRatio = 1/(0.5+2*math.floor(float(numStripes)/2))
        
        if numStripes > 1:
            #add corner stripes
            stripesPath = PathData()
            stripesPath.moveTo(corners[0])
            stripesPath.lineTo(getLineDivision(corners[0], corners[1], stripeSizeRatio))
            stripesPath.lineTo(getLineDivision(corners[0], corners[3], stripeSizeRatio))
            stripesPath.closePath()
            stripesGroup.appendChild(buildPath(docu, stripesPath, stripesAttrs))
            
            stripesPath = PathData()
            stripesPath.moveTo(corners[2])
            stripesPath.lineTo(getLineDivision(corners[2], corners[3], stripeSizeRatio))
            stripesPath.lineTo(getLineDivision(corners[2], corners[1], stripeSizeRatio))
            stripesPath.closePath()
            stripesGroup.appendChild(buildPath(docu, stripesPath, stripesAttrs))
            
            #add middle stripe
            stripesPath = PathData()
            stripesPath.moveTo(getLineDivision(corners[1], corners[0], 0.5*stripeSizeRatio))
            stripesPath.lineTo(corners[1])
            stripesPath.lineTo(getLineDivision(corners[1], corners[2],0.5*stripeSizeRatio ))
            stripesPath.lineTo(getLineDivision(corners[3], corners[2],0.5*stripeSizeRatio ))
            stripesPath.lineTo(corners[3])
            stripesPath.lineTo(getLineDivision(corners[3], corners[0], 0.5*stripeSizeRatio))
            stripesPath.closePath()
            stripesGroup.appendChild(buildPath(docu, stripesPath, stripesAttrs))
               
                
            if numStripes > 3:
                for i in range((numStripes -3)/2):
                    stripesPath = PathData()
                    stripesPath.moveTo(getLineDivision(corners[0], corners[1], (1+i)*2*stripeSizeRatio))
                    stripesPath.lineTo(getLineDivision(corners[0], corners[1],((1+i)*2+1)*stripeSizeRatio ))
                    stripesPath.lineTo(getLineDivision(corners[0], corners[3],((1+i)*2+1)*stripeSizeRatio ))
                    stripesPath.lineTo(getLineDivision(corners[0], corners[3], (1+i)*2*stripeSizeRatio))
                    stripesPath.closePath()
                    stripesGroup.appendChild(buildPath(docu, stripesPath, stripesAttrs))
                    
                    stripesPath = PathData()
                    stripesPath.moveTo(getLineDivision(corners[2], corners[1], (1+i)*2*stripeSizeRatio))
                    stripesPath.lineTo(getLineDivision(corners[2], corners[1],((1+i)*2+1)*stripeSizeRatio ))
                    stripesPath.lineTo(getLineDivision(corners[2], corners[3],((1+i)*2+1)*stripeSizeRatio ))
                    stripesPath.lineTo(getLineDivision(corners[2], corners[3], (1+i)*2*stripeSizeRatio))
                    stripesPath.closePath()
                    stripesGroup.appendChild(buildPath(docu, stripesPath, stripesAttrs))
                    
        
    return stripesGroup



docu = document.Document()
docu.appendElement( buildWeaveTile(docu,100, 0.5 ))

docu.writeSVG("weave_tile.svg" )
print "done"

