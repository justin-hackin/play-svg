#!/usr/bin/env python

import os
import shutil
import sys

thisFolder = os.curdir
print thisFolder
fileList = os.listdir(thisFolder)
fileList = [i for i in fileList if os.path.isfile(i) and (i.endswith(".svg")) ]

for thisFile in fileList:
    pngFile = thisFile.replace(".svg", ".png")
    print "Processing: "+thisFile+ " into " + pngFile
    os.spawnl(os.P_WAIT,'/usr/bin/inkscape','-f', thisFile, '-e', pngFile , '-C', '-d', '45')

    
	
