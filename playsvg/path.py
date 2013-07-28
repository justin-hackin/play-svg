"""
This module contains the PathData class which is used to store and manipulate paths as defined in the SVG specifications.  
Methods correspond to SVG path's D attribute commands as specified `here <http://www.w3.org/TR/SVG/paths.html#PathData>`_
PathData has only one attribute, commandList, which stores a list of objects representing commands.

playSVG is transitionally implementing the use of sympy.geometry.Point instead of the geom.Point for greater geometric functionality, with following replacements
str(point) => printPoint(point)
str(pathData) => pathData.getD()
"""

from geom import *
import string
import re
import simplepath
from copy import deepcopy

## Path Abstractions
## These are data structures used to model the path
## This will never support relative command paths, as relative co-ordinates can always be calculated using the geometry library
#FIXME : nix the Smooth Commands objects and convert smooth methods to absolute Commands 
#FIXME: type checking for commands


class PathData:
    """Data structure for storing and manipulating paths.   """
    #FIXME: relative co-ordinates support 
    #FIXME: path length (full and per-command)
    def __init__(self, text=''):
        self.commandList = []
        if not text == '': self.dInit(text)
    def dInit(self, text):
        """initialize the object with the code from an svg d attribute text """
        self.initWithSimplePathArray(simplepath.parsePath(text))
        return self
    def initWithSimplePathArray(self, pathArray):
        for command, params in pathArray:
            if command == 'L':
                self.lineTo(Point(params[0], params[1]))
            elif command == 'M':
                self.moveTo(Point(params[0], params[1]))
            elif command == 'Q':
                self.quadradicBezier(Point(params[0], params[1]), Point(params[2], params[3]))
            elif command == 'C':
                self.cubicBezier(Point(params[0], params[1]), Point(params[2], params[3]), Point(params[4], params[5]))
            elif command == 'A':
                self.elipticalArc(Point(params[0], params[1]), Point(params[5], params[6]), params[2], params[3], params[4])
            elif command == 'Z':
                self.closePath()
    
    def __str__(self):
       return  string.join([str(i) for i in self.commandList], ' ')
    def getD(self):
       return  string.join([i.toString() for i in self.commandList], ' ') 
    
    
    def __len__(self):
        length = 0
        for i in range(len(commandList)):
            length += getattr(commandList[i], 'length')
        return length
    
    def moveTo(self,point):
        """always the first command of the path.  repositions drawing location to point"""
        command = MoveCommand(point)
        command.length = 0 
        self.commandList.append(command)
        return self
    def closePath(self):
        """draws a line from the current point to the last move point"""
        self.commandList.append(CloseCommand())
        return self
    def lineTo(self, point):
        """draws a line from the current point to point"""
        command = LineCommand(point)
        command.length = distanceBetween(point, getattr(self.commandList[-1], 'endPt'))
        self.commandList.append(command)
        return self
##due to their redundancy and their non-compliance with the last parameters being the ending point, the H and V commands are not supported
    def cubicBezier(self,ctrlPt1,ctrlPt2, endPt):
        """draws a cubic bezier from the current point to endPt with ctrlPt1, ctrlPt2"""
        #FIXME bugs when multiple endpts
        command = CubicBezierCommand(ctrlPt1, ctrlPt2, endPt)
        command.length = cubicBezierLength(getattr(self.commandList[-1], 'endPt'), ctrlPt1, ctrlPt2, endPt)
        self.commandList.append(command)
        return self
##    def smoothCubicBezier(self, ctrlPt, endPt):
##        command = SmoothCubicBezierCommand(ctrlPt, endPt)
##        previousLastCtrl = self.lastCtrlPtForCommand(-2)
##        projectedCtrlPt = extendBendPoint(previousLastCtrl, getattr(self.commandList[-1], 'endPt'), distanceBetweenPoints(previousLastCtrl, getattr(self.commandList[index-1], 'endPt')), 0)
##        command.length =  cubicBezierLength(projectedCtrlPt, ctrlPt, endPt)
##        self.commandList.append(command)
##        return self
    def quadradicBezier(self, ctrlPt, endPt):
        """draws a quadradic bezier from the current point to endPt with ctrlPt1"""
        command = QuadradicBezierCommand(ctrlPt, endPt)
        command.length = quadradicBezierLength(getattr(self.commandList[-1], 'endPt'), ctrlPt, endPt)
        self.commandList.append(command)
        return self
