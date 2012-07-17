# Copyright (C) 2008-2009 Konstantin Lepa <konstantin.lepa@gmail.com>.
#
# This file is part of termcolor.
#
# termcolor is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 3, or (at your option) any later
# version.
#
# termcolor is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License
# along with termcolor.  If not, see <http://www.gnu.org/licenses/>.

"""ANSII Color formatting for output in terminal."""

import os
import copy

__ALL__ = [ 'termstyle','Termstyle']


class Termstyle:
    
    
    COLORS = {
                'grey' :    30,
                'red' :     31,
                'green' :   32,
                'yellow' :  33,
                'blue' :    34,
                'magenta' : 35,
                'cyan' :    36,
                'white' :   37
            }
            
    BACKGROUNDS = {
                    'grey' :    40,
                    'red' :     41,
                    'green' :   42,
                    'yellow' :  43,
                    'blue' :    44,
                    'magenta' : 45,
                    'cyan' :    46,
                    'white' :   47
                }
                
    ATTRIBUTES = {
                    'bold' :        1,
                    'dark' :        2,
                    'underlined' :  4,
                    'blinking' :    5,                  
                    'reversed' :    7,
                    'concealed' :   8
                }
    
    RESET = '\033[0m'
    
    ESCAPE_FORMAT = '\033[%dm'

    def __init__(self):
        self.attrs = []
        self.color = None
        self.background = None
    
        #normal mode, on puts it in background mode
        self.mode = 'normal'
        
        
    def copy(self,**kwargs):
        new = copy.deepcopy(self)
        for attr, value in kwargs.items():
            setattr(new, attr, value)
        return new
    
    def set_color(self,color):
        return self.copy(color=color)
        
    def set_background(self,color):
        return self.copy(background=color)
        
    def add_attribute(self,attribute):
        new = self.copy()
        new.attrs.append(attribute)      
        return new
        
    def set_mode(self,mode):
        return self.copy(mode=mode)
    
    def __getattr__(self,attr):
        """
        Allows for styles to be strung together using a syntax like
        termstyle.red.on.green.underlined
        """
        
        if attr in self.COLORS:        
            if self.mode == 'normal':
                return self.set_color(attr)
            else:
                return self.set_background(attr).set_mode('normal')
        
        elif attr in self.ATTRIBUTES:
            return self.add_attribute(attr)
            
        elif attr == 'on':        
            return self.set_mode('background')
                   
        else:
            raise AttributeError("No attribute found for termstyle %s"%attr)

        
    def __call__(self,text=""):
        
        if self.mode == 'background':
            raise SyntaxError("'on' must have a color after it to set the background")        

        if os.getenv('ANSI_COLORS_DISABLED'):
            return text
        
        else:    
            style_escapes = ""
            
            if self.color:
                style_escapes += (self.ESCAPE_FORMAT % self.COLORS[self.color])

            if self.background:
                style_escapes += (self.ESCAPE_FORMAT % self.BACKGROUNDS[self.background])

            for attr in self.attrs: # no-op if self.attrs is empty
                style_escapes += (self.ESCAPE_FORMAT % self.ATTRIBUTES[attr])

            return "%s%s%s" % (style_escapes, text, self.RESET)

    
    def __repr__(self):
        
        things = ["termstyle"]
        things.extend(self.attrs[:])
        
        if self.color is not None:
            things.append(self.color)
            
        if self.background is not None:
            things.append('on')
            things.append(self.background)
                 
        return ('.'.join(things))
        
    def __str__(self):
        return self(repr(self)) # :D
        
        
termstyle = Termstyle()

# should I pre-create the colors? :/

def test():
    """
    Test using your eyes (-)__(-)
    """
    
    print(('Current terminal type: ', os.getenv('TERM')))
    print('Test basic colors:')
    for key in termstyle.COLORS:
        print getattr(termstyle,key)("%s color" % key)
    print(('-' * 78))
    
    print('Test highlights:')
    for key in termstyle.COLORS:
        out = ""
        for background in termstyle.COLORS:
            out += getattr(getattr(termstyle,key).on,background)("%7s on %7s" % (key,background))
        print out
        
    print(('-' * 78))

    print('Test attributes:')
    
    for key in termstyle.ATTRIBUTES:
        print getattr(termstyle,key)("%s attribute" % key)

    print(('-' * 78))

    print('Test mixing:')
    
    print termstyle.underlined.red.on.blue("underlined red on blue")
    print termstyle.dark.bold.green.on.yellow("dark bold and green on yellow")


if __name__ == '__main__':
    test()
    
    
