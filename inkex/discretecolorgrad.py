#!/usr/bin/env python 
'''
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

class DiscreteColorGrad(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("-i", "--intervals",
                        action="store", type="int", 
                        dest="intervals", default=10,
                        help="Number of colors in palette")
        self.OptionParser.add_option("-s", "--startcolor",
                        action="store", type="string", 
                        dest="startcolor", default="#ff0000",
                        help="Starting color")
        self.OptionParser.add_option("-e", "--endcolor",
                        action="store", type="string", 
                        dest="endcolor", default="#0000ff",
                        help="Ending color")
        self.OptionParser.add_option("-z", "--size",
                        action="store", type="int", 
                        dest="size", default=300,
                        help="Palette size")


    def effect(self):
        docu = playsvg.document.Document(document=self.document)
	new = playsvg.compshapes.buildDiscreteColorGrad(docu, self.options.intervals, self.options.startcolor, self.options.endcolor, self.options.size)
	self.document.documentElement.appendChild(new)

e = DiscreteColorGrad()
e.affect()