##    def smoothQuadradicBezier(self, endpt):
##        command = SmoothCubicBezierCommand(endPt)
##        previousLastCtrl = self.lastCtrlPtForCommand(-2)
##        projectedCtrlPt = extendBendPoint(previousLastCtrl, getattr(self.commandList[-1], 'endPt'), distanceBetweenPoints(previousLastCtrl, getattr(self.commandList[index-1], 'endPt')), 0)
##        command.length =  cubicBezierLength(projectedCtrlPt, endPt)
##        return self 
    def elipticalArc(self, rPoint, endPt, xAxisRotation=0, largeArcFlag=0, sweepFlag=0, relative=0):
        """draws an eliptical arc"""
        self.commandList.append(ArcCommand(rPoint,xAxisRotation, largeArcFlag, sweepFlag, endPt))
        return self
    def lastCtrlPtForCommand(self, index):
        """allows one to find out the projected control point of a previous bezier even if there was one or more smooth bezier curves (in which case the ctrl point is not explicitly stated)"""
        lastCtrlPt = null
        if self.commandList[index].__class__.__name__ == "SmoothCubicBezierCommand" or \
        self.commandList[index].__class__.__name__ == "QuadradicBezierCommand":
            lastCtrlPt = getattr(self.commandList[index], 'ctrlPt')
        elif self.commandList[index].__class__.__name__ == "CubicBezierCommand":
            lastCtrlPt = getattr(self.commandList[index], 'ctrlPt2')
        elif self.commandList[index-1].__class__.__name__ == "SmoothQuadradicBezierCommand":
            previousLastCtrl = self.lastCtrlPtForCommand(index-1)
            lastCtrlPt = extendBendPoint(previousLastCtrl, getattr(self.commandList[index-1], 'endPt'), distanceBetweenPoints(previousLastCtrl, getattr(self.commandList[index-1], 'endPt')), 0)
        #***else:
            #***print 'error caclulating last ctrlPt'
        return lastCtrlPt
    def QRVBD(self, ctrlDistanceFromBaselineRatio, endPt, flipped=0 ):
        """Draws quadradic bezier using relative definitions.  Example in pathshpes.arcSpire """
        lastEnd = getattr(self.commandList[-1], 'endPt')
        distBetweenEnds = distanceBetween(lastEnd, endPt)
        if flipped : bendAngle = 0.25
        else : bendAngle = 0.75
        ctrlPt = extendBendPoint(lastEnd, getMidpoint(lastEnd, endPt), ctrlDistanceFromBaselineRatio*distBetweenEnds, bendAngle )
        self.quadradicBezier(ctrlPt, endPt)
        
        return self
    def SCRVBD(self, vector, endPt):
        """Draws symetric cubic bezier using relative terms.  See scripts/circularWeave.py for example use."""
        startPt = self.commandList[-1].endPt
        startEndDist = distanceBetween(startPt, endPt)
        ctrlPt1 = extendBendPoint(endPt, startPt, vector[0]*startEndDist, 0.5 - vector[1] )
        ctrlPt2 = extendBendPoint(startPt, endPt, vector[0]*startEndDist, 0.5 + vector[1] )
        self.cubicBezier(ctrlPt1, ctrlPt2, endPt)
        return self
    def CRVBD(self, vector1, vector2, endPt):
        """'Draws symetric cubic bezier using relative terms """
        startPt = self.commandList[-1].endPt
        startEndDist = distanceBetween(startPt, endPt)
        ctrlPt1 = extendBendPoint(endPt, startPt, vector1[0]*startEndDist, 0.5 - vector1[1] )
        ctrlPt2 = extendBendPoint(startPt, endPt, vector2[0]*startEndDist, 0.5 + vector2[1] )
        self.cubicBezier(ctrlPt1, ctrlPt2, endPt)
        return self
    
    def appendPath(self, path):
        """Concatenate commands from another PathData object into command list"""
        for command in path.commandList:
            self.commandList.append(command)
    def getNodes(self):
        """return an array of all points in path"""
        nodeList = []
        for command in self.commandList:
            if command.__class__.__name__ != 'CloseCommand' :
                nodeList.append(command.endPt)
        return nodeList
    
    def transformPoints(self, fn):
        """alter all points in path using a lambda function.  See inkex/radialtile.py or inkex/fitinabox.py for examples of use."""
        pointsList = []
        for command in self.commandList:
            if command.__class__.__name__ != 'CloseCommand'  :
                if command.__class__.__name__ == 'MoveCommand' or   command.__class__.__name__ == 'LineCommand'  :
                    command.endPt = fn(command.endPt)
                elif command.__class__.__name__ == 'QuadradicBezierCommand' :
                    command.endPt = fn(command.endPt)
                    command.ctrlPt = fn(command.ctrlPt)
                elif command.__class__.__name__ == 'CubicBezierCommand' :
                    command.ctrlPt1 = fn(command.ctrlPt1)
                    command.ctrlPt2 = fn(command.ctrlPt2)
                    command.endPt = fn(command.endPt)
                    
    def calculateCloseEndPts(self):
        closeIndices = []
        for i in range(len(self.commandList)):
            thisCommand = self.commandList[i]
            if thisCommand.__class__.__name__ == 'CloseCommand': closeIndices.append(i)
        
        for closeInd in closeIndices:
            searchInd = closeInd-1
            while (self.commandList[searchInd].__class__.__name__ != 'MoveCommand' ):
                searchInd -= 1
            self.commandList[closeInd].endPt = self.commandList[searchInd].endPt
    
    def replaceCloseWithLine(self): 
        """replaces all close commands with lineTo command"""
        self.calculateCloseEndPts()
        for i in range(len(self.commandList)):
            thisCommand = self.commandList[i]
            if thisCommand.__class__.__name__ == 'CloseCommand': 
                self.commandList[i] = LineCommand(thisCommand.endPt)
                
 
    def reversePath(self):
        """replaces all close commands with lineTo and reverses direction of path""" 
        self.replaceCloseWithLine() #hackish solution to reversing with z commands
        newCommandList = []
              
        noCommands = len(self.commandList)
        
        newCommandList.append(MoveCommand(self.commandList[noCommands-1].endPt))
        for i in range(noCommands-1,0 ,-1 ):
            thisCommand = deepcopy(self.commandList[i])
            thisEnd = self.commandList[i-1].endPt
            thisCommand.endPt = thisEnd
            thisCommandType = thisCommand.__class__.__name__
            if (thisCommandType == "CubicBezierCommand"):
                thisCtrlPt1 = thisCommand.ctrlPt1
                thisCommand.ctrlPt1 =  thisCommand.ctrlPt2
                thisCommand.ctrlPt2 = thisCtrlPt1
            newCommandList.append(thisCommand)
        self.commandList = newCommandList
        
    def up(self, val):
        """Turtle-like command to draw line up specified distance from last command endPt"""
        point = self.commandList[-1].endPt + Point(0, val) 
        command = LineCommand(point)
        command.length = distanceBetween(point, getattr(self.commandList[-1], 'endPt'))
        self.commandList.append(command)
        return self
    
    def down(self, val):
        """Turtle-like command to draw line down specified distance from last command endPt"""
        point = self.commandList[-1].endPt + Point(0, -1*val) 
        command = LineCommand(point)
        command.length = distanceBetween(point, getattr(self.commandList[-1], 'endPt'))
        self.commandList.append(command)
        return self
    
    def left(self, val):
        """Turtle-like command to draw line down specified distance from last command endPt"""
        point = self.commandList[-1].endPt + Point(-1*val, 0) 
        command = LineCommand(point)
        command.length = distanceBetween(point, getattr(self.commandList[-1], 'endPt'))
        self.commandList.append(command)
        return self
    
    def right(self, val):
        """Turtle-like command to draw line down specified distance from last command endPt"""
        point = self.commandList[-1].endPt + Point(val, 0) 
        command = LineCommand(point)
        command.length = distanceBetween(point, getattr(self.commandList[-1], 'endPt'))
        self.commandList.append(command)
        return self
    
    
    
    
    
        
        
