#!/usr/bin/env python 
"""representation of a fully connected graph with nodes equally-spaced along a circle"""

import inkex
import playsvg.pathshapes, playsvg.compshapes, playsvg.element, playsvg.document

class MetcalfeStar(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("-r", "--radius",
                        action="store", type="float", 
                        dest="radius", default=300.0,
                        help="Radius of Metcalfe star")
        self.OptionParser.add_option("-p", "--points",
                        action="store", type="int", 
                        dest="points", default=20,
                        help="Number of points in star")
	
	
	
    def effect(self):
        
	#using path results in buggyness of display
    ##new = playsvg.element.buildPath(docu, playsvg.pathshapes.metcalfeStar(self.options.points, self.options.radius), {'style':'stroke:black;fill:none'} )
        new = playsvg.compshapes.buildMetcalfeStar(self.options.points, self.options.radius)
        self.current_layer.append(new)

e = MetcalfeStar()
e.affect()
