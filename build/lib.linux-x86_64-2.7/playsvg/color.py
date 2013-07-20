'''color manipulation module
all colors are represented as arrays or tuples of 3 [0,1) values except for hex colors i.e. #ffffff
'''
from __future__ import division
import math 


#>>>Taken from ASPN cookbook'''
def RGBToHex(rgb_array):
    """convert an array of RGB % values into a hex color string"""
    rgb_tuple = tuple([i*255 for i in rgb_array])
    """ convert an (R, G, B) tuple to #RRGGBB """
    hexcolor = '#%02x%02x%02x' % rgb_tuple
    # that's it! '%02x' means zero-padded, 2-digit hex values
    return hexcolor

def hexToRGB(colorstring):
    """ convert a hex color string  to an RGB array """
    colorstring = colorstring.strip()
    if colorstring[0] == '#': colorstring = colorstring[1:]
    if len(colorstring) != 6:
        raise ValueError, "input #%s is not in #RRGGBB format" % colorstring
    r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
    r, g, b = [float(int(n, 16))/256 for n in (r, g, b)]
    return [r, g, b]

def hexToPIL(colorstring):
    """ converts hex color string to a PIL-compatible integers"""
    colorstring = colorstring.strip()
    while colorstring[0] == '#': colorstring = colorstring[1:]
    # get bytes in reverse order to deal with PIL quirk
    colorstring = colorstring[-2:] + colorstring[2:4] + colorstring[:2]
    # finally, make it numeric
    color = int(colorstring, 16)
    return color

def PILToRGB(pil_array):
    """ convert a PIL-compatible integer into an RGB % array """
    pil_color = tuple(pil_array)
    hexstr = '%06x' % pil_color
    # reverse byte order
    r, g, b = hexstr[4:], hexstr[2:4], hexstr[:2]
    r, g, b = [int(n, 16) for n in (r, g, b)]
    return [r, g, b]

def PILToHex(pil_integer):
    """ convert a PIL-compatible integer into a  hex color string"""
    return RGBToHex(PILToRGB(pil_integer))

def RGBToPIL(rgb_array):
    
    return hexToPIL(RGBToHex(rgb_array))
#<<<Taken from ASPN cookbook
    
def tupleGradient(fromTuple, toTuple, gradationSteps):
    '''given 2 3-tuples i.e. ((fromR, fromG, fromB) (toR, toG, toB)) and an integer(in), returns a list of tuples which is a discrete gradation from one tuple to the other'''
    def roundFloat(floater):
        if floater - math.floor(floater) < 0.5:
            return int(math.floor(floater))
        else:
            return int(math.ceil(floater))
    
    gradation = [fromTuple]
    #WARNING: very unelegant for python
    difference = [toTuple[0] - fromTuple[0], toTuple[1] - fromTuple[1], toTuple[2] - fromTuple[2]] 
    iterations=gradationSteps-1
    for i in range(iterations):
            gradation.append((fromTuple[0]+ float(i)/(gradationSteps-1)*difference[0], \
            fromTuple[1]+ float(i)/(gradationSteps-1)*difference[1],\
            fromTuple[2]+ float(i)/(gradationSteps-1)*difference[2]))
    gradation.append(toTuple)
    #gradation =  [[roundFloat(float(elem)) for elem in tup]  for tup in gradation]
    #gradation = [(arrayTup[0], arrayTup[1], arrayTup[2]) for arrayTup in gradation]
    gradation = [RGBToHex(modTup) for modTup in gradation]
    return gradation
    
def RGBToHSL(color):
    r = color[0]
    g = color[1]
    b = color[2]
    
    rgb_max = max(max(r, g), b)
    rgb_min = min(min(r, g), b)
    delta = rgb_max - rgb_min
    hsl = [0.0, 0.0, 0.0]
    hsl[2] = (rgb_max + rgb_min)/2.0
    if delta == 0:
        hsl[0] = 0.0
        hsl[1] = 0.0
    else:
        if hsl[2] <= 0.5:
            hsl[1] = delta / (rgb_max + rgb_min)
        else:
            hsl[1] = delta / (2 - rgb_max - rgb_min)
        if r == rgb_max:
            hsl[0] = (g - b) / delta
        else:
            if g == rgb_max:
                hsl[0] = 2.0 + (b - r) / delta
            else:
                if b == rgb_max:
                    hsl[0] = 4.0 + (r - g) / delta
        hsl[0] = hsl[0] / 6.0
        if hsl[0] < 0:
            hsl[0] = hsl[0] + 1
        if hsl[0] > 1:
            hsl[0] = hsl[0] - 1
    return hsl

def HSLToRGB (color):
    def hue_2_rgb (v1, v2, h):
        if h < 0:
            h += 6.0
        if h > 6:
            h -= 6.0
        if h < 1:
            return v1 + (v2 - v1) * h
        if h < 3:
            return v2
        if h < 4:
            return v1 + (v2 - v1) * (4 - h)
        return v1
    
    h = color[0]
    s = color[1]
    l = color[2]
    v1 = 0
    v2 = 0
    rgb = [0, 0, 0]
    if s == 0:
        rgb[0] = l
        rgb[1] = l
        rgb[2] = l
    else:
        if l < 0.5:
            v2 = l * (1 + s)
        else:
            v2 = l + s - l*s
        v1 = 2*l - v2
        rgb[0] = hue_2_rgb (v1, v2, h*6 + 2.0)
        rgb[1] = hue_2_rgb (v1, v2, h*6)
        rgb[2] = hue_2_rgb (v1, v2, h*6 - 2.0)
    return rgb


    
if __name__ == "__main__":
    tupleArray = tupleGradient((1,1,1), (0,0,0), 10)
    tupleArray = [ [roundFloat(float(elem)*255) for elem in tup]  for tup in tupleArray]
    print tupleArray
    tupleArray = [(arrayTup[0], arrayTup[1], arrayTup[2]) for arrayTup in tupleArray]
    print tupleArray
    tupleArray = [RGBToHTMLColor(modTup) for modTup in tupleArray]
    print tupleArray
    
    