#TODO: preserve close path on reverse        
#        closeIndices = []
#        for i in range(len(self.commandList)):
#            if thisCommand.__class__.__name__ == 'CloseCommand': closeIndices.append(i)
#        
#        #swap CloseCommand with first command after close but before MoveCommand or end of list    
#        for closeInd in closeIndices:
#            swapInd = len(self.commandList)-1
#            searchInd = closeInd + 1
#            while (searchInd != len(self.commandList)-1 ):
#                if self.commandList[searchInd+1].__class__.__name__ == 'MoveCommand': 
#                    swapInd = searchInd - 1
#                    break
#                searchInd += 1
#            #swap end Points of  closeInd and swap index
#            closeEnd = self.commandList[closeInd].endPt
#            swapEnd = self.commandList[swapInd].endPt
#            self.commandList[closeInd].endPt = swapEnd
#            self.commandList[swapInd].endPt = closeEnd
#            
#            #swap positions of closeInd and swap index
#            self.commandList[closeInd], self.commandList[swapInd] = self.commandList[swapInd], self.commandList[closeInd]
      
        return self 
        
    def backAndForth(self, overlaps):
        """makes a path overlap itself in a back and forth motion a certain number of times"""
        self.replaceCloseWithLine()
        originalPath = deepcopy(self)
        reversedPath = deepcopy(self).reversePath()
        for i in range(2,overlaps+1):
            if (i%2 == 0): self.commandList.extend(reversedPath.commandList[1:])
            else : self.commandList.extend(originalPath.commandList[1:])
          
        
        
                 
    def makeHull(self, points):
        """creates a series of lines between successive elements points, closing at the end""" 
        self.moveTo(points[0])
        for i in range(1,len(points)):
            self.lineTo(points[i])
        self.closePath()
        return self
    
    
