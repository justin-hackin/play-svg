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
        docu = playsvg.document.Document(document=self.document)
	#using path results in buggyness of display
    ##new = playsvg.element.buildPath(docu, playsvg.pathshapes.metcalfeStar(self.options.points, self.options.radius), {'style':'stroke:black;fill:none'} )
	new = playsvg.compshapes.buildMetcalfeStar(docu, self.options.points, self.options.radius)
        self.document.documentElement.appendChild(new)

e = MetcalfeStar()
e.affect()
