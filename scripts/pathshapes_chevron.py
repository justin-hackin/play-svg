from playsvg.document import *
from playsvg.element import *
from playsvg.path import *
from playsvg import pathshapes

startPoint = Point(0, -640)
thickness = 15
width = 300
angle = 33

docu = Document()
for i in range(0,20):
    thisChevron = pathshapes.chevron(startPoint+Point(0, i*3*thickness), thickness, width, (60-i)/360.00)
    docu.append(buildPath(thisChevron, {'style':'stroke:none;fill:black;'}))
   
docu.writeSVG('pathshapes_chevron.svg')
print