#!/usr/bin/env python 
"""creates a series of radiating quadrilaterals, see example in scripts/images/"""

import inkex, simplestyle, pturtle, random
import playsvg.pathshapes, playsvg.element, playsvg.document, playsvg.path

class RayBlocks(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("-r", "--numrays",
                        action="store", type="int", 
                        dest="numrays", default=8,
                        help="Number of rays in generation")
        self.OptionParser.add_option("-i", "--innerradius",
                        action="store", type="float", 
                        dest="innerradius", default=100.0,
                        help="radius of inner edge")
	self.OptionParser.add_option("-o", "--outerradius",
                        action="store", type="float", 
                        dest="outerradius", default=100.0,
                        help="radius of outer edge")
        self.OptionParser.add_option("-j", "--innerspacing",
                        action="store", type="float", 
                        dest="innerspacing", default=0.7,
                        help="percent of wedge that the inner ray edge ocupies")
	self.OptionParser.add_option("-p", "--outerspacing",
                        action="store", type="float", 
                        dest="outerspacing", default=0.7,
                        help="percent of wedge that the outer ray edge ocupies")
	self.OptionParser.add_option("-c", "--rounded",
                        action="store", type="inkbool", 
                        dest="rounded", default=True,
                        help="makes inner and outer edges rounded")
	self.OptionParser.add_option("-d", "--roundinglength",
                        action="store", type="float", 
                        dest="roundinglength", default=2.0,
                        help="how far out the rounded edges go")

	
	
    def effect(self):
        docu = playsvg.document.Document(document=self.document)
	new = playsvg.element.buildPath(docu, playsvg.pathshapes.rayBlocks(self.options.numrays, self.options.innerradius, self.options.outerradius, self.options.innerspacing,  self.options.outerspacing, self.options.rounded, self.options.roundinglength), {'style':'stroke:black;fill:none'})
	
        self.document.documentElement.appendChild(new)

e = RayBlocks()
e.affect()
