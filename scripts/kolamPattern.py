from playsvg.document import *
from playsvg.element import *
from playsvg.path import *
import playsvg.pathshapes

def buildDiagonalConnected(boxSize, ctrlDistRatio):
    tileGroup = docu.makeGroup()
    corners = [Point(-1*boxSize, boxSize), Point(boxSize, boxSize), Point(boxSize, -1*boxSize), Point(-1*boxSize, -1*boxSize)]
    containerBox = PathData().makeHull(corners)
    tileGroup.appendChild(buildPath(docu, containerBox, {'style':'fill:none;stroke:none'}))
    kolamLine = PathData().moveTo(corners[0]).\
    cubicBezier(getLineDivision(corners[0], corners[1], ctrlDistRatio),getLineDivision(corners[2], corners[1], ctrlDistRatio),corners[2]).\
    cubicBezier(getLineDivision(corners[2], corners[3], ctrlDistRatio),getLineDivision(corners[0], corners[3], ctrlDistRatio),corners[0]).closePath()
    tileGroup.appendChild(buildPath(docu, kolamLine, {'style':'fill:none;stroke:black'}))
    return tileGroup
    
def buildAdjacentConnected(boxSize, ctrlDistRatio):
    tileGroup = docu.makeGroup()
    corners = [Point(-1*boxSize, boxSize), Point(boxSize, boxSize), Point(boxSize, -1*boxSize), Point(-1*boxSize, -1*boxSize)]
    containerBox = PathData().makeHull(corners)
    tileGroup.appendChild(buildPath(docu, containerBox, {'style':'fill:none;stroke:none'}))
    kolamLine = PathData().moveTo(corners[0]).lineTo(corners[1]).\
    cubicBezier(getLineDivision(corners[1], corners[2], ctrlDistRatio),getLineDivision(corners[0], corners[3], ctrlDistRatio),corners[0]).closePath()
    tileGroup.appendChild(buildPath(docu, kolamLine, {'style':'fill:none;stroke:black'}))
    return tileGroup
       
def buildSingleConnected(boxSize, ctrlDistRatio):
    tileGroup = docu.makeGroup()
    corners = [Point(-1*boxSize, boxSize), Point(boxSize, boxSize), Point(boxSize, -1*boxSize), Point(-1*boxSize, -1*boxSize)]
    containerBox = PathData().makeHull(corners)
    tileGroup.appendChild(buildPath(docu, containerBox, {'style':'fill:none;stroke:none'}))
    kolamLine = PathData().moveTo(corners[0]).\
    cubicBezier(getLineDivision(corners[0], corners[1], ctrlDistRatio),getLineDivision(corners[0], corners[3], ctrlDistRatio),corners[0]).closePath()
    tileGroup.appendChild(buildPath(docu, kolamLine, {'style':'fill:none;stroke:black'}))
    return tileGroup
    
def buildAllButOneConnected(boxSize, ctrlDistRatio):
    tileGroup = docu.makeGroup()
    corners = [Point(-1*boxSize, boxSize), Point(boxSize, boxSize), Point(boxSize, -1*boxSize), Point(-1*boxSize, -1*boxSize)]
    containerBox = PathData().makeHull(corners)
    tileGroup.appendChild(buildPath(docu, containerBox, {'style':'fill:none;stroke:none'}))
    kolamLine = PathData().moveTo(corners[0]).lineTo(corners[1]).lineTo(corners[2]).\
    cubicBezier(getLineDivision(corners[2], corners[3], ctrlDistRatio),getLineDivision(corners[0], corners[3], ctrlDistRatio),corners[0]).closePath()
    tileGroup.appendChild(buildPath(docu, kolamLine, {'style':'fill:none;stroke:black'}))
    return tileGroup
    
    
def buildAllConnected(boxSize, ctrlDistRatio):
    tileGroup = docu.makeGroup()
    corners = [Point(-1*boxSize, boxSize), Point(boxSize, boxSize), Point(boxSize, -1*boxSize), Point(-1*boxSize, -1*boxSize)]
    containerBox = PathData().makeHull(corners)
    tileGroup.appendChild(buildPath(docu, containerBox, {'style':'fill:none;stroke:none'}))
    kolamLine = PathData().makeHull(corners)
    tileGroup.appendChild(buildPath(docu, kolamLine, {'style':'fill:none;stroke:black'}))
    return tileGroup

boxSize = 25
ratio = 0.75
docu = Document()
docu.appendElement(buildAllConnected(boxSize,ratio))
docu.appendElement(buildSingleConnected(boxSize,2))
docu.appendElement(buildAdjacentConnected(boxSize,ratio))
docu.appendElement(buildDiagonalConnected(boxSize,ratio))
docu.appendElement(buildAllButOneConnected(boxSize,ratio))

docu.writeSVG('kolam_tile.svg')

#now tiles must be rotated 45 degrees and duplicated for various alignments

