#!/usr/bin/env python

from distutils.core import setup
import os
import glob

setup(name='playsvg',
      version='1.0',
      description='playsvg: making graphical programming as easy as py',
      author='imagenerator',
      author_email='touchmewithsynchronicpulses@gmail.com',
      url='http://sourceforge.net/projects/play-svg/',
      packages=['playsvg'],
      data_files = [("scripts",[os.path.join("scripts", i) for i in glob.glob(os.path.join("scripts *.py"))] )  ]
     )