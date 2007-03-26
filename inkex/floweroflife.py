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
import inkex
import playsvg.pathshapes, playsvg.element, playsvg.document, playsvg.compshapes

class FlowerOfLife(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("-r", "--radius",
                        action="store", type="float", 
                        dest="radius", default=30.0,
                        help="Radius of circle")
        self.OptionParser.add_option("-l", "--levels",
                        action="store", type="int", 
                        dest="levels", default=20,
                        help="Number of concentric levels ")
	
	
	
    def effect(self):
        docu = playsvg.document.Document(document=self.document)
	new = playsvg.compshapes.buildFlowerOfLife(docu, self.options.levels, self.options.radius)
	self.document.documentElement.appendChild(new)

e = FlowerOfLife()
e.affect()
