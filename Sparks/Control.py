# Sparks - A vectorial shooter programmed by Haltux
# Copyright (C) 2010 Haltux
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import pygame
import sys
from Constants import *

def initialize_joystick():
    try:
        global button_joy
        global dir_joy
        global fire_joy 
        button_joy = pygame.joystick.Joystick(JOY_ID_BUTTONS)
        button_joy.init()
        
        dir_joy = pygame.joystick.Joystick(JOY_ID_DIR)
        dir_joy.init()
         
        fire_joy = pygame.joystick.Joystick(JOY_ID_FIRE)  
        fire_joy.init() # init instance
    except pygame.error:
        print 'joystick not found. Please check joystick ids in config file'
        sys.exit(0)

def getDirJoyXAxis():
    return dir_joy.get_axis(JOY_DIR_X)

def getDirJoyYAxis():
    return dir_joy.get_axis(JOY_DIR_Y)

def getFireJoyXAxis():
    return fire_joy.get_axis(JOY_FIRE_X)

def getFireJoyYAxis():
    return fire_joy.get_axis(JOY_FIRE_Y)



