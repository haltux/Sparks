'''
Created on 9 mai 2010

@author: Julien
'''
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



import sys, os
import math, random

import pygame
from pygame.locals import *

from Game import *
from Menu import *
from Constants import *

import cProfile

def Run():
    pygame.init()  
    initialize_joystick()
    if sys.platform in ["win32", "win64"]:
        os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.display.set_caption("Sparks")
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.FULLSCREEN)
    game = MainMenu(screen)
    game.Run()

Run()
#cProfile.run('Run()', 'saprof.log')
