from geom import *
import string
import re
import simplepath
from ctypes import pointer
## Path Abstractions
## These are data structures used to model the path
## This will never support relative command paths, as relative co-ordinates can always be calculated using the geometry library
#FIXME : nix the Smooth Commands objects and convert smooth methods to absolute Commands 
#FIXME: type checking for commands

class PathCommand:
    def __init__(self):
        self.length = 0
    
class MoveCommand(PathCommand):
    def __init__(self, endPt):
        self.endPt = endPt
        PathCommand.__init__(self)
    def __str__(self): return 'M'  + str(self.endPt)

class LineCommand(PathCommand):
    def __init__(self, endPt):
        self.endPt = endPt
        PathCommand.__init__(self)        
    def __str__(self): return 'L'  + str(self.endPt)
        
class CloseCommand(PathCommand):
    def __init__(self):
        PathCommand.__init__(self)
    def __str__(self): return 'Z'

class CubicBezierCommand(PathCommand):
    def __init__(self, ctrlPt1, ctrlPt2, endPt):
        self.ctrlPt1 = ctrlPt1
        self.ctrlPt2 = ctrlPt2
        self.endPt = endPt
        PathCommand.__init__(self)
    def __str__(self): return 'C'  + str(self.ctrlPt1) + ' ' + str(self.ctrlPt2) + ' ' + str(self.endPt)
    

class SmoothCubicBezierCommand(PathCommand):
    def __init__(self, ctrlPt, endPt):
        self.ctrlPt = ctrlPt
        self.endPt = endPt
        PathCommand.__init__(self)
    def __str__(self): return 'S'  + str(self.ctrlPt1) + ' ' + str(self.ctrlPt2) + ' ' + str(self.endPt)


class QuadradicBezierCommand(PathCommand):
    def __init__(self, ctrlPt, endPt):
        self.ctrlPt = ctrlPt
        self.endPt = endPt
        PathCommand.__init__(self)
    def __str__(self): return 'Q'  + str(self.ctrlPt) +  ' ' + str(self.endPt)

class SmoothQuadradicBezierCommand(PathCommand):
    def __init__(self, endPt):
            self.endPt = endPt
            PathCommand.__init__(self)
    def __str__(self): return 'T'  +  ' ' + str(self.endPt)
    
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

    
class PathData:
    '''data structure for storing and manipulating paths'''
    #FIXME: relative co-ordinates support 
    #FIXME: path length (full and per-command)
    def __init__(self, text=''):
        self.commandList = []
        if not text == '': self.dInit(text)
    def dInit(self, text):
        self.initWithSimplePathArray(simplepath.parsePath(text))
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
    def moveTo(self,point):
        command = MoveCommand(point)
        command.length = 0 
        self.commandList.append(command)
        return self
    def closePath(self):
        self.commandList.append(CloseCommand())
        return self
    def lineTo(self, point):
        command = LineCommand(point)
        command.length = distanceBetween(point, getattr(self.commandList[-1], 'endPt'))
        self.commandList.append(command)
        return self
##due to their redundancy and their non-compliance with the last parameters being the ending point, the H and V commands are not supported
    def cubicBezier(self,ctrlPt1,ctrlPt2, endPt):
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
        else:
            print 'error caclulating last ctrlPt'
        return lastCtrlPt
    def QRVBD(self, ctrlDistanceFromBaselineRatio, endPt, flipped=0 ):
        '''draws quadradic bezier using RVBD.  see bezdok.txt for a descpription of Relative Vector-Bezier Definition (RVBD)'''
        lastEnd = getattr(self.commandList[-1], 'endPt')
        distBetweenEnds = distanceBetween(lastEnd, endPt)
        if flipped : bendAngle = 0.25
        else : bendAngle = 0.75
        ctrlPt = extendBendPoint(lastEnd, getMidpoint(lastEnd, endPt), ctrlDistanceFromBaselineRatio*distBetweenEnds, bendAngle )
        self.quadradicBezier(ctrlPt, endPt)
        
        return self
    def SCRVBD(self, vector, endPt):
        '''draws symetric cubic bezier using RVBD.  see bezdok.txt for a descpription of Relative Vector-Bezier Definition (RVBD)'''
        startPt = self.commandList[-1].endPt
        startEndDist = distanceBetween(startPt, endPt)
        ctrlPt1 = extendBendPoint(endPt, startPt, vector[0]*startEndDist, 0.5 - vector[1] )
        ctrlPt2 = extendBendPoint(startPt, endPt, vector[0]*startEndDist, 0.5 + vector[1] )
        self.cubicBezier(ctrlPt1, ctrlPt2, endPt)
        return self
    def CRVBD(self, vector1, vector2, endPt):
        '''draws cubic bezier using RVBD.  see bezdok.txt for a descpription of Relative Vector-Bezier Definition (RVBD)'''
        startPt = self.commandList[-1].endPt
        startEndDist = distanceBetween(startPt, endPt)
        ctrlPt1 = extendBendPoint(endPt, startPt, vector1[0]*startEndDist, 0.5 - vector1[1] )
        ctrlPt2 = extendBendPoint(startPt, endPt, vector2[0]*startEndDist, 0.5 + vector2[1] )
        self.cubicBezier(ctrlPt1, ctrlPt2, endPt)
        return self
    def __str__(self):
       return  string.join([str(i) for i in self.commandList], ' ')
    def __len__(self):
        length = 0
        for i in range(len(commandList)):
            length += getattr(commandList[i], 'length')
        return length
    def appendPath(self, path):
        for command in path.commandList:
            self.commandList.append(command)
    def getNodes(self):
        nodeList = []
        for command in self.commandList:
            if command.__class__.__name__ != 'CloseCommand' :
                nodeList.append(command.endPt)
        return nodeList
    
    def transformPoints(self, fn):
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

    def makeHull(self, points):
        self.moveTo(points[0])
        for i in range(1,len(points)):
            self.lineTo(points[i])
        self.closePath()
        return self
    

