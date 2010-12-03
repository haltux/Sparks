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
import sys
import shutil


VERSION = 3

config_parser = ConfigParser.ConfigParser()

if len(sys.argv)==1:
    config_file = os.path.join(os.path.dirname(__file__), "cfg", "sparks-pc.cfg")
else:
    config_file = sys.argv[1]

config_parser.readfp(open(config_file))

if int(config_parser.get("version","number")) != VERSION:
    print "Configuration file is an outdated version.  Moving it to {0}.old".format(config_file)
    shutil.move(config_file, "{0}.old".format(config_file))
    sys.exit(1)


SCREEN_WIDTH = int(config_parser.get("graphics","screen_width"))
SCREEN_HEIGHT = int(config_parser.get("graphics","screen_height"))
COLOR_DEPTH = int(config_parser.get("graphics","color_depth"))
FULLSCREEN = int(config_parser.get("graphics","fullscreen"))
USE_ANTIALIAS = int(config_parser.get("graphics","antialias"))
NB_PARTICLES_PER_EXPLOSION = int(config_parser.get("graphics","nb_particles_per_explosion"))




DRAW_WIDTH = int(config_parser.get("graphics","draw_width"))

#maximum number of bulls (basic enemies) on the screen. decrease this if the game runs too slowly
MAX_BULL = int(config_parser.get("graphics","max_sprites"))
PRECOMPUTE_SPRITES = int(config_parser.get("graphics","precompute_sprites"))
DO_NOT_PRECOMPUTE_BIG_SPRITES = int(config_parser.get("graphics","do_not_precompute_big_sprites"))
MAX_FPS = int(config_parser.get("graphics","max_fps"))


#joystick ID. should be set to 1 to use secondary joystick. should be changed to be configurable
JOY_ID_BUTTONS = int(config_parser.get("control","joystick_id_buttons"))#0
JOY_FIRE = int(config_parser.get("control","joy_fire"))#2
JOY_ESCAPE = int(config_parser.get("control","joy_escape"))#8
JOY_PAUSE = int(config_parser.get("control","joy_pause"))#9
JOY_BACK = int(config_parser.get("control","joy_menu_back"))
JOY_FPS = int(config_parser.get("control","joy_fps"))

JOY_ID_DIR = int(config_parser.get("control","joy_id_dir"))
JOY_ID_FIRE = int(config_parser.get("control","joy_id_fire"))    

JOY_DIR_X = int(config_parser.get("control","joy_dir_x"))
JOY_DIR_Y = int(config_parser.get("control","joy_dir_y"))
JOY_FIRE_X = int(config_parser.get("control","joy_fire_x"))
JOY_FIRE_Y = int(config_parser.get("control","joy_fire_y"))    
       
        

#END OF CONFIGURATION CONSTANTS

GLOBAL_SPEED=60

#changing these constants will change the size of each objects on the screen, therefore it will change the gameplay and the difficulty
WORLD_WIDTH = 800*256
WORLD_HEIGHT = WORLD_WIDTH * SCREEN_HEIGHT / SCREEN_WIDTH  
SPRITE_SCALE = SCREEN_WIDTH/800.0


APPEARANCE_DELAY = 1500



SHIP_NORMAL_POINTS = ((-10,-10), (10,0), (-10, 10))
SHIP_ACCEL_POINTS  = SHIP_NORMAL_POINTS
ASTEROID1_POINTS   = ((-8, -30), (-30, -9), (-15, 2), (-30, 4), (-15, 30), (0, 10), (0, 30), (16, 30), (30, 4), (30, -10), (16, -30))
ASTEROID2_POINTS   = ((-13, -30), (-30, -16), (-21, -3), (-30, 11), (-13, 30), (-4, 16), (12, 26), (30, 6), (14, -8), (27, -15), (14, -30), (0, -21))
ASTEROID3_POINTS   = ((-14, -30), (-30, -16), (-30, 14), (-13, 30), (10, 30), (30, 10), (22, -2), (30, -15), (16, -30), (0, -13))
ASTEROID4_POINTS   = ((-15, -30), (-5, -15), (-30, -15), (-30, 6), (-15, 30), (7, 20), (15, 30), (30, 12), (8, 0), (30, -8), (30, -15), (0, -30))
UFO_POINTS = ((-7, -20), (-12, -7), (-30, 5), (-11, 19), (11, 19), (30, 5), (12, -7), (7, -20), (-7, -20), (-12, -7), (12, -7), (30, 5), (-30, 5))
SHOT_POINTS = ((0, 0), (20, 0))
BULL_POINTS = ((-10,-10),(0,-6),(10,-10),(6,0),(10,10),(0,6),(-10,10),(-6,0),(-10,-10))
COWARD_POINTS = ((-10,-10),(10,-10),(0,0),(10,10),(-10,10),(-10,-10))
BERZERKER_POINTS = ((-10,-10),(10,-10),(-10,10),(10,10),(-10,-10))
MISSILE_POINTS = ((-5,-1),(5,0),(-5,1),(-5,-1))
CORNERKEEPER_POINTS = ((-3,0),(0,-3),(3,0),(0,3))

BIG_SPRITE_THRESHOLD = 40

LEVEL_STEP_LENGTH = 100


