#!/usr/bin/env python 
"""creates a series of vertically-stacked boxes with a fill color changing incrementally from one color to another"""
import inkex
import math

from playsvg import element, geom, color, path


class DiscreteColorGrad(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("-p", "--sides",
                        action="store", type="int", 
                        dest="sides", default=6,
                        help="Number of colors in palette")
        self.OptionParser.add_option("-r", "--radius",
                        action="store", type="float", 
                        dest="radius", default=100,
                        help="Radius")
        self.OptionParser.add_option("-s", "--startcolor",
                        action="store", type="string", 
                        dest="startcolor", default="#ff0000",
                        help="Starting color")
        self.OptionParser.add_option("-e", "--endcolor",
                        action="store", type="string", 
                        dest="endcolor", default="#0000ff",
                        help="Ending color")
        self.OptionParser.add_option("-d", "--divisions",
                        action="store", type="int", 
                        dest="divisions", default=16,
                        help="Divisions")
        self.OptionParser.add_option("-t", "--sideturn",
                        action="store", type="int", 
                        dest="sideturn", default=2,
                        help="Side turnings")
        
    
    def polygonGradientIris(self, position,sides, radius,  startColor, endColor, divisionOfPieRotation,  sideTurnings, reverse=0, passiveopt=0):
        
        gradientIrisGroup = inkex.etree.Element("g")
        #calculate creepRatio from rotationAngle,
        #where rotationAngle is the angle each polygon is rotated
        #and creepRatio is the percentage of the polygon side to move from one corner to the other
        rotations = divisionOfPieRotation*sideTurnings/2
        colorGradation = color.tupleGradient(color.hexToRGB(startColor), color.hexToRGB(endColor),rotations )
        
        pieCornerAngle = 1.0/sides*math.pi*2
        rotationAngle = 1.0/divisionOfPieRotation*pieCornerAngle
        
        polygonCornerAngle =  (sides-2)*math.pi/(2*sides)
        adjacentAngle = math.pi - rotationAngle - polygonCornerAngle
        
        adjacentSide = math.sin(rotationAngle)/math.sin(adjacentAngle)*radius
        innerSide = math.sin(rotationAngle)*radius/math.sin(adjacentAngle)
        outerSegmentLength = math.sin(pieCornerAngle)*radius/math.sin(polygonCornerAngle)
        creepRatio = innerSide/outerSegmentLength
        if reverse : creepRatio = 1 - creepRatio
        
        
        linePoints = geom.createRadialPlots(position, radius, sides, passive=passiveopt )
        
        for i in range(rotations+1):
            polygonAttributes = {u'style':u'stroke:black;stroke-width:1;fill:' + unicode(colorGradation[i])}
            trianglePath = path.PathData().moveTo(linePoints[0])
            for j in range(1,sides):
                trianglePath.lineTo(linePoints[j])
            trianglePath.closePath()
            gradientIrisGroup.append(element.buildPath( trianglePath, polygonAttributes))
            newLinePoints = []
            for j in range(sides):
                newLinePoints.append(geom.getLineDivision(linePoints[j], linePoints[(j+1)%sides], creepRatio))
            linePoints = newLinePoints
        return gradientIrisGroup
    

    def effect(self):
        
        new = self.polygonGradientIris(geom.Point(0,0), self.options.sides, self.options.radius, self.options.startcolor, self.options.endcolor, self.options.divisions, self.options.sideturn)
        self.current_layer.append(new)

e = DiscreteColorGrad()
e.affect()
