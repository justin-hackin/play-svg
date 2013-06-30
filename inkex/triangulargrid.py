#!/usr/bin/env python 
'''creates a triangular grid bounded by a large triangle'''
import inkex
import playsvg.pathshapes, playsvg.element, playsvg.document, playsvg.compshapes

class TriangularGrid(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("-l", "--levels",
                        action="store", type="int", 
                        dest="levels", default=6,
                        help="Amount of levels tall the grid is")
        self.OptionParser.add_option("-s", "--sidelength",
                        action="store", type="float", 
                        dest="sidelength", default=20,
                        help="Length of side of 1 triangle")

    def effect(self):
        new = playsvg.compshapes.buildTriangularGrid( self.options.levels, self.options.sidelength)
        self.current_layer.append(new)

e = TriangularGrid()
e.affect()
