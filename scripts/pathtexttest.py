from playsvg.document import *
from playsvg.element import *
from playsvg.path import *
import playsvg.pathshapes

docu = Document()
aPath = PathData(text = 'M 331.42857,195.21933 C 385.71429,483.79075 200,806.6479 388.57143,480.93361 C 577.14286,155.21933 568.57143,-67.637817 577.14286,160.93361 C 585.71429,389.50504 465.71429,1129.505 282.85714,683.79075 C 100,238.07647 -5.7142857,175.21933 177.14286,135.21933 C 360,95.219325 337.14286,198.07647 331.42857,195.21933 z')
docu.append(buildPath( aPath, {'style':'stroke:black;fill:none'} ))
docu.writeSVG('pathtexttest.svg')

