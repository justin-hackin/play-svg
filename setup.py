#!/usr/bin/env python

#FIXME: "sudo python setup.py install" copies extensions with owner as root, making the extensions inaccessible to anyone but root user
  
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
      version='0.3',
      description='playsvg: making graphical programming as easy as py',
      author='cosmo-guffa',
      author_email='cosmo.guffa@gmail.com',
      url='https://github.com/cosmo-guffa/play-svg',
      packages=['playsvg'],
      data_files=dataFiles
      #data_files = [("scripts",[os.path.join("scripts", i) for i in glob.glob(os.path.join("scripts *.py"))] ), ("", ["README.TXT"]), ("inkex",[os.path.join("inkex", i) for i in glob.glob(os.path.join("inkex *.py"))] )  ]
     )

