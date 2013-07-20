=============
pLAySVG: making graphical programming as easy as py
Download: http://github.com/cosmo-guffa/play-svg
Documentation: http://cosmo-guffa.github.io/play-svg/
Example script gallery: http://cosmic-spacecrafts.net/blog/playsvg-gallery
=============

pLAySVG is a python library that facilitates the generation and manipulation of SVG vector graphics.  It is designed to be easy to use, even for non-programmers.  It is geared toward educational and artistic use.  It contains code to  construct XML nodes corresponding to SVG elements, perform geometric operations, manipulate colors, and produce complex shapes.  

It can be used as a library to generate SVG images 'from scratch' by writing a python script that describes an image.    As well, pLAySVG can be used as a utility in the development of Inkscape plugins.  The project contains several examples of Inkscape scripts.

To install pLAySVG, first ensure you have python 2.4 installed.  Then extract the compressed file.  This will create a directory called play-svg.  Enter this directory using a command prompt and install the libraries by entering:
python setup.py install

To install the Inkscape plugins, copy all files in the inkex folder into your Inkscape extensions folder.  See http://wiki.inkscape.org/wiki/index.php/ScriptingHOWTO for more info on how to install Inkscape scripts.  You must first install pLAySVG for these plugins to work.  Linux users: the Inkscape plugins will automatically be installed for you :) 

  
