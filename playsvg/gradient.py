from amara import binderytools
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
        offsetSum = 0.0
        for i in range(len(self.stopList)):
            offsetSum += self.stopList[i].offset
        if offsetSum !=+ 1.0: 
            return false
        else: 
            return true
    def rotateTransform(self, angal):
        self.transform = u'rotate(' + u'%.5f)'%(360.0*angal)
        return self
    def createBalancedGradient(self, colors):
        self.stopList = []
        for i in range(len(colors)):
            self.appendStop(GradientStop(colors[i], float(i)/((len(colors))-1)))
        return self
    def createDefinition(self, docu):
        definition = docu.xdoc.createElement(u'linearGradient') 
        setAttributesFromDict(definition, {u'id':unicode(self.id) })
        
        for i in range(len(self.stopList)):
            stopElement = docu.xdoc.createElement(u'stop')
            setAttributesFromDict(stopElement, {u'style':u'stop-color:'+unicode(self.stopList[i].color)+u';stop-opacity:'+unicode(self.stopList[i].opacity) , u'offset': u'%.5f'%(100.0*self.stopList[i].offset)+u"%" })
            
            definition.appendChild(stopElement)
        return definition

class LinearGradient:
    """represents a linear gradient"""
    def __init__(self, id , gradient, ctrls):
        self.id = id
        self.ctrls = ctrls
        self.attributes = {}
        self.gradient = gradient

    def createDefinition(self, docu):
        """creates an XML node to be stored in the defs of an SVG document"""
        self.attributes[u'id'] = unicode(self.id)
        if not self.ctrls == None :
            self.attributes[u'x1'] = u'%.5f' %getattr(self.ctrls[0],'x') 
            self.attributes[u'y1'] = u'%.5f' %getattr(self.ctrls[0],'y')
            self.attributes[u'x2'] = u'%.5f' %getattr(self.ctrls[1],'x')
            self.attributes[u'y2'] = u'%.5f' % getattr(self.ctrls[1],'y')
        self.attributes[u'gradientUnits'] = u'userSpaceOnUse'
        definition = docu.xdoc.createElement(u'linearGradient')
        setAttributesFromDict(definition, self.attributes)
        definition.setAttributeNS("http://www.w3.org/1999/xlink", "xlink:href", "#"+self.gradient.id)
        
        return definition
        
class RadialGradient:
    """represents a radial gradient"""
    def __init__(self, id,  gradient, radius,  ctrls):
        self.id = id
        self.radius = radius
        self.ctrls = ctrls
        self.attributes = {}
        self.gradient = gradient

    def createDefinition(self, docu):
        """"creates an XML node to be stored in the defs of an SVG document"""
        self.attributes[u'id'] = unicode(self.id)
        if not self.ctrls == None :
            self.attributes[u'cx'] = u'%.5f' %getattr(self.ctrls[0],'x') 
            self.attributes[u'cy'] = u'%.5f' %getattr(self.ctrls[0],'y')
            self.attributes[u'fx'] = u'%.5f' %getattr(self.ctrls[1],'x')
            self.attributes[u'fy'] = u'%.5f' % getattr(self.ctrls[1],'y')
            self.attributes[u'r'] = u'%.5f' % self.radius
        self.attributes[u'gradientUnits'] = u'userSpaceOnUse'
        definition = docu.xdoc.createElement(u'radialGradient')
        setAttributesFromDict(definition, self.attributes)
        definition.setAttributeNS("http://www.w3.org/1999/xlink", "xlink:href", "#"+self.gradient.id)
          
        
        return definition



