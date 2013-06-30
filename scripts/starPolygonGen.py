from playsvg.document import *
from playsvg.element import *
from playsvg.path import *
from playsvg import pathshapes
import os
import string

starDictionary = generateStarDict(88)
if not os.path.exists("images/"):
    os.mkdir("images/")    
if not os.path.exists("images/star_polygons/"):
    os.mkdir("images/star_polygons/")

for i in starDictionary.keys():
    for j in starDictionary[i]:
        docu = document.Document()
        docu.append(buildPath( pathshapes.starPolygon(i,j,100), {'style':'fill:none;stroke:black'}))
        docu.writeSVG("star_polygons/star_polygon-"+string.zfill(i,2)+ "_" + string.zfill(j,2)+ ".svg" )
        



