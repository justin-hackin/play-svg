"""
#FIXME: gradient lxml conversion
CODE INVALID
DO NOT USE
""" 

from document import *
"""Classes for building gradients"""
class GradientStop:
    """a gradient stop that stores color, offset, and opacity"""
    def __init__(self, color, offset, opacity=1.0):
        self.color = color
        self.offset = offset
        self.opacity = opacity
 
class Gradient:
    """represents a generic gradient (abstract, neither linear nor radial)"""
    def __init__(self, id):
        self.id = id
        self.stopList = []
        self.transform = None
    def appendStop(self,stop):
        self.stopList.append(stop)
        return self
    def appendStopRefactor(self, stop):
        remaining = 1 - stop
        for i in range(len(self.stopList)):
            self.stopList[i].offset = self.stopList[i].offset
        return self
    def appendStopEquidistant(self, stop):
        totalStops = len(self.stopList)
        for i in range(len(self.stopList)):
            self.stopList[i].offset = float(1)/totalStops
        return self
    def ensureOffsetValid(self):
        #FIXME: DUHH, THIS IS WRONG, EACH SUCCESSIVE OFFSET NEEDS TO BE HIGHER THAT THE LAST
        offsetSum = 0.0
        for i in range(len(self.stopList)):
            offsetSum += self.stopList[i].offset
        if offsetSum !=+ 1.0: 
            return false
        else: 
            return true
    def rotateTransform(self, angal):
        self.transform = 'rotate(' + '%.5f)'%(360.0*angal)
        return self
    def createBalancedGradient(self, colors):
        self.stopList = []
        for i in range(len(colors)):
            self.appendStop(GradientStop(colors[i], float(i)/((len(colors))-1)))
        return self
    def createDefinition(self):
        definition = etree.Element('linearGradient')
        definition.set('id',self.id)    
      
        for i in range(len(self.stopList)):
            stopElement = etree.Element('stop')
            setAttributesFromDict(stopElement, {'style':'stop-color:'+unicode(self.stopList[i].color)+';stop-opacity:'+unicode(self.stopList[i].opacity) , 'offset': '%.5f'%(100.0*self.stopList[i].offset)+u"%" })
            
            definition.append(stopElement)
        return definition

class LinearGradient:
    """represents a linear gradient"""
    def __init__(self, id , gradient, ctrls):
        self.id = id
        self.ctrls = ctrls
        self.attributes = {}
        self.gradient = gradient
 
    def createDefinition(self):
        """creates an XML node to be stored in the defs of an SVG document"""
        self.attributes['id'] = unicode(self.id)
        if not self.ctrls == None :
            self.attributes['x1'] = '%.5f' %getattr(self.ctrls[0],'x') 
            self.attributes['y1'] = '%.5f' %getattr(self.ctrls[0],'y')
            self.attributes['x2'] = '%.5f' %getattr(self.ctrls[1],'x')
            self.attributes['y2'] = '%.5f' % getattr(self.ctrls[1],'y')
        self.attributes['gradientUnits'] = 'userSpaceOnUse'
        self.attributes["{http://www.w3.org/1999/xlink}href"] = '#'+self.gradient.id
        definition = etree.Element('linearGradient')
        setAttributesFromDict(definition, self.attributes)
         
        return definition
         
class RadialGradient:
    """represents a radial gradient"""
    def __init__(self, id,  gradient, radius,  ctrls):
        self.id = id
        self.radius = radius
        self.ctrls = ctrls
        self.attributes = {}
        self.gradient = gradient
 
    def createDefinition(self):
        """"creates an XML node to be stored in the defs of an SVG document"""
        self.attributes['id'] = self.id
        if not self.ctrls == None :
            self.attributes['cx'] = '%.5f' %getattr(self.ctrls[0],'x') 
            self.attributes['cy'] = '%.5f' %getattr(self.ctrls[0],'y')
            self.attributes['fx'] = '%.5f' %getattr(self.ctrls[1],'x')
            self.attributes['fy'] = '%.5f' % getattr(self.ctrls[1],'y')
            self.attributes['r'] = '%.5f' % self.radius
        self.attributes['gradientUnits'] = 'userSpaceOnUse'
        self.attributes["{http://www.w3.org/1999/xlink}href"] = '#'+self.gradient.id
        definition = etree.Element('radialGradient')
        setAttributesFromDict(definition, self.attributes)
                
        return definition
 
 

