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
import pygame.locals 

import Game
import Menu 
import Control


import cProfile

import Constants

import Colors

def Run():
    pygame.init()  
    Control.initialize_joystick()
    if sys.platform in ["win32", "win64"]:
        os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.display.set_caption("Sparks")
    
    mode_flag=0
    if Constants.FULLSCREEN:
        mode_flag = pygame.FULLSCREEN
    
    if (Constants.COLOR_DEPTH>0):
        screen = pygame.display.set_mode((Constants.SCREEN_WIDTH,Constants.SCREEN_HEIGHT),mode_flag,Constants.COLOR_DEPTH)
    else:
        screen = pygame.display.set_mode((Constants.SCREEN_WIDTH,Constants.SCREEN_HEIGHT),mode_flag)

    Colors.init_colors()

    pygame.mouse.set_visible(0)
    game = Menu.MainMenu(screen)
    game.Run()

Run()
#cProfile.run('Run()', 'saprof.log')
