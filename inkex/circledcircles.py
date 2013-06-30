#!/usr/bin/env python 
"""creates a pattern similar to the Flower of Life (circles on outer edges should be arcs and not full circles)  """
import inkex
from playsvg import element, geom, path


class CircledCircles(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("-c", "--circles",
                        action="store", type="int", 
                        dest="circles", default=20,
                        help="Number of circles ")
        self.OptionParser.add_option("-r", "--radius",
                        action="store", type="float", 
                        dest="radius", default=300.0,
                        help="Radius of circle")
        self.OptionParser.add_option("-s", "--spacing",
                        action="store", type="float", 
                        dest="spacing", default=1.0,
                        help="Spacing ratio")
       
    def buildCircledCircles(self, circles, radius, spacing):
        circleGroup = inkex.etree.Element('g', id='circledcircles')
        
        vertices = geom.createRadialPlots(geom.Point(0,0), radius*spacing/100.0, circles)
        for i in range(circles):
            circleGroup.append(element.buildCircle(vertices[i], radius, {'style':' stroke:black; fill:none' }))
        return circleGroup
        
            
    
    
    def effect(self):
        new = self.buildCircledCircles(self.options.circles, self.options.radius, self.options.spacing)
        self.current_layer.append(new)

           

e = CircledCircles()
e.affect()
