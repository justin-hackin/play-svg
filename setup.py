#!/usr/bin/env python

from distutils.core import setup
import os
import glob

dataFiles = []
if os.name == "posix":
    print "Inkscape extensions will be automatically installed on this Linux-based system"
    dataFiles.append(("/usr/share/inkscape/extensions/", [i for i in glob.glob(os.path.join("inkex", "*.*"))] ))
else:
    print "You are not running Linux, therefore you must install Inkscape extensions manually by copying files in the inkex directory to the Inkscape extensions directory on your system"

setup(name='playsvg',
      version='0.2',
      description='playsvg: making graphical programming as easy as py',
      author='playful_geometr',
      author_email='justinbarca@gmail.com',
      url='http://sourceforge.net/projects/play-svg/',
      packages=['playsvg'],
      data_files=dataFiles
      #data_files = [("scripts",[os.path.join("scripts", i) for i in glob.glob(os.path.join("scripts *.py"))] ), ("", ["README.TXT"]), ("inkex",[os.path.join("inkex", i) for i in glob.glob(os.path.join("inkex *.py"))] )  ]
     )
