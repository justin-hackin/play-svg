#!/usr/bin/env python 
"""creates a series of interlocking hexagons that roughly form a hexagon shape"""

import inkex
import playsvg.pathshapes, playsvg.element, playsvg.document, playsvg.compshapes

class HexagonLattice(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("-r", "--radius",
                        action="store", type="float", 
                        dest="radius", default=300.0,
                        help="Radius of hexagon")
        self.OptionParser.add_option("-l", "--levels",
                        action="store", type="int", 
                        dest="levels", default=20,
                        help="Number of concentric layers in lattice")
	
	
	
    def effect(self):
        docu = playsvg.document.Document(document=self.document)
	new = playsvg.compshapes.buildHexagonLattice(docu, self.options.levels, self.options.radius)
	self.document.documentElement.appendChild(new)

e = HexagonLattice()
e.affect()
