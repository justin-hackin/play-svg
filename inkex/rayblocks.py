#!/usr/bin/env python 
'''
Copyright (C) 2007 Justin Barca, justinbarca@gmail.com

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
'''
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
                        action="store", type="int", 
                        dest="rounded", default=1,
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