class PathCommand:
    def __init__(self):
        self.length = 0
    
class MoveCommand(PathCommand):
    def __init__(self, endPt):
        self.endPt = endPt
        PathCommand.__init__(self)
    def __str__(self): return 'M'  + str(self.endPt)
    def toString(self): return 'M '  + printPoint(self.endPt)

class LineCommand(PathCommand):
    def __init__(self, endPt):
        self.endPt = endPt
        PathCommand.__init__(self)        
    def __str__(self): return 'L'  + str(self.endPt)
    def toString(self): return 'L'  + printPoint(self.endPt)
        
class CloseCommand(PathCommand):
    def __init__(self):
        self.endPt = None
        PathCommand.__init__(self)
    def __str__(self): return 'Z'
    def toString(self): return 'Z' 

class CubicBezierCommand(PathCommand):
    def __init__(self, ctrlPt1, ctrlPt2, endPt):
        self.ctrlPt1 = ctrlPt1
        self.ctrlPt2 = ctrlPt2
        self.endPt = endPt
        PathCommand.__init__(self)
    def __str__(self): return 'C'  + str(self.ctrlPt1) + ' ' + str(self.ctrlPt2) + ' ' + str(self.endPt)
    def toString(self): return 'C'  + printPoint(self.ctrlPt1) + ' ' + printPoint(self.ctrlPt2) + ' ' + printPoint(self.endPt)
     

class SmoothCubicBezierCommand(PathCommand):
    def __init__(self, ctrlPt, endPt):
        self.ctrlPt = ctrlPt
        self.endPt = endPt
        PathCommand.__init__(self)
    def __str__(self): return 'S'  + str(self.ctrlPt1) + ' ' + str(self.ctrlPt2) + ' ' + str(self.endPt)
    def toString(self): return 'S'  + printPoint(self.ctrlPt1) + ' ' + printPoint(self.ctrlPt2) + ' ' + printPoint(self.endPt)


class QuadradicBezierCommand(PathCommand):
    def __init__(self, ctrlPt, endPt):
        self.ctrlPt = ctrlPt
        self.endPt = endPt
        PathCommand.__init__(self)
    def __str__(self): return 'Q'  + str(self.ctrlPt) +  ' ' + str(self.endPt)
    def toString(self): return 'Q'  + printPoint(self.ctrlPt) +  ' ' + printPoint(self.endPt)

class SmoothQuadradicBezierCommand(PathCommand):
    def __init__(self, endPt):
            self.endPt = endPt
            PathCommand.__init__(self)
    def __str__(self): return 'T'  +  ' ' + str(self.endPt)
    def toString(self): return 'T'  +  ' ' + printPoint(self.endPt)
    
class ArcCommand(PathCommand):
    def __init__(self, rPoint, xAxisRotation, sweepFlag, arcFlag, endPt):
        self.rPoint = rPoint
        self.xAxisRotation = xAxisRotation
        self.sweepFlag = sweepFlag
        self.arcFlag = arcFlag
        self.endPt = endPt
        PathCommand.__init__(self)
    def __str__(self): 
        return ' A' +  ' '+ str(getattr(self.rPoint, 'x')) +' '+ str(getattr(self.rPoint, 'y')) +' '+ str(self.sweepFlag) +' '+ str(self.arcFlag) +' '+ str(self.endPt)
    
    def toString(self): 
        return ' A' +  ' '+ printPoint(self.rPoint) + ' '+ str(self.sweepFlag) +','+ str(self.arcFlag) +' '+ printPoint(self.endPt)


def printPoint(point):
    return '%.5f'% float(point.x) + ' , ' + '%.5f'% float(point.y)






