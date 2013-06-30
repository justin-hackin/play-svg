==============
Basic tutorial
==============

It is suggested you have a basic understanding of cartesian geometry and SVG syntax before you begin, but if you don't you can probably learn both as you go along.
	
########
Geometry
########
	
	pLAySVG has a co-ordinate system that is slightly different from native SVG documents, namely in that (0,0) lies in the center of the document rather than the bottom left.  It bears a resemblence to the cartesian system you probably learned in school, such that:
	 * (0,0) is in the center of the document 
	 * (10,0) is to the right of center
	 * (-10,0) is to the left of center
	 * (0,10) is above center
	 * (0,10) is below center
	  
	
	To plot anything you'll need to start working with the geometry module.  Lets include it and define some ponts.  You can run these examples from the python console or cut and paste these snippets into a .py document:: 
	
		from playsvg.geom import *
		pointA = Point() # a point at (0,0)
		pointB = Point(10,10)
		print "Position of pointA:" + str(pointA)
		print "Position of pointB:" + str(pointB) 
	
	
	We can use operators to create some new points::
	
		pointC = pointB + Point(12,7)
		pointD = pointC - Point(7,12)
		pointE = pointD.scale(10) 
		print "Position of pointC:" + str(pointC)
		print "Position of pointD:" + str(pointD)
		print "Position of pointE:" + str(pointE)
	
##########
SVG coding
##########
	
	OK, so now lets get to making some SVG with our points. You'll need to include the document and element libraries::   
	
		from playsvg.document import *
		from playsvg.element import *
	
	Now we can create a document::  
	
		docu = Document(gridSize=1080) #if brackets are empty, gridSize=640
	
Lines
=====	
	
		Its time to draw a line and write it to a file::
			
			firstLine = buildLine(pointA, pointB)
			docu.append(firstLine)
			print "Here's our document output:"
			print "-----------------------------"
			str(docu)
			docu.writeSVG("hello.svg")
		
		
		`Inkscape <http://inkscape.org/>`_ is reccomended to view the output of the script.  With it you can easily view the SVG image and the SVG code at the same time.  You will find hello.svg in the "images" folder, which was generated inside the folder you ran your script in (if it did not already exist). Alternately, you could have the file written to an absolute path like this::
	
			docu.writeSVG("/home/user/hello.svg", pathAbsolute=True)
		
		or for Windows users it will look something more like::
	
			docu.writeSVG("C:\\users\\User1\\hello.svg", pathAbsolute=True)

Circles
=======
	
		Lets draw some circles on the nodes of our line::	
		
			circleA = buildCircle(pointA, 5) #center , radius 
			circleB = buildCircle(pointB, 5)
			docu.append(firstLine)
			print "Here's our document output:"
			print "-----------------------------"
			str(docu)
			docu.writeSVG("hello.svg")

Paths
=====
	
		pLAySVG uses a special class called PathData to store and manipulate path data as seen here::
		
			pathABC = PathData().moveTo(pointA).lineTo(pointB).lineTo(pointC)
			pathABCsvg = buildPath(pathABC)
			docu.append(pathABCsvg)
		
		The PathData object implements all of the other path commands including beziers, arcs, close path, etc.    
				
Styles and other attributes
===========================
	
		Most of the buildXXX functions have a default style they use, defined by a dictionary as such::
	
			defaultStyleAttrs = { "style": "fill:none;stroke:black;stroke-width:1"}
	
		You can define your own attributes dictionary instead and pass it to buildLine::
	
			myStyleAttrs = { "style": "fill:none;stroke:red;stroke-width:10"; "id":"secondLine"}
			secondLine = buildLine(pointB, pointC, myStyleAttrs)
			docu.append(secondLine)
	
		Or, if you want to keep the default style and just add the id::
	
			myStyleAttrs = defaultStyleAttrs #imported with element module
			myStyleAttrs["id"] = "secondLine"
			secondLine = buildLine(pointB, pointC, myStyleAttrs)
		
#############
Learning more
#############

	pLAySVG contains a large number of example scripts in its scripts/ folder.  A great way to learn more about pLAySVG and its functionality is to look through these scripts, run them, view their output, and manipulate them to see how their output changes.  You can also refer to the module sections for more details on the API and available classes and methods.	
	
	

