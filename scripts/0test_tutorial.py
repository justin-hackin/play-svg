"""outline for Image of a crop circle design found at T+0:49 in http://video.google.ca/videoplay?docid=2560466181031386448&q=sacred+geometry&total=308&start=0&num=10&so=0&type=search&plindex=9 """
from playsvg.geom import *
from playsvg.document import *
from playsvg.element import *
from playsvg.path import *

pointA = Point() # a point at (0,0)
pointB = Point(10,10)
print "Position of pointA:" + str(pointA)
print "Position of pointB:" + str(pointB) 
pointC = pointB + Point(12,7)
pointD = pointC - Point(7,12)
pointE = pointD.scale(10) 
print "Position of pointC:" + str(pointC)
print "Position of pointD:" + str(pointD)
print "Position of pointE:" + str(pointE)
docu = Document()
firstLine = buildLine(pointA, pointB)
print "Contents of firstLine: " + str(firstLine)
docu.append(firstLine)
print str(docu)
docu.writeSVG("hello.svg")

