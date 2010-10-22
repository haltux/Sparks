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


import ConfigParser
import os

global config
try:
    config
except NameError:
    config = ConfigParser.ConfigParser()
    config.readfp(open(os.path.join(".", "sparks.cfg")))
   
    SCREEN_WIDTH = int(config.get("graphics","screen_width"))
    SCREEN_HEIGHT = int(config.get("graphics","screen_height"))
    
    USE_ANTIALIAS = int(config.get("graphics","antialias"))
    
    
    DRAW_WIDTH = int(config.get("graphics","draw_width"))
    
    #maximum number of bulls (basic enemies) on the screen. decrease this if the game runs too slowly
    MAX_BULL = int(config.get("graphics","max_sprites"))
    PRECOMPUTE_SPRITES = int(config.get("graphics","precompute_sprites"))
    DO_NOT_PRECOMPUTE_BIG_SPRITES = int(config.get("graphics","do_not_precompute_big_sprites"))
    MAX_FPS = int(config.get("graphics","max_fps"))
    
    
    #joystick ID. should be set to 1 to use secondary joystick. should be changed to be configurable
    JOYSTICK_ID = int(config.get("control","joystick_id"))#0
    JOY_FIRE = int(config.get("control","joy_fire"))#2
    JOY_ESCAPE = int(config.get("control","joy_escape"))#8
    JOY_PAUSE = int(config.get("control","joy_pause"))#9
    JOY_BACK = int(config.get("control","joy_menu_back"))


#END OF CONFIGURATION CONSTANTS


#changing these constants will change the size of each objects on the screen, therefore it will change the gameplay and the difficulty
WORLD_WIDTH = 800*256
WORLD_HEIGHT = WORLD_WIDTH * SCREEN_HEIGHT / SCREEN_WIDTH  
SPRITE_SCALE = SCREEN_WIDTH/800.0


APPEARANCE_DELAY = 100



SHIP_NORMAL_POINTS = ((-10,-10), (10,0), (-10, 10))
SHIP_ACCEL_POINTS  = SHIP_NORMAL_POINTS
ASTEROID1_POINTS   = ((-8, -30), (-30, -9), (-15, 2), (-30, 4), (-15, 30), (0, 10), (0, 30), (16, 30), (30, 4), (30, -10), (16, -30))
ASTEROID2_POINTS   = ((-13, -30), (-30, -16), (-21, -3), (-30, 11), (-13, 30), (-4, 16), (12, 26), (30, 6), (14, -8), (27, -15), (14, -30), (0, -21))
ASTEROID3_POINTS   = ((-14, -30), (-30, -16), (-30, 14), (-13, 30), (10, 30), (30, 10), (22, -2), (30, -15), (16, -30), (0, -13))
ASTEROID4_POINTS   = ((-15, -30), (-5, -15), (-30, -15), (-30, 6), (-15, 30), (7, 20), (15, 30), (30, 12), (8, 0), (30, -8), (30, -15), (0, -30))
UFO_POINTS = ((-7, -20), (-12, -7), (-30, 5), (-11, 19), (11, 19), (30, 5), (12, -7), (7, -20), (-7, -20), (-12, -7), (12, -7), (30, 5), (-30, 5))
SHOT_POINTS = ((0, 0), (10, 0))
BULL_POINTS = ((-10,-10),(0,-6),(10,-10),(6,0),(10,10),(0,6),(-10,10),(-6,0),(-10,-10))
COWARD_POINTS = ((-10,-10),(10,-10),(0,0),(10,10),(-10,10),(-10,-10))
BERZERKER_POINTS = ((-10,-10),(10,-10),(-10,10),(10,10),(-10,-10))
MISSILE_POINTS = ((-5,-1),(5,0),(-5,1),(-5,-1))
CORNERKEEPER_POINTS = ((-3,0),(0,-3),(3,0),(0,3))

BIG_SPRITE_THRESHOLD = 40