'''Document is the SVG document representation, provides file I/O and access to the DOM '''
import os
from copy import copy
from element import *
from geom import *
try:
    import xml.dom.ext
    import xml.dom.minidom
    import xml.dom.ext.reader.Sax2
    import xml.xpath
except:
    sys.exit('The document.py module requires PyXML. Please download the latest version from <http://pyxml.sourceforge.net/>.')

def setAttributesFromDict(element,dict):
    for key, val in dict.items():
        element.setAttribute(key, val)

##def allSubnodesIteratorHelp(subnodes, node):
##    children = node.xml_children
##    for i in range(len(children)):
##        if not type(children[i]).__name__ == 'unicode' and not type(children[i]).__name__ == 'metadata' :
##            subnodes.append(children[i])
##            allSubnodesIteratorHelp(subnodes, subnodes[-1])
##    return subnodes
##def allSubnodesIterator(node):
##    subnodes = []
##    return allSubnodesIteratorHelp(subnodes, node)
    


class Document:
    def __init__(self, document = None, file=None,  gridSize=295, alignment='mm'):
        #FIXME: test file support
        #FIXME: add support for different canvas alignments and sizes of document
        if file != None:
            reader = xml.dom.ext.reader.Sax2.Reader()
            try:
                stream = open(file,'r')
            except:
                print 'failed to parse SVG document'
        else:
            #create SVG document elements from scratch
            if document == None:
                self.xdoc= xml.dom.getDOMImplementation().createDocument(None, 'svg',None)
                svgAttributes = {u'xmlns':'http://www.w3.org/2000/svg', u'height':unicode(gridSize*2), u'width':unicode(gridSize*2)}  
                setAttributesFromDict(self.xdoc.documentElement, svgAttributes)
                self.xdoc.documentElement.setAttributeNS( 'http://www.w3.org/1999/xlink', 'href:xlink', 'xlink')
                self.defs = self.xdoc.createElement(u'defs')
                self.xdoc.documentElement.appendChild(self.defs)
            else:
                self.xdoc = document
            
            
            #append canvas, the co-ordinate system group
            canvasAtts = {u'id':u'canvas', u'transform':(u'matrix(1,0,0,-1,0,'+str(gridSize*2) +u') ' + u'translate('+unicode(gridSize)+ u','+ unicode(gridSize)+u')')}
            self.canvas = self.xdoc.createElement(u'g')
            setAttributesFromDict(self.canvas, canvasAtts)
            self.xdoc.documentElement.appendChild(self.canvas)
    
    def appendElement(self, element):
        """appends element to canvas"""
        self.canvas.appendChild(element)
    def makeGroup(self, id=None):
        """returns a group element"""
        groupElement = self.xdoc.createElement('g')
        if id != None:
            groupElement.setAttribute('id', id)
        return groupElement
    def appendDefinition(self, definition):
        """adds element to defs"""
        self.defs.appendChild(definition)
    def writeSVG(self, filename ):
        """writes SVG document to file"""
        imagePath = os.getcwd() + "/images/"
        if not os.path.exists(imagePath):
            os.mkdir(imagePath)  
        file = open((imagePath+filename),'w')
        xml.dom.ext.PrettyPrint(self.xdoc, file)
        file.close()


if __name__ == "__main__":
    docu = Document()
    docu.appendElement(buildCircle(docu, Point(0,0), 100, {u'style':u'fill:black'}))
    docu.writeSVG('testdocum.svg')
    print 'done'
    

